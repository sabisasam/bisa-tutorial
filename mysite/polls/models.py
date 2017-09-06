import datetime

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# imports for function add_permissions
from django.db.models.signals import post_migrate
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.models import Permission


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __str__(self):
        return self.question_text
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.choice_text

    class Meta:
        permissions = (
            ("vote_choice", "Can vote for a choice"),
        )


class QuestionHistory(models.Model):
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, blank=True, null=True)
    creation_time = models.DateTimeField('date created')

    def __str__(self):
        time = self.creation_time.strftime('%b. %d, %Y, %X')
        return time

    @receiver(post_save, sender=Question)
    def save_question_creation_time(sender, instance, created, **kwargs):
        if created:
            obj, obj_created = QuestionHistory.objects.get_or_create(
                question=instance,
                defaults={'creation_time': timezone.now()},
            )


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
