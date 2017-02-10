from django.db import models



class BlogPost( models.Model ):

	slug = models.SlugField(max_length=70, blank=True)
	title = models.CharField(max_length=200, blank=True)
	text = models.TextField(max_length=4000, default='', blank=True)

	def __unicode__(self):
		return self.title


