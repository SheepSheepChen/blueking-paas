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

"""Collect application resource usage report

Examples:

    # 仅评估指定的应用（支持列表）
    python manage.py collect_app_res_usage_report --codes app-code-1 app-code-2

    # 评估全量应用（性能不会很好）
    python manage.py collect_app_res_usage_report --all
"""
from django.core.management.base import BaseCommand

from paasng.misc.monitoring.metrics.tasks import collect_and_update_app_res_usage_reports


class Command(BaseCommand):
    help = "Collect and statistics application history metrics"

    def add_arguments(self, parser):
        parser.add_argument("--codes", dest="app_codes", default=[], nargs="*", help="应用 Code 列表")
        parser.add_argument("--all", dest="collect_all", default=False, action="store_true", help="采集全量应用")

    def handle(self, app_codes, collect_all, *args, **options):
        if not (collect_all or app_codes):
            raise ValueError("please specify --codes or --all")

        collect_and_update_app_res_usage_reports(app_codes)
