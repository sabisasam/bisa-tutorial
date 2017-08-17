# django-tutorial

## Tutorial part 8

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
