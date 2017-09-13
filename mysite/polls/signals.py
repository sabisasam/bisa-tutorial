
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver

from .models import Question, QuestionHistory


@receiver(post_migrate)
def add_permissions(sender, **kwargs):
    """
    Add view and list permissions to all content types.
    """
    for content_type in ContentType.objects.all():
        for action in ['view', 'list']:
            codename = "%s_%s" % (action, content_type.model)
            try:
                Permission.objects.get(content_type=content_type, codename=codename)
            except Permission.DoesNotExist:
                Permission.objects.create(
                    content_type=content_type,
                    codename=codename,
                    name="Can %s %s" % (action, content_type.name),
                )
                print("Added %s permission for %s" % (action, content_type.name))


@receiver(post_save, sender=Question)
def save_question_creation_time(sender, instance, created, **kwargs):
    """
    Automatically creates an object of QuestionHistory if a new question gets created.
    """
    if created:
        obj, obj_created = QuestionHistory.objects.get_or_create(
            question=instance,
            defaults={'creation_time': instance.created},
        )
