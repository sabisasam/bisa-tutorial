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

## Tutorial part 4

The detail template got changed.
Previously it just listed the choices but now you can vote for a choice.
After a vote, another page with voting results is displayed.
To do this, the vote and results view got modified and a vote and results template got added.
Now the vote view adds 1 to the vote counter of the selected choice.
If the vote button got clicked and no choice was selected, the sentence "You didn't select a choice." appears above the choices.
The results view and its template show the question text, its choices with their number of votes and a link to the detail page of that question to vote again.
Finally the index, detail and results view were revised to use generic views.

## Tutorial part 3

A detail, results and vote view as well as a detail template got added.
The detail view with its template shows the question text and the choices for this question.
Both other views show a simple sentence with the corresponding question ID.
The index view and its template got modified so now they list the 5 latest questions.

## Tutorial part 2

Database tables got created as well as question and choice models.
A question has question_text and pub_date as its attributes.
Its method was_published_recently tells if the question got published within the last 24 hours.
A choice is assigned to exactly one question and also has choice_text and votes as its attributes.
At least an user who can login to the admin site got created and the polls app got modifiable in the admin.

## Tutorial part 1

The project mysite was set up and the polls app got created.
The polls app got a simple index view with the message:
    "Hello, world. You're at the polls index."
