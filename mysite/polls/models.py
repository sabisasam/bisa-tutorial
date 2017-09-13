import datetime

from django.db import models
from django.utils import timezone
from django_extensions.db.models import TimeStampedModel


class Question(TimeStampedModel):
    """
    A question object has a question_text attribute, which contains the question text,
    a pub_date attribute, telling you when the question was or will be published,
    an archived attribute, which is True if the question is archived, and a created
    attribute, containing the creation time of the question.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    archived = models.BooleanField(default=False)
    
    def __str__(self):
        """
        Defines representation of a question object.
        """
        return self.question_text
    
    def was_published_recently(self):
        """
        Tells if a question was published within the last 24 hours.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """
    A choice object belongs to a question object. It has the attributes choice_text,
    containing text of the choice, and votes, which tells how often the choice was voted.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    def __str__(self):
        """
        Defines representation of a choice object.
        """
        return self.choice_text

    class Meta:
        """
        Defines specific permissions for Choice model.
        """
        permissions = (
            ("vote_choice", "Can vote for a choice"),
        )


class QuestionHistory(models.Model):
    """
    An object of the QuestionHistory model is automatically created when a question object
    gets created. The question attribute points to the correlating question as long as it
    exists and will be NULL if the question gets deleted. The creation_time contains the
    creation time of the question.
    """
    question = models.ForeignKey(Question, on_delete=models.SET_NULL, blank=True, null=True)
    creation_time = models.DateTimeField('date created')

    def __str__(self):
        """
        Defines representation of a questionHistory object.
        """
        time = self.creation_time.strftime('%b. %d, %Y, %X')
        return time
