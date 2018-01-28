# bisa-tutorial



## 1) Tutorial Part 1

The project mysite was set up and the polls app got created.
The polls app got a simple index view with the message:

    "Hello, world. You're at the polls index."



## 2) Tutorial Part 2

Database tables got created as well as question and choice models.
A question has question_text and pub_date as its attributes.
Its method was_published_recently tells if the question got published within the last 24 hours.
A choice is assigned to exactly one question and also has choice_text and votes as its attributes.
At least an user who can login to the admin site got created and the polls app got modifiable in the admin.



## 3) Tutorial Part 3

A detail, results and vote view as well as a detail template got added.
The detail view with its template shows the question text and the choices for this question.
Both other views show a simple sentence with the corresponding question ID.
The index view and its template got modified so now they list the 5 latest questions.



## 4) Tutorial Part 4

The detail template got changed.
Previously it just listed the choices but now you can vote for a choice.
After a vote, another page with voting results is displayed.
To do this, the vote and results view got modified and a vote and results template got added.
Now the vote view adds 1 to the vote counter of the selected choice.
If the vote button got clicked and no choice was selected, the sentence "You didn't select a choice." appears above the choices.
The results view and its template show the question text, its choices with their number of votes and a link to the detail page of that question to vote again.
Finally the index, detail and results view were revised to use generic views.



## 5) Tutorial Part 5

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



## 6) Tutorial Part 6

At the index page, the color of question links was set to green and a background image was added.



## 7) Tutorial Part 7

The admin form was edited.

The edit form for questions got restructured and the possibility to set choices was added.
The admin change list now shows more information about the questions.
Also a filter sidebar to filter by date published and a search box to search for questions were added.
Finally, the admin site name got changed to "Polls Administration".



## 8) Tutorial Part 8

Random1 view and random view as well as random template were added.
Both views return a random published question to display but they work different.
Random1 view uses the random order function of queryset while random view uses a random number to get a random question.

Tests for random1 and random view were implemented also.
QuestionRandom1ViewTests tests the behavior of random1 view and QuestionRandomViewTests does the same for random view.
They check if an appropriate message is displayed if no questions or only unpublished questions exist.
They also test if the result is not NULL but a question object in case at least one published question exists.

Mockups in JPG and PDF format were added.

A .gitignore file were created and modified.
It tells which files should be ignored by Git.



## 9) Signal Handling

A model named QuestionHistory with question and creation_time as its attributes got added.

If a question is added to the database, an instance of QuestionHistory gets created.
The attribute creation_time will be set to the datetime at that moment and question is simply the question it relates to.
The question attribute will be set to null if the question object gets deleted.



## 10) Custom Permissions

Custom permissions got added.

In class Question, the permissions to view published questions and to view unpublished questions were introduced.
In class Choice, the permission to vote for a choice were added.
And in class QuestionHistory, it's the permission to view the question history.



## 11) Signals and Permissions for All Classes at the Same Time

Changed custom permissions.
Added function add_permissions which automatically adds view and list permissions for every content type after migration if they don't exist already.



## 12) Django Packages

Added django-extensions to installed apps.

Changed Question model to be a TimeStampedModel and adjusted save_question_creation_time function in the QuestionHistory model so now it uses the created attribute of Question model.



## 13) Question Display

A detailed question display with four buttons got added.
Use the left and right button to navigate through the questions.
The top button redirects to a page from where you can choose which question to display.
The bottom button changes the question status to archived.

Archived questions won't be shown in this question display.



## 14) Channels

The file mysite/settings.py got changed for use of channels.
The models Room and Message got added to polls/models.py.
They are used in polls/consumers.py which contains four functions or consumers.
The function msg_consumer in polls/consumers.py sends incoming messages to listening sockets.
The consumer ws_connect accepts connection requests.
The function ws_message deals with messages and ws_disconnect discards a connection.
Channel routing is contained in polls/routing.py and it maps channels to consumer functions.

To activate "redis" install docker and avoid this way multiple local installations. After the installation
run your redis or rabbitmq instances like this

     $ docker run -p 6379:6379 redis

## 15) Management Page

The code which belongs to the Channels part got separated from the polls app and put into an extra chat app.

Two versions of management page got added, one working with Signals and one with Data Binding.
Each of them lists all questions which are added within the last 24 hours.
The lists get automatically updated if a question gets created, updated or deleted.



## 16) Template Tag

The templatetags directory got created in the polls app through running the following command:

    $ python manage.py create_template_tags polls

In polls/templatetags/polls_tags.py a template tag named get_question got implemented.
It gets a value and tries to return a question which has this value as its ID.
It will return None if it fails or a random question if value is None.



## 17) REST Framework

### 17.1) Requests and Beautiful Soup

The instructions of the [Short Intro to Scraping](https://gist.github.com/bradmontgomery/1872970) were followed.
A few things were done differently because the given link in the intro doesn't work anymore.

The tools get installed through:

    $ pip install beautifulsoup4
    $ pip install requests

The Python shell is used for all the following inputs.
The page http://www.oreilly.com/free/reports.html is used for the get request.

```pycon
>>> import requests
>>> result = requests.get("http://www.oreilly.com/free/reports.html")
```

The result gets checked through:

```pycon
>>> result.status_code
200
>>> result.headers
{'Server': 'Apache', 'Last-Modified': ...
```

The content gets stored in a variable:

```pycon
>>> c = result.content
```

It gets parsed with Beautiful Soup through the following
(replace `bs4` with `BeautifulSoup` if the source were downloaded and not installed with pip):

```pycon
>>> from bs4 import BeautifulSoup
>>> soup = BeautifulSoup(c)
>>> samples = soup.find_all("a", { "data-container": "body" })
>>> samples[0]
<a data-container="body" data-content= ...
```

The book titles (as keys) and the corresponding links (as values) get saved in `data`:

```pycon
>>> data = {}
>>> for a in samples:
...     title = a.attrs['title']
...     data[title] = a.attrs['href']
... 
>>> for key, value in data.items():
...     print(key + '\n' + value + '\n')
... 
The New Manager Mindset
http:// ...
```

### 17.2) JSON Server

The steps and code lines are taken from [here](https://github.com/typicode/json-server) and [here](http://www.betterpixels.co.uk/projects/2015/05/09/mock-up-your-rest-api-with-json-server/).

A file named data.json got created which specifies endpoints that should be provided.
The endpoints are /questions and /choices.
A sample question and related choices were added to have some data.
A configuration file named json-server.json got created for the possibility of saving option settings.

To start the JSON server, open command prompt (or something similar) and run the following:

    $ json-server data.json

Open a browser (like Chrome or Firefox), go to http://localhost:3000/ and open the browser's developer tools to use the console.
The data.json file can be modified through pasting the following snippets into console:

Add a question with `question_text`, `pub_date`, `archived` and `id` as its attributes
(`id` is given automatically and will be 2 because in this case a question with id=1 already exists):

```javascript
fetch('http://localhost:3000/questions/', {
    method: 'post',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        "question_text": "What is the meaning of life?",
        "pub_date": "2017-10-21T13:08:09.381Z",
        "archived": false
    })
})
```

Edit question with id=2:

```javascript
fetch('http://localhost:3000/questions/2', {
    method: 'put',
    headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    },
    body: JSON.stringify({
        "question_text": "What is the meaning of life?",
        "pub_date": "2017-10-21T13:08:09.381Z",
        "archived": true
    })
})
```

Delete question with id=2:

```javascript
fetch('http://localhost:3000/questions/2', {
    method: 'delete',
})
```



## 18) Django Messages

Django messages were already used in the base.html template of the polls app but not each template extended the file or dealt with those messages itself.
So those templates got changed to handle messages in one of those ways.



## 19) Fortune

The Fortune Pages show a random quote, saying or something similar.
The normal version of the page loads as long as fortune packs get loaded
while the websocket version loads the packs in the background and updates the page afterwards.
If you run the script rabbitmq_send.py it will send a message (optional with a category) through RabbitMQ to a consumer.
Then, this consumer will send a fortune (of given category) to the websocket of the RabbitMQ version of the Fortune Page.
This websocket will then replace the text on that page with the sent fortune.

The rabbitmq folder contains the results of doing the RabbitMQ tutorial for Python.



## 20) Webhooks

The webhook got created through doing the steps described on [this page](https://simpleisbetterthancomplex.com/tutorial/2016/10/31/how-to-handle-github-webhooks-using-django.html).
If the right secret token is used, the webhook reacts to GitHub's POST requests by e.g. sending "pong".
