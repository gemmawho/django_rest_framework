from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class Post(models.Model):
    text = models.TextField(verbose_name='Текст', help_text='Напишите то, что у вас на душе')
    pub_date = models.DateTimeField('date published', auto_now_add=True, db_index=True)
    author = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    objects = (text, pub_date, author, image)

    def __str__(self):
        return self.text


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    objects = (post, author, text, created)
