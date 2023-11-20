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
import random

from django.utils.crypto import get_random_string


def random_resource_name():
    """A random name used as kubernetes resource name to avoid conflict
    can also be used for application name
    """
    return 'bkapp-' + get_random_string(length=12).lower() + "-" + random.choice(["stag", "prod"])


def make_container_status(state: dict, last_state: dict):
    """Make a container status dict that fits in Pod.status.containerStatuses."""
    return {
        "image": "",
        "imageID": "",
        "name": "",
        "ready": True,
        "restartCount": 0,
        "state": state,
        "lastState": last_state,
    }
