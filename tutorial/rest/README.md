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



## 2) Requests and Responses

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
