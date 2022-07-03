
from django.db import models

# Create your models here.
class User(models.Model):
    username=models.CharField(max_length=40)
    email=models.EmailField(max_length=40)
    password=models.CharField(max_length=20)
    


    def __str__(self):
        return self.email
    
class Post(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.CharField(max_length=1000)
    upvotes_count=models.IntegerField(default=0)
    date_time=models.DateTimeField(auto_now=True)


    def __str__(self):
        return str(self.id)


class Upvotes(models.Model):
    user_upvote= models.ForeignKey(User,on_delete=models.CASCADE,related_name="user_upvote")
    post_upvote = models.ForeignKey(Post, on_delete=models.CASCADE,related_name="post_upvote")
    upvote_bool = models.BooleanField(default=False)

    def __str__(self):
        return str(self.post_upvote.id) + "number id post is liked by " + self.user_upvote.email



