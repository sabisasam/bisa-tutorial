from rest_framework import serializers
from rest.models import Snippet


# A serializer class is very similar to a Django Form class.
class SnippetSerializer(serializers.ModelSerializer):
	class Meta:
		model = Snippet
		fields = ('id', 'title', 'code', 'linenos', 'language', 'style')
