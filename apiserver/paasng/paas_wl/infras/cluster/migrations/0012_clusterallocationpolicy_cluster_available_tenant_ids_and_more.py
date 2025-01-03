# Generated by Django 4.2.17 on 2024-12-23 11:51

import blue_krill.models.fields
from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields
import paas_wl.infras.cluster.constants
import paas_wl.infras.cluster.models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('cluster', '0011_cluster_exposed_url_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClusterAllocationPolicy',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('tenant_id', models.CharField(help_text='所属租户', max_length=128, unique=True)),
                ('type', models.CharField(help_text='分配策略类型', max_length=32)),
                ('manual_allocation_config', paas_wl.infras.cluster.models.ManualAllocationConfigField(default=None, help_text='手动分配配置')),
                ('allocation_rules', paas_wl.infras.cluster.models.AllocationRulesField(default=list, help_text='集群分配规则列表')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='cluster',
            name='available_tenant_ids',
            field=models.JSONField(default=list, help_text='可用的租户 ID 列表'),
        ),
        migrations.AddField(
            model_name='cluster',
            name='component_image_registry',
            field=models.CharField(default='hub.bktencent.com', help_text='集群组件镜像仓库地址', max_length=255),
        ),
        migrations.AddField(
            model_name='cluster',
            name='component_preferred_namespace',
            field=models.CharField(default='blueking', help_text='集群组件优先部署的命名空间', max_length=64),
        ),
        migrations.AddField(
            model_name='cluster',
            name='container_log_dir',
            field=models.CharField(default='/var/lib/docker/containers', help_text='容器日志目录', max_length=255),
        ),
        migrations.AddField(
            model_name='cluster',
            name='tenant_id',
            field=models.CharField(default='default', help_text='所属租户', max_length=128),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='annotations',
            field=jsonfield.fields.JSONField(default=dict, help_text='集群元数据，如 BCS 项目，集群，业务信息等'),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='ca_data',
            field=blue_krill.models.fields.EncryptField(help_text='证书认证机构（CA）', null=True),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='cert_data',
            field=blue_krill.models.fields.EncryptField(help_text='客户端证书', null=True),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='default_node_selector',
            field=jsonfield.fields.JSONField(default=dict, help_text='部署到本集群的应用默认节点选择器（node_selector）'),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='default_tolerations',
            field=jsonfield.fields.JSONField(default=list, help_text='部署到本集群的应用默认容忍度（tolerations）'),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='description',
            field=models.TextField(blank=True, help_text='集群描述'),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='feature_flags',
            field=jsonfield.fields.JSONField(default=dict, help_text='集群特性集'),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='ingress_config',
            field=paas_wl.infras.cluster.models.IngressConfigField(help_text='ingress 配置'),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='is_default',
            field=models.BooleanField(default=False, help_text='是否为默认集群（deprecated，后续由分配策略替代）', null=True),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='key_data',
            field=blue_krill.models.fields.EncryptField(help_text='客户端密钥', null=True),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='name',
            field=models.CharField(help_text='集群名称', max_length=32, unique=True),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='region',
            field=models.CharField(db_index=True, help_text='可用区域', max_length=32),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='token_type',
            field=models.IntegerField(default=paas_wl.infras.cluster.constants.ClusterTokenType['SERVICE_ACCOUNT'], help_text='Token 类型'),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='token_value',
            field=blue_krill.models.fields.EncryptField(help_text='Token 值', null=True),
        ),
        migrations.AlterField(
            model_name='cluster',
            name='type',
            field=models.CharField(default=paas_wl.infras.cluster.constants.ClusterType['NORMAL'], help_text='集群类型', max_length=32),
        ),
        migrations.CreateModel(
            name='ClusterElasticSearchConfig',
            fields=[
                ('uuid', models.UUIDField(auto_created=True, default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='UUID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('scheme', models.CharField(help_text='ES 集群协议', max_length=12)),
                ('host', models.CharField(help_text='ES 集群地址', max_length=128)),
                ('port', models.IntegerField(help_text='ES 集群端口')),
                ('username', models.CharField(help_text='ES 集群用户名', max_length=64)),
                ('password', blue_krill.models.fields.EncryptField(help_text='ES 集群密码')),
                ('cluster', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='elastic_search_config', to='cluster.cluster')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
