# Fortune

Fortune is an application which gives you the possibility to integrate "fortune cookies" into your work.
Without much effort you can show a different (random) fortune every time a user visits your page.
And if you want, you can specify which category that fortune should be of.



## 1) What Is a Fortune?

A fortune can be any kind of text: a quote, saying, joke or even a story. It only depends on you.
Every fortune belongs to a category so you can have different types of fortunes without any problem.
Some category examples are "Star Wars quotes", "life hacks" or "health tips".
Note that duplicates of fortune texts as well as category names are not allowed.



## 2) How to Create Fortunes

The easiest way is to load fortunes from a file located in the `cookies` folder of the Fortune app.
By default, the file name (including its extension) defines the category name.
Therefore a file name with no extension is recommended.
The file should contain all fortunes of the category that file belongs to.
A line with a `%` symbol between the fortunes works as separator.
Only use it between fortunes, not at the beginning or at the end of a file.
An example:

    This is the first fortune and the very first line of the file.
    %
    This is the
    second fortune.
    %
    This is the
        last fortune with the last line of the file.



### 2.1) Load Fortunes with Class Method

To load fortunes from a file using the class method `load` of the class `Category`,
put the following into your Python code:

```python
from fortune.models import Category, PackAlreadyLoadedError, UnavailablePackError

try:
    Category.load("file name") # Creates a category out of the file's name and creates
                               # a fortune for every fortune text contained by the file.
except PackAlreadyLoadedError: # Raised if a category of the file's name already exists.
    pass # Do something.
except UnavailablePackError: # Raised if the file doesn't exist within 'cookies' folder.
    pass # Do something.
```

You can also load fortunes from all files within the `cookies` folder:

```python
from fortune.models import (Category, get_available_pack_names,
                            UnavailablePackError, PackAlreadyLoadedError)

packs = get_available_pack_names() # Lists all files contained by 'cookies' folder.
for pack in packs:
    try:
        Category.load(pack)
    except PackAlreadyLoadedError:
        pass # Do something.
    except UnavailablePackError:
        pass # Do something.
```



### 2.2) Load Fortunes with Command

To load fortunes from a file using the command `import_fortune`, write the following into your console:

    $ python manage.py import_fortune <file_path> [-c category_name]

By default, it takes the name of the file given through file path and uses it as category name.
But as you can see, you're able to define a different category name.
If you want to specify a category name which contains spaces, use double quotes.
An example:

![import_fortune](/mysite/fortune/static/fortune/images/import_fortune.jpg)



## 3) How to Get a Fortune

To get a random fortune text within your python code, simply write:

```python
from fortune.models import Fortune

fortune = Fortune.fortune() # Returns a random fortune of no specific category.
fortune = Fortune.fortune("category name") # Returns a random fortune of given category.
                                           # If the given category doesn't exist, the
                                           # fortune will be of no specific category.
```

To show a random fortune text on your page,
write `{% load fortunes %}` at the beginning of your template to load the fortune templatetags.
With `{% fortune %}` a random fortune text will be displayed.
To get a fortune text of a specific category, use `{{ "category name" | fortune }}`.



## 4) RabbitMQ and Channels

If you installed docker, you just need to start redis and rabbitmq within a container and not local.

**Redis**

    $  docker run -p 6379:6379 redis

**RabbitMQ**

    $ docker run -p 4369:4369 -p 5672:5672 -p 15672:15672 -p 25672:25672 --hostname your_rabbit --name your-docker-rabbit -e RABBITMQ_DEFAULT_USER=guest -e RABBITMQ_DEFAULT_PASS=guest rabbitmq:3-management 

The default password needs to be known within the django application and within any job which likes
to send via RabbiqMQ a text.

Through RabbitMQ, you can receive messages on an exchange of type `fanout`
which will cause the subscriber in `consumers.py` to send a random fortune text to a Channels group.
The message can be from outside, it only has to be sent through the same RabbitMQ server to that exchange
(don't forget to change the RabbitMQ connection settings if neccessary).
If the message contains a category name, the fortune text will be of that category.
Every channel which got added to that Channels group will receive the fortune text.
The consumers behind that channels can do with it whatever they are supposed to,
e.g. replacing content of a page with the received fortune text.

If you want to send a message through your RabbitMQ server to the exchange,
write one of the following lines into your console:

    $ python fortune\rabbitmq_send.py [category_name]
    $ python manage.py rabbitmq_send [-c category_name]

E.g. sending a message with "starwars" as category using the first line would look like:

![rabbitmq_send script](/mysite/fortune/static/fortune/images/rabbitmq_send_script.jpg)

Doing the same using the second line would look like:

![rabbitmq_send command](/mysite/fortune/static/fortune/images/rabbitmq_send_command.jpg)
