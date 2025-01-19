# Generated by Django 5.1.2 on 2024-10-23 16:25

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_alter_membership_options_alter_organization_options_and_more'),
        ('words_soup_game', '0003_alter_exercise_correct_word_alter_exercise_words'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='exercise',
            name='created_by',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='exercise',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='organization.organization'),
            preserve_default=False,
        ),
    ]
