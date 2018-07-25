# Generated by Django 2.0.7 on 2018-07-24 09:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MockCondition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('key', models.CharField(default='key', max_length=32)),
                ('value', models.CharField(default='value', max_length=255)),
                ('compFunc', models.CharField(default='==', max_length=32)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='MockItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('activeType', models.BooleanField(default=True)),
                ('redirect', models.CharField(max_length=255)),
                ('finalTarget', models.CharField(max_length=255)),
                ('desc', models.CharField(blank=True, max_length=255, null=True)),
                ('url', models.CharField(max_length=255)),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.CreateModel(
            name='MockLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=255)),
                ('active_type', models.CharField(max_length=11)),
                ('method', models.CharField(default='', max_length=10)),
                ('request', models.TextField()),
                ('response', models.TextField()),
                ('time_request', models.CharField(max_length=255)),
                ('time_response', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='MockSlot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('value', models.TextField(default='{\n\t"data":\n\t{\n\n\t},\n\t"code": 0\n}')),
                ('desc', models.CharField(default='', max_length=255)),
                ('compMethod', models.BooleanField(default=True)),
                ('active', models.BooleanField(default=True)),
                ('mockItem', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='slots', to='mocker.MockItem')),
            ],
            options={
                'ordering': ('created',),
            },
        ),
        migrations.AddField(
            model_name='mockcondition',
            name='mockSlot',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='conditions', to='mocker.MockSlot'),
        ),
    ]
