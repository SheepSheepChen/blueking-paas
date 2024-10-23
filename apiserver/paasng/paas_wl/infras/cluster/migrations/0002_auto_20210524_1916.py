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

# Generated by Django 2.2.17 on 2021-05-24 11:16

import paas_wl.infras.cluster.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cluster',
            name='token_type',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='cluster',
            name='token_value',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='ingress_config',
            field=paas_wl.infras.cluster.models.IngressConfigField(),
        ),
    ]