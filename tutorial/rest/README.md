# Django REST Framework Tutorial

The tutorial can be found [here](http://www.django-rest-framework.org/#tutorial).

This file contains notes about the content of the tutorial.



## 1) Serialization

A serializer class is very similar to a Django `Form` class,
and includes similar validation flags on the various fields,
such as `required`, `max_length` and `default`.
The field flags can also control how the serializer should be displayed in certain circumstances,
such as when rendering to HTML.

With a serializer, it is quite easy to render a model instance into representations (e.g. json)
as well as to transform such a representation to a Python model instance (deserialization).
It is also possible to serialize querysets instead of model instances
(through adding a `many=True` flag to the serializer arguments).

By using `ModelSerializer` classes we can save ourselves some time.
They are a simple shortcut for creating serializer classes,
because they have an automatically determined set of fields
and simple default implementations for the `create()` and `update()` methods.

You can inspect all the fields in a serializer instance e.g. by printing its representation:
```python
from .serializers import YourSerializer

serializer = YourSerializer()
print(repr(serializer))
```



## 2) Requests & Responses

REST framework introduces a `Request` object that extends the regular `HttpRequest`,
and provides more flexible request parsing.
The core functionality of the `Request` object is the `request.data` attribute
which handles arbitrary data and works for 'POST', 'PUT' and 'PATCH' methods.
This is similar to `request.POST` which only handles form data and only works for 'POST' method.

REST framework also introduces a `Response` object,
which is a type of `TemplateResponse` that takes unrendered content
and uses content negotiation to determine the correct content type to return to the client.
```python
return Response(data) # Renders to content type as requested by the client.
```

REST framework provides two wrappers you can use to write API views:
the `@api_view` decorator for working with function based views
and the `APIView` class for working with class-based views.
These wrappers provide a few bits of functionality
such as making sure you receive `Request` instances in your view,
and adding context to `Response` objects so that content negotiation can be performed.
The wrappers also provide behaviour
such as returning `405 Method Not Allowed` responses when appropriate,
and handling any `ParseError` exception that occurs
when accessing `request.data` with malformed input.

Using those things we no longer need to explicitly tying our requests or responses
to a given content type.
`request.data` can handle incoming `json` requests, but it can also handle other formats.
Similarly we're returning response objects with data,
but allowing REST framework to render the response into the correct content type for us.

To take advantage of the fact that our responses are no longer hardwired to a single content type
we can add support for format suffixes to our API endpoints
by adding a `format` keyword argument to the views
and appending a set of `format_suffix_patterns` in addition to the URLs.
Using format suffixes gives us URLs that explicitly refer to a given format,
and means our API will be able to handle URLs such as <http://example.com/api/items/4.json>.



## 3) Class-based Views

We can write our API views using class-based views which is a powerful pattern
that allows us to reuse common functionality and helps us keep our code DRY
([**D**on't **R**epeat **Y**ourself](https://en.wikipedia.org/wiki/Don't_repeat_yourself)).

One of the big wins of using class-based views is that it allows us
to easily compose reusable bits of behaviour (e.g. create/retrieve/update/delete operations).
Those bits of common behaviour are implemented in REST framework's mixin classes
which slightly reduce the code, but we can go one step further.
REST framework provides a set of already mixed-in generic views
(e.g. `generics.ListCreateAPIView` or `generics.RetrieveUpdateDestroyAPIView`)
that we can use to trim down our `views.py` module even more.



## 4) Authentication & Permissions

A field which is a reverse relationship on a model
will not be included by default when using the `ModelSerializer` class,
so we need to add an explicit field for it in the corresponding serializer.

The `source` argument of a serializer's field controls which attribute is used
to populate a field, and can point at any attribute on the serialized instance.
It can also take the dotted notation (e.g. `'owner.username'`),
in which case it will traverse the given attributes,
in a similar way as it is used with Django's template language.

The untyped `ReadOnlyField` class is always read-only,
and will be used for serialized representations,
but will not be used for updating model instances when they are deserialized.
Another way to achieve this is to use `CharField(read_only=True)`.

By overriding a `.perform_create()` method on a generic class-based view,
we can modify how the instance save is managed,
and handle any information that is implicit in the incoming request or requested URL.
This way we can e.g. associate a user with a snippet instance:
```python
def perform_create(self, serializer):
    serializer.save(owner=self.request.user)
```
In this case, the `create()` method of the serializer
will be passed an additional `'owner'` field,
along with the validated data from the request.

REST framework includes a number of permission classes
that we can use to restrict who can access a given view.
An example is `IsAuthenticatedOrReadOnly` which will ensure
that authenticated requests get read-write access,
and unauthenticated requests get read-only access:
```python
from rest_framework import generics, permissions

class SomeList(generics.ListAPIView):
    # ...
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
```
Of course you can also create custom permissions.

We can add a login view for use with the browsable API,
by editing the URLconf in the **project-level** `urls.py` file.
Therefore we have to import `include` from `django.conf.urls` and
add `url(r'^api-auth/', include('rest_framework.urls')),` at the end of the `urlpatterns` list.
The `r'^api-auth/'` part of pattern can actually be whatever URL you want to use.
