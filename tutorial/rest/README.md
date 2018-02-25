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
