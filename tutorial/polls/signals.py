from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission
from django.db.models.signals import post_migrate, post_save, post_delete
from django.dispatch import receiver

from .models import Question, QuestionHistory

import json
from channels import Group


@receiver(post_migrate)
def add_permissions(sender, **kwargs):
    """
    Add view and list permissions to all content types.
    """
    for content_type in ContentType.objects.all():
        for action in ['view', 'list']:
            codename = "%s_%s" % (action, content_type.model)
            try:
                Permission.objects.get(
                    content_type=content_type, codename=codename)
            except Permission.DoesNotExist:
                Permission.objects.create(
                    content_type=content_type,
                    codename=codename,
                    name="Can %s %s" % (action, content_type.name),
                )
                print(
                    "Added %s permission for %s" %
                    (action, content_type.name))


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


@receiver(post_save, sender=Question)
@receiver(post_delete, sender=Question)
def update_management_page(sender, **kwargs):
    """
    If a new question gets created, the function sends a message, which contains id and
    text of the question, to the management group.
    """
    Group("management-signals").send({
        'text': json.dumps({})
    })
