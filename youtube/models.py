from django.db import models
from django.utils.text import slugify
from embed_video.fields import EmbedVideoField
from django.utils import timezone
from PIL import Image

# Create your models here.
from embed_video.fields import EmbedVideoField

class Video(models.Model):
	video = EmbedVideoField()
	title = models.CharField(max_length=150, default="Video")
	video_id = models.CharField(max_length=150, default="000000000000000")
	date_posted = models.CharField(max_length=20, default="0000-00-00")
	thumbnail = models.CharField(max_length=50, default="https://i.ytimg.com/vi/7NpvXBM4-1A/mqdefault.jpg")
	description = models.TextField(default="Enjoy!")
	views = models.IntegerField(default=0)
	slug = models.SlugField(max_length=150, default="none", allow_unicode=True)

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("video_detail", kwargs={"slug": self.slug})