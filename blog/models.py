from django.db import models
from user.models import UserProfile
from sport.models import Sport

def blog_directory_path(instance, filename):
	return 'blog/post/{0}_{1}'.format(instance.id,filename)

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    last_modification_date = models.DateTimeField(auto_now=True)
    sport = models.ForeignKey(Sport, blank=False)
    title = models.CharField(max_length=140)
    description = models.TextField(max_length=400, blank=True)
    content = models.TextField()
    picture = models.ImageField(upload_to=blog_directory_path, default=None, null=True, blank=True)

    def __str__(self):
            return self.title+' by '+self.author.displayName
