# django-tutorial

## Channels

- mysite/settings.py got changed for use of channels.
- The models Room and Message got added to polls/models.py.
- They are used in polls/consumers.py which contains four functions or consumers.
- The function msg_consumer in polls/consumers.py sends incoming messages to listening sockets.
- The consumer ws_connect accepts connection requests. 
* ws_message deals with messages and 
* ws_disconnect discards a connection.
- Channel routing is contained in polls/routing.py and it maps channels to consumer functions.

A detailed question display with four buttons got added.
Use the left and right button to navigate through the questions.
The top button redirects to a page from where you can choose which question to display.
The bottom button changes the question status to archived.

Archived questions won't be shown in this question display.

## Django Packages

Added django-extensions to installed apps.

Changed Question model to be a TimeStampedModel and adjusted save_question_creation_time function in the QuestionHistory model so now it uses the created attribute of Question model.

## Signals and permissions for all classes at the same time

Changed custom permissions.
Added function add_permissions which automatically adds view and list permissions for every content type after migration if they don't exist already.

## Custom Permissions

Custom permissions got added.

In class Question, the permissions to view published questions and to view unpublished questions were introduced.

In class Choice, the permission to vote for a choice were added.

And in class QuestionHistory, it's the permission to view the question history.

## Signal Handling

A model named QuestionHistory with question and creation_time as its attributes got added.

If a question is added to the database, an instance of QuestionHistory gets created.

The attribute creation_time will be set to the datetime at that moment and question is simply the question it relates to.
The question attribute will be set to null if the question object gets deleted.

## Tutorial part 8

Random1 view and random view as well as random template were added.

Both views return a random published question to display but they work different.
Random1 view uses the random order function of queryset while random view uses a random number to get a random question.

Tests for random1 and random view were implemented also.

QuestionRandom1ViewTests tests the behavior of random1 view and QuestionRandomViewTests does the same for random view.
They check if an appropriate message is displayed if no questions or only unpublished questions exist.
They also test if the result is not NULL but a question object in case at least one published question exists.

Mockups in JPG and PDF format were added.

## Feature/Tutorial8

A .gitignore file were created and modified. It tells which files should be ignored by Git.

## Tutorial part 7

The admin form was edited.  

The edit form for questions got restructured and the possibility to set choices was added.

The admin change list now shows more information about the questions.

Also a filter sidebar to filter by date published and a search box to search for questions were added.
Finally, the admin site name got changed to "Polls Administration".

## Tutorial part 6

At the index page, the color of question links was set to green and a background image was added.

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

After a vote, another page with voting results is displayed.To do this, the vote and results view got modified and a vote and results template got added.
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
