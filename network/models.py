from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    date_update = models.DateTimeField(auto_now=True, null=True)

class Post(models.Model):
    text = models.TextField(blank = True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posted_by")

    def __str__(self):
        return f"{self.id}: {self.text}"

class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_likes")
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}: {self.user.username} - {self.post.text}" 

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="post_comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_comments")
    comment = models.TextField()
    date_creation = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}: {self.user.username} - {self.comment} - {self.post.text}" 

# los seguidores de user_id
class UserFollowing(models.Model):
    user_id = models.ForeignKey("User",on_delete=models.CASCADE, related_name="following")
    following_user_id = models.ForeignKey("User", on_delete=models.CASCADE, related_name="followers")
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user_id.username}"