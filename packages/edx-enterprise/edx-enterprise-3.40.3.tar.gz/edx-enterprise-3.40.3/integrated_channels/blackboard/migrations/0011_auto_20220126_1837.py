# Generated by Django 3.2.11 on 2022-01-26 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blackboard', '0010_auto_20211221_1532'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blackboardenterprisecustomerconfiguration',
            name='blackboard_base_url',
            field=models.CharField(blank=True, default='', help_text='The base URL used for API requests to Blackboard, i.e. https://blackboard.com.', max_length=255, verbose_name='Base URL'),
        ),
        migrations.AlterField(
            model_name='blackboardenterprisecustomerconfiguration',
            name='catalogs_to_transmit',
            field=models.TextField(blank=True, default='', help_text='A comma-separated list of catalog UUIDs to transmit. If blank, all customer catalogs will be transmitted. If there are overlapping courses in the customer catalogs, the overlapping course metadata will be selected from the newest catalog.'),
        ),
        migrations.AlterField(
            model_name='blackboardenterprisecustomerconfiguration',
            name='channel_worker_username',
            field=models.CharField(blank=True, default='', help_text='Enterprise channel worker username to get JWT tokens for authenticating LMS APIs.', max_length=255),
        ),
        migrations.AlterField(
            model_name='blackboardenterprisecustomerconfiguration',
            name='client_id',
            field=models.CharField(blank=True, default='', help_text='The API Client ID provided to edX by the enterprise customer to be used to make API calls on behalf of the customer. Called Application Key in Blackboard', max_length=255, verbose_name='API Client ID or Blackboard Application Key'),
        ),
        migrations.AlterField(
            model_name='blackboardenterprisecustomerconfiguration',
            name='client_secret',
            field=models.CharField(blank=True, default='', help_text='The API Client Secret provided to edX by the enterprise customer to be used to make  API calls on behalf of the customer. Called Application Secret in Blackboard', max_length=255, verbose_name='API Client Secret or Application Secret'),
        ),
        migrations.AlterField(
            model_name='blackboardenterprisecustomerconfiguration',
            name='idp_id',
            field=models.CharField(blank=True, default='', help_text='If provided, will be used as IDP slug to locate remote id for learners', max_length=255),
        ),
        migrations.AlterField(
            model_name='historicalblackboardenterprisecustomerconfiguration',
            name='blackboard_base_url',
            field=models.CharField(blank=True, default='', help_text='The base URL used for API requests to Blackboard, i.e. https://blackboard.com.', max_length=255, verbose_name='Base URL'),
        ),
        migrations.AlterField(
            model_name='historicalblackboardenterprisecustomerconfiguration',
            name='catalogs_to_transmit',
            field=models.TextField(blank=True, default='', help_text='A comma-separated list of catalog UUIDs to transmit. If blank, all customer catalogs will be transmitted. If there are overlapping courses in the customer catalogs, the overlapping course metadata will be selected from the newest catalog.'),
        ),
        migrations.AlterField(
            model_name='historicalblackboardenterprisecustomerconfiguration',
            name='channel_worker_username',
            field=models.CharField(blank=True, default='', help_text='Enterprise channel worker username to get JWT tokens for authenticating LMS APIs.', max_length=255),
        ),
        migrations.AlterField(
            model_name='historicalblackboardenterprisecustomerconfiguration',
            name='client_id',
            field=models.CharField(blank=True, default='', help_text='The API Client ID provided to edX by the enterprise customer to be used to make API calls on behalf of the customer. Called Application Key in Blackboard', max_length=255, verbose_name='API Client ID or Blackboard Application Key'),
        ),
        migrations.AlterField(
            model_name='historicalblackboardenterprisecustomerconfiguration',
            name='client_secret',
            field=models.CharField(blank=True, default='', help_text='The API Client Secret provided to edX by the enterprise customer to be used to make  API calls on behalf of the customer. Called Application Secret in Blackboard', max_length=255, verbose_name='API Client Secret or Application Secret'),
        ),
        migrations.AlterField(
            model_name='historicalblackboardenterprisecustomerconfiguration',
            name='idp_id',
            field=models.CharField(blank=True, default='', help_text='If provided, will be used as IDP slug to locate remote id for learners', max_length=255),
        ),
    ]
