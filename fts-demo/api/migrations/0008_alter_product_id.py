# Generated by Django 4.1.1 on 2022-09-21 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0007_product_alter_chapter_unique_together_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="id",
            field=models.CharField(max_length=500, primary_key=True, serialize=False),
        ),
    ]
