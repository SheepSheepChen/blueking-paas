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

package metric

import (
	paasv1alpha2 "bk.tencent.com/paas-app-operator/api/v1alpha2"
	"time"
)

// ReportHooksFinishedErrors ...
func ReportHooksFinishedErrors(bkapp *paasv1alpha2.BkApp) {
	HooksFinishedErrors.WithLabelValues(bkapp.Name, bkapp.Namespace).Inc()
}

// ReportDeleteResourcesErrors ...
func ReportDeleteResourcesErrors(bkapp *paasv1alpha2.BkApp) {
	DeleteResourcesErrors.WithLabelValues(bkapp.Name, bkapp.Namespace).Inc()
}

// ReportDeployActionUpdateBkappStatusErrors ...
func ReportDeployActionUpdateBkappStatusErrors(bkapp *paasv1alpha2.BkApp) {
	DeployActionUpdateBkappStatusErrors.WithLabelValues(bkapp.Name, bkapp.Namespace, bkapp.Status.DeployId).Inc()
}

// ReportDeleteOutdatedDeployErrors ...
func ReportDeleteOutdatedDeployErrors(bkapp *paasv1alpha2.BkApp, deploymentName string) {
	DeleteOutdatedDeployErrors.WithLabelValues(bkapp.Name, bkapp.Namespace, deploymentName).Inc()
}

// ReportDeployExpectedDeployErrors ...
func ReportDeployExpectedDeployErrors(bkapp *paasv1alpha2.BkApp, deploymentName string) {
	DeployExpectedDeployErrors.WithLabelValues(bkapp.Name, bkapp.Namespace, deploymentName).Inc()
}

// ReportAddonClearHistoryErrors ...
func ReportAddonClearHistoryErrors(bkapp *paasv1alpha2.BkApp) {
	AddonClearHistoryErrors.WithLabelValues(bkapp.Name, bkapp.Namespace).Inc()
}

// ReportGetBkappInfoErrors ...
func ReportGetBkappInfoErrors(bkapp *paasv1alpha2.BkApp) {
	GetBkappInfoErrors.WithLabelValues(bkapp.Name, bkapp.Namespace).Inc()
}

// ReportProvisionAddonInstanceErrors ...
func ReportProvisionAddonInstanceErrors(bkapp *paasv1alpha2.BkApp) {
	ProvisionAddonInstanceErrors.WithLabelValues(bkapp.Name, bkapp.Namespace).Inc()
}

// ReportQueryAddonSpecsErrors ...
func ReportQueryAddonSpecsErrors(appCode string, moduleName string, svcID string) {
	QueryAddonSpecsErrors.WithLabelValues(appCode, moduleName, svcID).Inc()
}

// ReportQueryAddonSpecsDuration ...
func ReportQueryAddonSpecsDuration(appCode string, moduleName string, svcID string, started time.Time) {
	QueryAddonSpecsDuration.WithLabelValues(appCode, moduleName, svcID).Observe(float64(time.Since(started).Milliseconds()))
}

// ReportDeleteOutdatedServiceErrors ...
func ReportDeleteOutdatedServiceErrors(bkapp *paasv1alpha2.BkApp, svcName string) {
	DeleteOutdatedServiceErrors.WithLabelValues(bkapp.Name, bkapp.Namespace, svcName).Inc()
}

// ReportDeployExpectedServiceErrors ...
func ReportDeployExpectedServiceErrors(bkapp *paasv1alpha2.BkApp, svcName string) {
	DeployExpectedServiceErrors.WithLabelValues(bkapp.Name, bkapp.Namespace, svcName).Inc()
}

// ReportDeleteOutdatedGpaErrors ...
func ReportDeleteOutdatedGpaErrors(bkapp *paasv1alpha2.BkApp, gpaName string) {
	DeleteOutdatedGpaErrors.WithLabelValues(bkapp.Name, bkapp.Namespace, gpaName).Inc()
}

// ReportDeployExpectedGpaErrors ...
func ReportDeployExpectedGpaErrors(bkapp *paasv1alpha2.BkApp, gpaName string) {
	DeployExpectedGpaErrors.WithLabelValues(bkapp.Name, bkapp.Namespace, gpaName).Inc()
}

// ReportAutoscaleUpdateBkappStatusErrors ...
func ReportAutoscaleUpdateBkappStatusErrors(bkapp *paasv1alpha2.BkApp) {
	AutoscaleUpdateBkappStatusErrors.WithLabelValues(bkapp.Name, bkapp.Namespace).Inc()
}

// ReportAddFinalizerErrors ...
func ReportAddFinalizerErrors(bkapp *paasv1alpha2.BkApp) {
	AddFinalizerErrors.WithLabelValues(bkapp.Name, bkapp.Namespace).Inc()
}

// ReportGetBkappErrors ...
func ReportGetBkappErrors(namespace string) {
	GetBkappErrors.WithLabelValues(namespace).Inc()
}

// ReportBkappReconcileDuration ...
func ReportBkappReconcileDuration(bkapp *paasv1alpha2.BkApp, started time.Time) {
	BkappReconcileDuration.WithLabelValues(bkapp.Name, bkapp.Namespace).Observe(float64(time.Since(started).Milliseconds()))
}
