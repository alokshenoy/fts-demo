# Generated by Django 4.1.1 on 2022-09-20 17:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="character",
            fields=[
                (
                    "id",
                    models.CharField(max_length=32, primary_key=True, serialize=False),
                ),
                ("name", models.CharField(max_length=64)),
                ("abbrev", models.CharField(max_length=32)),
                ("work_ids_string", models.CharField(max_length=256)),
                ("description", models.CharField(max_length=2056)),
                ("speech_count", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="work",
            fields=[
                (
                    "id",
                    models.CharField(max_length=32, primary_key=True, serialize=False),
                ),
                ("title", models.CharField(max_length=32, verbose_name="Title")),
                (
                    "long_title",
                    models.CharField(max_length=64, verbose_name="Long Title"),
                ),
                ("year", models.IntegerField(verbose_name="Year Published")),
                ("genere_type", models.CharField(max_length=1, verbose_name="Genre")),
                ("notes", models.TextField(verbose_name="Notes")),
                ("source", models.CharField(max_length=16)),
                ("total_words", models.IntegerField()),
                ("total_paragraphs", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="paragraph",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("paragraph_num", models.IntegerField()),
                ("plain_text", models.TextField()),
                ("phonetic_text", models.TextField()),
                ("stem_text", models.TextField()),
                ("paragraph_type", models.CharField(max_length=1)),
                ("section_number", models.IntegerField()),
                ("chapter_number", models.IntegerField()),
                ("char_count", models.IntegerField()),
                ("word_count", models.IntegerField()),
                (
                    "character_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.character"
                    ),
                ),
                (
                    "work_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.work"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="chapter",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                ("section_number", models.IntegerField()),
                ("chapter_number", models.IntegerField()),
                (
                    "work_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="api.work"
                    ),
                ),
            ],
            options={
                "unique_together": {("work_id", "section_number", "chapter_number")},
            },
        ),
    ]
