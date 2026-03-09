import uuid
from django.db import migrations, models


def assign_tokens(apps, schema_editor):
    Question = apps.get_model('polls', 'Question')
    for question in Question.objects.all():
        question.share_token = uuid.uuid4()
        question.save()


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_comment_reaction'),  # keep your existing dependency
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='share_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, null=True),
        ),
        migrations.RunPython(assign_tokens),
        migrations.AlterField(
            model_name='question',
            name='share_token',
            field=models.UUIDField(default=uuid.uuid4, editable=False, unique=True),
        ),
    ]