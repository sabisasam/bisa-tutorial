from django import template
from random import randint

from polls.models import Question

register = template.Library()


@register.filter
def get_question(value):
	"""
	Returns question with value as given ID.
	"""
	if value == None:
		num_questions = Question.objects.all().count()
		if num_questions > 0:
			random_question = Question.objects.all()[randint(0, num_questions - 1)]
			return random_question
		else:
			return None
	elif not isinstance(value, int):
		# value isn't an integer, try to convert
		try:
			value = int(value)
		except ValueError:
			return None
	# try to get question with value as ID
	try:
		question = Question.objects.get(pk=value)
	except (KeyError, Question.DoesNotExist):
		return None
	else:
		return question
