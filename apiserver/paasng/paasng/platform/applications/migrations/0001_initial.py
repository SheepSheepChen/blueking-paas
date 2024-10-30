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

# Generated by Django 2.2.17 on 2020-11-27 02:50

from django.db import migrations, models
import django.db.models.deletion
import paasng.utils.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', paasng.utils.models.BkUserField(blank=True, db_index=True, max_length=64, null=True)),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='应用代号')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='应用名称')),
                ('language', models.CharField(max_length=32, verbose_name='编程语言')),
                ('source_init_template', models.CharField(max_length=32, verbose_name='初始化模板类型')),
                ('source_type', models.CharField(max_length=16, null=True, verbose_name='源码托管类型')),
                ('source_repo_id', models.IntegerField(null=True, verbose_name='源码 ID')),
                ('app_type', models.CharField(default='web', max_length=32, verbose_name='应用类型')),
                ('is_active', models.BooleanField(default=True, verbose_name='是否活跃')),
                ('last_deployed_date', models.DateTimeField(null=True, verbose_name='最近部署时间')),
                ('creator', paasng.utils.models.BkUserField(blank=True, db_index=True, max_length=64, null=True)),
                ('is_deleted', models.BooleanField(default=False, verbose_name='是否删除')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserMarkedApplication',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('owner', paasng.utils.models.BkUserField(blank=True, db_index=True, max_length=64, null=True)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applications.Application')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationMembership',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('user', paasng.utils.models.BkUserField(blank=True, db_index=True, max_length=64, null=True)),
                ('role', models.IntegerField(default=3)),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='applications.Application')),
            ],
        ),
        migrations.CreateModel(
            name='ApplicationFeatureFlag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('effect', models.BooleanField(default=True, verbose_name='是否允许(value)')),
                ('name', models.CharField(max_length=30, verbose_name='特性名称(key)')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feature_flag', to='applications.Application')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ApplicationEnvironment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(help_text='部署区域', max_length=32)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('environment', models.CharField(max_length=16, verbose_name='部署环境')),
                ('is_offlined', models.BooleanField(default=False, help_text='是否已经下线，仅成功下线后变为False')),
                ('application', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='envs', to='applications.Application')),
            ],
        ),
    ]