from django import template

from polls.models import Question

register = template.Library()


@register.filter
def get_question(value):
	"""
	Returns question with value as given ID.
	"""
	if not isinstance(value, int):
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
