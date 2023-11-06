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
from typing import Optional


class BkMonitorGatewayServiceError(Exception):
    """This error indicates that there's something wrong when operating bk_monitor's
    API Gateway resource. It's a wrapper class of API SDK's original exceptions
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class BkMonitorApiError(BkMonitorGatewayServiceError):
    """When calling the bk_monitor api, bk_monitor returns an error message,
    which needs to be captured and displayed to the user on the page
    """

    def __init__(self, message: str, code: Optional[int] = None):
        super().__init__(message)
        self.code = code


class BkMonitorSpaceDoesNotExist(BkMonitorApiError):
    """The namespace applied to BK Monitoring does not exist"""


class ParamsToDictError(Exception):
    """Raised when params cannot be converted to dict"""
