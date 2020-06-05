from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator


class Board(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    def get_posts_count(self):
        return Post.objects.filter(topic__board=self).count()

    def get_last_post(self):
        return Post.objects.filter(topic__board=self).order_by('-created_at').first()
    

class Topic(models.Model):
    subject = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='topics')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='topics')
    views_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

    def last_updated(self):
        last_update = self.posts.order_by('-created_at').first()
        if not last_update:
            last_update = self.created_at
        else:
            last_update = last_update.created_at
        return last_update


class Post(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='posts')
    message = models.TextField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    authored_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    moderated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='+', null=True, blank=True)

    def __str__(self):
        truncated_msg = Truncator(self.message)
        return truncated_msg.chars(30)
    
        