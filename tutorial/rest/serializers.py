from django.contrib.auth.models import User
from rest_framework import serializers
from rest.models import Snippet


# A serializer class is very similar to a Django Form class.
class SnippetSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    highlight = serializers.HyperlinkedIdentityField(view_name='rest:snippet-highlight', format='html')

    class Meta:
        model = Snippet
        fields = ('url', 'id', 'highlight', 'owner', 'title', 'code', 'linenos', 'language', 'style')
        extra_kwargs = {'url': {'view_name': 'rest:snippet-detail'}}


class UserSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(many=True, view_name='rest:snippet-detail', read_only=True)
    # Because 'snippets' is a reverse relationship on the User model,
    # it will not be included by default when using the ModelSerializer class,
    # so we needed to add an explicit field for it.

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'snippets')
        extra_kwargs = {'url': {'view_name': 'rest:user-detail'}}
