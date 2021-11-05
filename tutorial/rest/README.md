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



## 5) Relationships & Hyperlinked APIs

There are a number of different ways that we can choose
to represent a relationship between entities:
* Using primary keys.
* Using hyperlinking between entities.
* Using a unique identifying slug field on the related entity.
* Using the default string representation of the related entity.
* Nesting the related entity inside the parent representation.
* Some other custom representation.
REST framework supports all of these styles,
and can apply them across forward or reverse relationships,
or apply them across custom managers such as generic foreign keys.

To use a hyperlinked style between entities,
the serializers should extend `HyperlinkedModelSerializer`,
which has the following differences from `ModelSerializer`:
* It does not include the `id` field by default.
* It includes a `url` field, using `HyperlinkedIdentityField`.
* Relationships use `HyperlinkedRelatedField`, instead of `PrimaryKeyRelatedField`.
We also need to make sure we name our URL patterns if we want to have a hyperlinked API.

In case we defined an `app_name` in `urls.py`,
we have to take it into account whenever we set a `view_name`.
And because the `'url'` fields included by our serializers
by default will refer to `'{model_name}-detail'`
we especially have to specify those within our serializers, e.g. like this:
```python
class UserSerializer(serializers.HyperlinkedModelSerializer):
    # ...

    class Meta:
        # ...
        extra_kwargs = {'url': {'view_name': 'appname:user-detail'}}
```



## 6) ViewSets & Routers

`ViewSet` classes are almost the same thing as `View` classes,
except that they provide operations such as `read` or `update`,
and not method handlers such as `get` or `put`.
A `ViewSet` class is only bound to a set of method handlers at the last moment,
when it is instantiated into a set of views, typically by using a `Router` class
which handles the complexities of defining the URL conf for you.
So the developer can concentrate on modeling the state and interactions of the API,
and leave the URL construction to be handled automatically, based on common conventions.
Using viewsets helps ensure that URL conventions will be consistent across your API
and minimizes the amount of code you need to write,
but it is less explicit than building your views individually.

A single `ViewSet` class can replace multiple `View` classes,
e.g. `UserList` and `UserDetail` which are `View` classes can be refactored
into a single `UserViewSet` class.
We still have to set the attributes exactly as we do when we are using regular views,
but we don't need to provide the same information to multiple classes.
The `ModelViewSet` class provides the complete set of default read and write operations
while e.g. the `ReadOnlyModelViewSet` class only provides the default 'read-only' operations.
We can use the `@detail_route` decorator to add any custom endpoints
that don't fit into the standard `create`/`update`/`delete` style.
Custom actions which use the `@detail_route` decorator
will respond to `GET` requests by default.
We can use the `methods` argument if we want an action that responds to `POST` requests.
The URLs for custom actions by default depend on the method name itself.
If you want to change the way url should be constructed,
you can include `url_path` as a decorator keyword argument.

By using `ViewSet` classes instead of `View` classes,
the conventions of wiring up resources into views and urls
can be handled automatically, [using a `Router` class](http://www.django-rest-framework.org/tutorial/6-viewsets-and-routers/#using-routers).
All we need to do is register the appropriate viewsets with a router,
which is similar to providing an urlpattern, and let it do the rest.
Using the `DefaultRouter` class,
we don't need to implement an `api_root` method in `views.py`
because the `DefaultRouter` class automatically creates that view for us.



## 7) Schemas & Client Libraries

A schema is a machine-readable document that describes the available API endpoints,
their URLs, and what operations they support.
Schemas can be a useful tool for auto-generated documentation,
and can also be used to drive dynamic client libraries that can interact with the API.

In order to provide schema support REST framework uses [Core API](http://www.coreapi.org/).
REST framework supports either explicitly defined schema views,
or automatically generated schemas.
By using viewsets and routers, wen can simply use the automatic schema generation.
