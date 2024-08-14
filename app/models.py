
from django.db import models
from django.contrib.auth.models import User


from django.utils.text import slugify
from django.urls import reverse
from django.db.models.signals import pre_save
from django.utils import timezone

class Notice(models.Model):
    content = models.TextField()

    def save(self, *args, **kwargs):
        # Check if there's already an announcement
        if Notice.objects.exists():
            # Delete the existing announcement
            Notice.objects.all().delete()
        # Save the new announcement
        super().save(*args, **kwargs)

    def __str__(self):
        return self.content[:50]



class Categories(models.Model):
    icon = models.CharField(max_length=200, null=True)
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Author(models.Model):
    author_profile = models.ImageField(upload_to="Media/author")
    name = models.CharField(max_length=100, null=True)
    about_author = models.TextField()

    def __str__(self):
        return self.name

class Course(models.Model):
    featured_image = models.ImageField(upload_to="Media/featured_img", null=True)
    course_title=models.CharField(max_length=100)
    
    
    
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    description = models.TextField()
    title = models.CharField(max_length=500)
    
    slug = models.SlugField(max_length=100,null=True, unique=True, blank=False)
    

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return reverse("course_details", kwargs={'slug': self.slug})
    



class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name='lessons', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    notes_pdf = models.FileField(upload_to="lesson_notes", null=True, blank=True)

    def __str__(self):
        return self.name + " - " + self.course.title

class Video(models.Model):
    serial_number = models.IntegerField(null=True)
    
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, related_name='videos', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    youtube_id = models.CharField(max_length=200, null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    time_duration = models.FloatField(null=True)
    video_file = models.FileField(upload_to='Media/videos/', null=True, blank=True)
    

    def __str__(self):
        return self.title

    def get_video_source(self):
        if self.youtube_id:
            return f"https://www.youtube.com/embed/{self.youtube_id}"
        elif self.video_url:
            return self.video_url
        elif  self.video_file:
            return self.video_file.url
        return None
    
class CourseAccess(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, on_delete=models.CASCADE)
    access_granted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.course.title} - {self.category.name}"




