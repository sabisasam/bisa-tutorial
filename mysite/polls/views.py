from django.contrib import messages
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
		random_question = Question.objects.filter(pub_date__lte=timezone.now()).order_by('?').first()
		return random_question


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
			random_question = published_questions[randint(0, number_of_objects - 1)]
			return random_question


def questions(request):
	question_list = Question.objects.filter(archived=False).order_by('pub_date')
	# show 1 question per page
	paginator = Paginator(question_list, 1)

	page = request.GET.get('page')
	try:
		question = paginator.page(page)
	except PageNotAnInteger:
		# if page is not an integer, deliver first page
		question = paginator.page(1)
		page = 1
	except EmptyPage:
		# if page is out of range, deliver last page of results
		question = paginator.page(paginator.num_pages)
		page = paginator.num_pages

	return render(request, 'polls/questions.html', {
		'question': question,
		'page': page,
	})


def questionsIndex(request):
	question_list = Question.objects.filter(archived=False).order_by('pub_date')
	num_questions = question_list.count()

	return render(request, 'polls/questions.index.html', {
		'num_questions': num_questions,
	})


def questionsArchive(request, page_num):
	question_list = Question.objects.filter(archived=False).order_by('pub_date')
	num_questions = question_list.count()
	try:
		question = question_list[int(page_num) - 1]
	except IndexError:
                messages.error(request, 'An error has occurred. The question could not be archived.')
                return HttpResponseRedirect(reverse('polls:questions-index'))
	else:
		question_text = question.question_text
		question.archived = True
		question.save()
		num_questions -= 1
		messages.success(request, 'The question "' + question_text + '" is now archived.')
		return HttpResponseRedirect(reverse('polls:questions-index'))
