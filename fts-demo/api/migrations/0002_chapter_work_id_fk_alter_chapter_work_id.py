# Generated by Django 4.1.1 on 2022-09-20 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="chapter",
            name="work_id_fk",
            field=models.ForeignKey(
                default=0, on_delete=django.db.models.deletion.CASCADE, to="api.work"
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="chapter",
            name="work_id",
            field=models.CharField(max_length=32),
        ),
    ]
