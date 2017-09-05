# django-tutorial

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
