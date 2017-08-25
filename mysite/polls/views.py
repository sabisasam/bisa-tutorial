from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from random import randint

from .models import Choice, Question


class IndexView(generic.ListView):
	template_name = 'polls/index.html'
	context_object_name = 'latest_question_list'

	def get_queryset(self):
		"""
		Return the last five published questions
		(not including those set to be published in the future).
		"""
		return Question.objects.filter(
			pub_date__lte=timezone.now()
		).order_by('-pub_date')[:5]


class DetailView(generic.DetailView):
	model = Question
	template_name = 'polls/detail.html'

	def get_queryset(self):
		"""
		Excludes any questions that aren't published yet.
		"""
		return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
	model = Question
	template_name = 'polls/results.html'

	def get_queryset(self):
		"""
		Excludes any questions that aren't published yet.
		"""
		return Question.objects.filter(pub_date__lte=timezone.now())


def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	try:
		selected_choice = question.choice_set.get(pk=request.POST['choice'])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay the question voting form.
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': "You didn't select a choice.",
		})
	else:
		selected_choice.votes += 1
		selected_choice.save()
		# Returning HttpResponseRedirect after successfully dealing
		# with POST data prevents data from being postet twice if a
		# user hits the Back button.
		return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class Random1View(generic.ListView):
	template_name = 'polls/random.html'
	context_object_name = 'random_question'

	def get_queryset(self):
		"""
		Returns a random question, selected through using
		queryset (random order).
		"""
		return Question.objects.filter(pub_date__lte=timezone.now()).order_by('?').first()


class RandomView(generic.ListView):
	template_name = 'polls/random.html'
	context_object_name = 'random_question'

	def get_queryset(self):
		"""
		Returns a random question, selected through using
		a random number.
		"""
		published_questions = Question.objects.filter(pub_date__lte=timezone.now())
		number_of_objects = published_questions.count()
		if number_of_objects > 0:
			return published_questions[randint(0, number_of_objects - 1)]


def questions(request):
	all_questions = Question.objects.all()
	# show 1 question per page
	paginator = Paginator(all_questions, 1)

	page = request.GET.get('page')
	try:
		question = paginator.page(page)
	except PageNotAnInteger:
		# if page is not an integer, deliver first page
		question = paginator.page(1)
	except EmptyPage:
		# if page is out of range, deliver last page of results
		question = paginator.page(paginator.num_pages)

	return render(request, 'questions.html', {'question': question})
