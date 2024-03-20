/*
 * TencentBlueKing is pleased to support the open source community by making
 * 蓝鲸智云 - PaaS 平台 (BlueKing - PaaS System) available.
 * Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
 * Licensed under the MIT License (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 *	http://opensource.org/licenses/MIT
 *
 * Unless required by applicable law or agreed to in writing, software distributed under
 * the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
 * either express or implied. See the License for the specific language governing permissions and
 * limitations under the License.
 *
 * We undertake not to change the open source license (MIT license) applicable
 * to the current version of the project delivered to anyone in the future.
 */

package controllers

import (
	"context"
	"fmt"

	"github.com/getsentry/sentry-go"
	"github.com/pkg/errors"
	apierrors "k8s.io/apimachinery/pkg/api/errors"
	apimeta "k8s.io/apimachinery/pkg/api/meta"
	metav1 "k8s.io/apimachinery/pkg/apis/meta/v1"
	"k8s.io/apimachinery/pkg/fields"
	"k8s.io/apimachinery/pkg/runtime"
	"k8s.io/apimachinery/pkg/types"
	ctrl "sigs.k8s.io/controller-runtime"
	"sigs.k8s.io/controller-runtime/pkg/client"
	"sigs.k8s.io/controller-runtime/pkg/controller"
	"sigs.k8s.io/controller-runtime/pkg/controller/controllerutil"
	"sigs.k8s.io/controller-runtime/pkg/handler"
	logf "sigs.k8s.io/controller-runtime/pkg/log"
	"sigs.k8s.io/controller-runtime/pkg/reconcile"
	"sigs.k8s.io/controller-runtime/pkg/source"

	paasv1alpha1 "bk.tencent.com/paas-app-operator/api/v1alpha1"
	paasv1alpha2 "bk.tencent.com/paas-app-operator/api/v1alpha2"
	"bk.tencent.com/paas-app-operator/pkg/controllers/dgroupmapping"
	dgmingress "bk.tencent.com/paas-app-operator/pkg/controllers/dgroupmapping/ingress"
)

// NewDomainGroupMappingReconciler will return a DomainGroupMappingReconciler with given k8s client and scheme
func NewDomainGroupMappingReconciler(cli client.Client, scheme *runtime.Scheme) *DomainGroupMappingReconciler {
	return &DomainGroupMappingReconciler{client: cli, scheme: scheme}
}

// DomainGroupMappingReconciler reconciles a DomainGroupMapping object
type DomainGroupMappingReconciler struct {
	client client.Client
	scheme *runtime.Scheme
}

// ErrReferenceUndefined means that the DomainGroupMapping object didn't define any referenced resource.
var ErrReferenceUndefined = errors.New("reference is not defined")

//+kubebuilder:rbac:groups=paas.bk.tencent.com,resources=domaingroupmappings,verbs=get;list;watch;create;update;patch;delete
//+kubebuilder:rbac:groups=paas.bk.tencent.com,resources=domaingroupmappings/status,verbs=get;update;patch
//+kubebuilder:rbac:groups=paas.bk.tencent.com,resources=domaingroupmappings/finalizers,verbs=update

// Reconcile is part of the main kubernetes reconciliation loop which aims to
// move the current state of the cluster closer to the desired state.
func (r *DomainGroupMappingReconciler) Reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	result, err := r.reconcile(ctx, req)
	if err != nil {
		sentry.CaptureException(
			errors.WithMessagef(
				err,
				"error found while executing DomainGroupMapping (%s/%s) reconciler loop",
				req.Namespace,
				req.Name,
			),
		)
	}
	return result, err
}

func (r *DomainGroupMappingReconciler) reconcile(ctx context.Context, req ctrl.Request) (ctrl.Result, error) {
	log := logf.FromContext(ctx)
	dgmapping := &paasv1alpha1.DomainGroupMapping{}
	err := r.client.Get(ctx, req.NamespacedName, dgmapping)
	if err != nil {
		log.Info(fmt.Sprintf("unable to fetch DomainGroupMapping %v", req.NamespacedName))
		return ctrl.Result{}, client.IgnoreNotFound(err)
	}

	// Handle deletion and finalizer related logics:
	// If object is not under deletion, add our finalizer
	if dgmapping.DeletionTimestamp.IsZero() {
		if !controllerutil.ContainsFinalizer(dgmapping, paasv1alpha1.DGroupMappingFinalizerName) {
			controllerutil.AddFinalizer(dgmapping, paasv1alpha1.DGroupMappingFinalizerName)
			if err = r.client.Update(ctx, dgmapping); err != nil {
				return ctrl.Result{}, err
			}
		}
	} else {
		// The resource is under deletion
		if controllerutil.ContainsFinalizer(dgmapping, paasv1alpha1.DGroupMappingFinalizerName) {
			// Our finalizer is present, handle any external dependency
			if err = r.SyncDeletion(ctx, dgmapping); err != nil {
				return ctrl.Result{}, err
			}
			controllerutil.RemoveFinalizer(dgmapping, paasv1alpha1.DGroupMappingFinalizerName)
			if err = r.client.Update(ctx, dgmapping); err != nil {
				return ctrl.Result{}, err
			}
			// Stop reconciliation as the item is being deleted
			return ctrl.Result{}, nil
		}
	}

	// Start the main sync procedure
	if err = r.Sync(ctx, dgmapping); err != nil {
		return ctrl.Result{RequeueAfter: paasv1alpha2.DefaultRequeueAfter}, err
	}
	return ctrl.Result{}, nil
}

// Sync DomainGroupMapping object, move it to desired state by manipulating Ingress
// and BkApp resources.
func (r *DomainGroupMappingReconciler) Sync(ctx context.Context, dgmapping *paasv1alpha1.DomainGroupMapping) error {
	log := logf.FromContext(ctx)
	bkapp, errRef := r.GetRef(ctx, dgmapping)
	// Update status first
	if err := r.syncRefErrStatus(ctx, dgmapping, errRef); err != nil {
		log.Error(err, "Error updating status", "DGroupMappingName", dgmapping.Name)
		return errors.Wrap(errRef, err.Error())
	}
	if errRef != nil {
		if apierrors.IsNotFound(errRef) || errors.Is(errRef, ErrReferenceUndefined) {
			log.Info(fmt.Sprintf("Reference info empty or can't be found: %s", errRef))
			log.Info("Deleting related Ingresses")
			if errDel := dgroupmapping.DeleteIngresses(ctx, r.client, dgmapping); errDel != nil {
				log.Error(errDel, "Delete ingresses failed", "DGroupMappingName", dgmapping.Name)
				return errors.Wrap(errRef, errDel.Error())
			}
			return nil
		}
		log.Error(errRef, "Unable to get referenced object from mapping")
		return errRef
	}

	// Start sync procedure only if the referenced BkApp exists
	mappingSyncer := dgroupmapping.NewDGroupMappingSyncer(r.client, &bkapp)
	domainGroups, err := mappingSyncer.Sync(ctx, dgmapping)
	if err != nil {
		log.Error(err, "Fail to sync mapping", "DGroupMappingName", dgmapping.Name)
		return err
	}

	// Sync status field in the end
	if err = r.syncProcessedStatus(ctx, &bkapp, dgmapping, domainGroups); err != nil {
		log.Error(err, "Error updating status for processed item", "DGroupMappingName", dgmapping.Name)
		return err
	}
	return nil
}

// SyncDeletion method handle deletions of DomainGroupMapping resources
func (r *DomainGroupMappingReconciler) SyncDeletion(
	ctx context.Context,
	dgmapping *paasv1alpha1.DomainGroupMapping,
) error {
	// Delete all related Ingresses
	if err := dgroupmapping.DeleteIngresses(ctx, r.client, dgmapping); err != nil {
		return err
	}

	bkapp, err := r.GetRef(ctx, dgmapping)
	if err != nil {
		// Ignore when ref BkApp can't be found
		if apierrors.IsNotFound(err) || errors.Is(err, ErrReferenceUndefined) {
			return nil
		}
		return errors.WithStack(err)
	}
	// Update bkapp's "status.Addresses" field
	// TODO: When multiple DomainGroupMapping objs reference to one same BkApp object,
	// Only remove addresses which are bound with current mapping object.

	// deep copy bkapp to generate merge-patch
	originalBkApp := bkapp.DeepCopy()
	// Update BkApp's status
	bkapp.Status.Addresses = nil
	return errors.WithStack(r.client.Status().Patch(ctx, &bkapp, client.MergeFrom(originalBkApp)))
}

// GetRef gets the BkApp object which is referenced by given mapping object
func (r *DomainGroupMappingReconciler) GetRef(
	ctx context.Context,
	dgmapping *paasv1alpha1.DomainGroupMapping,
) (paasv1alpha2.BkApp, error) {
	refObj := paasv1alpha2.BkApp{}
	if dgmapping.Spec.Ref.Name == "" {
		return refObj, errors.WithStack(ErrReferenceUndefined)
	}

	// Only the same namespace is supported
	// TODO: Handler different apiVersions
	key := client.ObjectKey{Namespace: dgmapping.Namespace, Name: dgmapping.Spec.Ref.Name}
	if err := r.client.Get(ctx, key, &refObj); err != nil {
		return refObj, errors.Wrap(err, "fail to get referenced obj")
	}
	return refObj, nil
}

// Sync domain group mapping's status field by err which was produced during finding referenced object.
func (r *DomainGroupMappingReconciler) syncRefErrStatus(
	ctx context.Context, dgmapping *paasv1alpha1.DomainGroupMapping, err error,
) error {
	// Skip updating status if no error
	if err == nil {
		return nil
	}

	var reason, message string
	if apierrors.IsNotFound(err) {
		message = "Referenced object can't be found"
		reason = "RefNotFound"
	} else {
		message = "Error getting referenced object"
		reason = "RefGettingError"
	}
	apimeta.SetStatusCondition(&dgmapping.Status.Conditions, metav1.Condition{
		Type:    paasv1alpha1.DomainMappingProcessed,
		Status:  metav1.ConditionFalse,
		Reason:  reason,
		Message: message,
	})
	return r.client.Status().Update(ctx, dgmapping)
}

// Sync both mapping and bkapp's status field when the reconciler
// has finished processing current mapping obj.
//
// - bkapp is the BkApp obj which is referenced by DomainGroupMapping.
// - domainGroups is the collection of domain groups which is calculated from
// current resource.
func (r *DomainGroupMappingReconciler) syncProcessedStatus(
	ctx context.Context,
	bkapp *paasv1alpha2.BkApp,
	dgmapping *paasv1alpha1.DomainGroupMapping,
	domainGroups []dgmingress.DomainGroup,
) error {
	// Update mapping obj's conditions
	apimeta.SetStatusCondition(&dgmapping.Status.Conditions, metav1.Condition{
		Type:   paasv1alpha1.DomainMappingProcessed,
		Status: metav1.ConditionTrue,
		Reason: "Processed",
	})
	if err := r.client.Status().Update(ctx, dgmapping); err != nil {
		return errors.WithStack(err)
	}

	// deep copy bkapp to generate merge-patch
	originalBkApp := bkapp.DeepCopy()
	// Update BkApp's status
	bkapp.Status.Addresses = ToAddressableStatus(domainGroups)
	return errors.WithStack(r.client.Status().Patch(ctx, bkapp, client.MergeFrom(originalBkApp)))
}

// BkAppIndexField is the name for indexing DomainGroupMapping
const BkAppIndexField = ".Spec.Ref.BkAppName"

// SetupWithManager sets up the controller with the Manager.
func (r *DomainGroupMappingReconciler) SetupWithManager(
	ctx context.Context, mgr ctrl.Manager, opts controller.Options,
) error {
	// Build an index to query DomainGroupMappings by BkApp later
	err := mgr.GetFieldIndexer().
		IndexField(ctx, &paasv1alpha1.DomainGroupMapping{}, BkAppIndexField, getDGMappingOwnerNames)
	if err != nil {
		return err
	}

	// A handler function which transform BkApp's events into DomainGroupMapping's
	// enqueue requests.
	handleEnqueueBkApp := func(bkapp client.Object) []reconcile.Request {
		// List attached DomainGroupMapping objects by index
		dgmappings := &paasv1alpha1.DomainGroupMappingList{}
		listOps := &client.ListOptions{
			FieldSelector: fields.OneTermEqualSelector(BkAppIndexField, bkapp.GetName()),
			Namespace:     bkapp.GetNamespace(),
		}
		// 不复用 ctx 讨论：https://github.com/TencentBlueKing/blueking-paas/pull/154/files#r1080770867
		if err = r.client.List(context.TODO(), dgmappings, listOps); err != nil {
			return []reconcile.Request{}
		}

		// Build requests for related DomainGroupMapping resources and return
		reqs := make([]reconcile.Request, len(dgmappings.Items))
		for i, mapping := range dgmappings.Items {
			reqs[i] = reconcile.Request{
				NamespacedName: types.NamespacedName{
					Namespace: bkapp.GetNamespace(),
					Name:      mapping.Name,
				},
			}
		}
		return reqs
	}
	return ctrl.NewControllerManagedBy(mgr).
		For(&paasv1alpha1.DomainGroupMapping{}).
		WithOptions(opts).
		Watches(&source.Kind{
			Type: &paasv1alpha2.BkApp{},
		}, handler.EnqueueRequestsFromMapFunc(handleEnqueueBkApp)).
		Complete(r)
}

func getDGMappingOwnerNames(rawObj client.Object) []string {
	dgmapping := rawObj.(*paasv1alpha1.DomainGroupMapping)
	if dgmapping.Spec.Ref.Kind == paasv1alpha2.KindBkApp && dgmapping.Spec.Ref.Name != "" {
		return []string{dgmapping.Spec.Ref.Name}
	}
	return nil
}

// ToAddressableStatus receives a list of DomainGroups, turns them into
// addressable objects which can be used for BkApp's status field
func ToAddressableStatus(groups []dgmingress.DomainGroup) []paasv1alpha2.Addressable {
	var results []paasv1alpha2.Addressable
	for _, group := range groups {
		for _, d := range group.Domains {
			for _, url := range d.GetURLs() {
				results = append(results, paasv1alpha2.Addressable{SourceType: string(group.SourceType), URL: url})
			}
		}
	}
	return results
}
