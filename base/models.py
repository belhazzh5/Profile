from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

from django.utils.text import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Activity(models.Model):
	text = models.TextField()	

class Category(models.Model):
	name =  models.CharField(max_length=50)
	def __str__(self):
		return self.name
	
class Skill(models.Model):
	title = models.CharField(max_length=50)
	power = models.IntegerField()
	def __str__(self):
		return self.title
	
class Galerie(models.Model):
	image = models.ImageField(upload_to='images/project',default='/static/assets/img/work-4.jpg')
	
class Project(models.Model):
	title = models.CharField(max_length=100)
	description = models.TextField()
	url = models.URLField(max_length=200)
	images = models.ManyToManyField(Galerie)
	created = models.DateField()
	category = models.ForeignKey(Category,  on_delete=models.PROTECT,blank=True,null=True)
	slug = models.SlugField(blank=True,null=True)
	def __str__(self):
		return self.title
	def save(self, *args, **kwargs):

		if self.slug is None:
			slug = slugify(self.title)

			has_slug = Project.objects.filter(slug=slug).exists()
			count = 1
			while has_slug:
				count += 1
				slug = slugify(self.title) + '-' + str(count) 
				has_slug = Project.objects.filter(slug=slug).exists()

			self.slug = slug

		super().save(*args, **kwargs)
class Me(models.Model):
	first_name = models.CharField(max_length=200, blank=True, null=True)
	last_name = models.CharField(max_length=200, blank=True, null=True)
	email = models.CharField(max_length=200)
	profile_pic = models.ImageField(null=True, blank=True, upload_to="images", default="/user.png")
	title = models.TextField(null=True, blank=True)
	bio = models.ManyToManyField(Activity)
	skills = models.ManyToManyField(Skill)
	phone = models.CharField(max_length=200,null=True, blank=True)
	projects = models.ManyToManyField(Project)
	def __str__(self):
		name = str(self.first_name)
		if self.last_name:
			name += ' ' + str(self.last_name)
		return name

class Profile(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	first_name = models.CharField(max_length=200, blank=True, null=True)
	last_name = models.CharField(max_length=200, blank=True, null=True)
	email = models.CharField(max_length=200)
	profile_pic = models.ImageField(null=True, blank=True, upload_to="images", default="/user.png")
	bio = models.TextField(null=True, blank=True)
	twitter = models.CharField(max_length=200,null=True, blank=True)

	def __str__(self):
		name = str(self.first_name)
		if self.last_name:
			name += ' ' + str(self.last_name)
		return name

class Tag(models.Model):
	name = models.CharField(max_length=200)

	def __str__(self):
		return self.name


class Post(models.Model):
	headline = models.CharField(max_length=200)
	sub_headline = models.CharField(max_length=200, null=True, blank=True)
	description = models.CharField(max_length=200,null=True,blank=True)
	thumbnail = models.ImageField(null=True, blank=True, upload_to="images", default="/images/placeholder.png")
	body = RichTextUploadingField(null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True)
	active = models.BooleanField(default=False)
	featured = models.BooleanField(default=False)
	tags = models.ManyToManyField(Tag)
	slug = models.SlugField(null=True, blank=True)

	def __str__(self):
		return self.headline
	
	def get_absolute_url(self):
		return reverse("post", kwargs={"slug": self.slug})

	def save(self, *args, **kwargs):

		if self.slug == None:
			slug = slugify(self.headline)

			has_slug = Post.objects.filter(slug=slug).exists()
			count = 1
			while has_slug:
				count += 1
				slug = slugify(self.headline) + '-' + str(count) 
				has_slug = Post.objects.filter(slug=slug).exists()

			self.slug = slug

		super().save(*args, **kwargs)

class SubComment(models.Model):
	author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
	body = models.TextField(null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	def __str__(self):
		return str(self.author)
	
class PostComment(models.Model):
	author = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
	post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
	body = models.TextField(null=True, blank=True)
	created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
	subComment = models.ManyToManyField(SubComment)
	def __str__(self):
		return self.body

	@property
	def created_dynamic(self):
		now = timezone.now()
		return now

class Message(models.Model):
	name = models.CharField(max_length=200,null=True,blank=True)
	email = models.EmailField()
	subject = models.CharField(max_length=200,null=True,blank=True)
	message = models.TextField()
	def __str__(self):
		return self.name
	