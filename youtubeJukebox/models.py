from django.db import models

# Create your models here.
class Video(models.Model):
	url = models.URLField()
	videoId = models.CharField(max_length=100,unique=True)
	vote = models.IntegerField(default=0)

	def __str__(self):
		return self.videoId
