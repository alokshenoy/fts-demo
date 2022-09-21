# Generated by Django 4.1.1 on 2022-09-21 14:29

import django.contrib.postgres.search
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0006_creating_trigger"),
    ]

    operations = [
        migrations.CreateModel(
            name="product",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("product_name", models.CharField(max_length=500)),
                ("category_tree", models.CharField(max_length=1000)),
                ("brand", models.CharField(max_length=500)),
                ("product_description", models.TextField()),
                ("product_specifications", models.CharField(max_length=1)),
                (
                    "fts_vector_name",
                    django.contrib.postgres.search.SearchVectorField(null=True),
                ),
                (
                    "fts_vector_pd",
                    django.contrib.postgres.search.SearchVectorField(null=True),
                ),
                (
                    "fts_vector_all",
                    django.contrib.postgres.search.SearchVectorField(null=True),
                ),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="chapter",
            unique_together=None,
        ),
        migrations.RemoveField(
            model_name="chapter",
            name="work_id_fk",
        ),
        migrations.DeleteModel(
            name="character",
        ),
        migrations.DeleteModel(
            name="paragraph",
        ),
        migrations.DeleteModel(
            name="chapter",
        ),
        migrations.DeleteModel(
            name="work",
        ),
    ]
