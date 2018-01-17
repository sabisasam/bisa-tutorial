import os 
from django.contrib.auth.models import User 
print (os.environ['USERNAME'] + ' user already exists') if User.objects.filter(username=os.environ['USERNAME']) else User.objects.create_superuser(os.environ['USERNAME'], os.environ['EMAIL'], os.environ['PASSWORD'])
