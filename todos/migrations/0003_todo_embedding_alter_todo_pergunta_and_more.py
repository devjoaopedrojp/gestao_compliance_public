# Generated by Django 5.1.2 on 2024-10-31 13:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("todos", "0002_alter_todo_pergunta_alter_todo_resposta"),
    ]

    operations = [
        migrations.AddField(
            model_name="todo",
            name="embedding",
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="todo",
            name="pergunta",
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name="todo",
            name="resposta",
            field=models.TextField(),
        ),
    ]