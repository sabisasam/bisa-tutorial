# django-tutorial

## Tutorial part 5

Tests were introduced and found bugs got fixed.

QuestionModelTests tests the question function was_published_recently().
The function should only return True if the question was published within the last 24 hours,
so it should return False if the question was published earlier or if the pub_date is in the future.
In this way a bug in the function was found and fixed.
Before this, the function returned True if a pub_date was in the future.

QuestionIndexViewTests tests how the function get_queryset() of IndexView behaves.
The function showed questions of which the pub_date is in the future.
But it should only show questions which are already published so it was edited accordingly.

QuestionDetailViewTests checks in which cases the details of a question can be viewed.
Because it was possible to view the details of a question which isn't already published through for example guessing the right URL,
a get_queryset() function was added to DetailView and it excludes such questions through a filter.

QuestionResultsViewTests works similar to QuestionDetailViewTests but refers to vote results of a question.
The get_queryset() function of ResultsView is implemented quite the same as the function of DetailView.
