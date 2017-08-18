# django-tutorial

## Signal Handling

A model named QuestionHistory with question and creation_time as its attributes got added.
If a question is added to the database, an instance of QuestionHistory gets created.
The attribute creation_time will be set to the datetime at that moment
and question is simply the question it relates to.
The question attribute will be set to null if the question object gets deleted.
