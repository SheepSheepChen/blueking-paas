# -*- coding: utf-8 -*-
"""
TencentBlueKing is pleased to support the open source community by making
蓝鲸智云 - PaaS 平台 (BlueKing - PaaS System) available.
Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
Licensed under the MIT License (the "License"); you may not use this file except
in compliance with the License. You may obtain a copy of the License at

    http://opensource.org/licenses/MIT

Unless required by applicable law or agreed to in writing, software distributed under
the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
either express or implied. See the License for the specific language governing permissions and
limitations under the License.

We undertake not to change the open source license (MIT license) applicable
to the current version of the project delivered to anyone in the future.
"""
import os
from typing import List, Optional

import cattr

from paas_wl.resources.base.kube_client import CoreDynamicClient
from paas_wl.workloads.processes.models import ProcessProbe
from paasng.extensions.declarative.deployment.resources import Probe
from paasng.platform.applications.models import ModuleEnvironment


def get_command_name(command: str) -> str:
    """Get name from command"""
    # fit for old paas app celery start by django-celery: python manage.py celery beat/worker....
    if command.startswith("python manage.py celery"):
        return "celery"

    process_exec = command.split(' ')[0]
    return os.path.basename(process_exec)


def find_deployment_condition(conditions: List, cond_type: str):
    """finds the conditionType in conditions."""
    for cond in conditions:
        if cond.type == cond_type:
            return cond
    return None


def list_unavailable_deployment(client: CoreDynamicClient) -> List:
    """查询整个命名空间下的deployments，并通过replica，获取不处于 Available 的 deployments"""
    unavailable_deployments = []
    kind_deployment = client.get_preferred_resource(kind="Deployment")
    deployment_list = client.get(kind_deployment)

    for deployment in deployment_list.items:
        # 判断 Deployment 是否由蓝鲸应用的工作负载
        if not deployment.metadata.namespace.startswith('bkapp'):
            continue

        # 只有当前就绪的副本数等于需要的副本数时, Deployment 才完成滚动更新
        if deployment.status.get("updatedReplicas", None) == deployment.status.get("replicas", None):
            available_cond = find_deployment_condition(deployment.status.get("conditions") or [], "Available")
            if available_cond and available_cond.status == "True":
                continue
        # 其他情况的 Deployment 均认为 unavailable
        unavailable_deployments.append(deployment)
    return unavailable_deployments


def upsert_process_probe(
    env: ModuleEnvironment,
    process_type: str,
    probe_type: str,
    probe: Probe,
):
    """更新或创建应用探针的配置"""
    instance, _ = ProcessProbe.objects.update_or_create(
        defaults={
            "check_mechanism": cattr.unstructure(probe.get_probe_handler()),
            "initial_delay_seconds": probe.initial_delay_seconds,
            "timeout_seconds": probe.timeout_seconds,
            "period_seconds": probe.period_seconds,
            "success_threshold": probe.success_threshold,
            "failure_threshold": probe.failure_threshold,
        },
        app=env.wl_app,
        process_type=process_type,
        probe_type=probe_type,
    )


def delete_process_probe(
    env: ModuleEnvironment,
    process_type: str,
    probe_type: Optional[str] = None,
):
    """删除应用探针的配置"""
    if probe_type:
        ProcessProbe.objects.filter(app=env.wl_app, process_type=process_type, probe_type=probe_type).delete()
    else:
        ProcessProbe.objects.filter(app=env.wl_app, process_type=process_type).delete()
