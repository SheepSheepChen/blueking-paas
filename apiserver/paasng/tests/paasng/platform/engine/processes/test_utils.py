# -*- coding: utf-8 -*-
# TencentBlueKing is pleased to support the open source community by making
# 蓝鲸智云 - PaaS 平台 (BlueKing - PaaS System) available.
# Copyright (C) 2017 THL A29 Limited, a Tencent company. All rights reserved.
# Licensed under the MIT License (the "License"); you may not use this file except
# in compliance with the License. You may obtain a copy of the License at
#
#     http://opensource.org/licenses/MIT
#
# Unless required by applicable law or agreed to in writing, software distributed under
# the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,
# either express or implied. See the License for the specific language governing permissions and
# limitations under the License.
#
# We undertake not to change the open source license (MIT license) applicable
# to the current version of the project delivered to anyone in the future.

import pytest

from paas_wl.bk_app.processes.processes import PlainInstance, PlainProcess
from paasng.platform.engine.processes.utils import ProcessesSnapshotStore

pytestmark = pytest.mark.django_db(databases=["default", "workloads"])


@pytest.fixture()
def process():
    """A Process object"""
    inst = PlainInstance(name="instance-foo", version=1, process_type="web", ready=False)
    return PlainProcess(
        name="web",
        version=1,
        replicas=1,
        type="web",
        command="foo",
        instances=[inst],
    )


class TestProcessesSnapshotStore:
    def test_save_then_get(self, bk_stag_env, process):
        store = ProcessesSnapshotStore(bk_stag_env)
        store.save([process])
        assert store.get() == [process]