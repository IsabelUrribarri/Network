from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    date_creation = models.DateTimeField(auto_now_add=True, null=True)
    date_update = models.DateTimeField(auto_now=True, null=True)
    banner_url_image = models.URLField(max_length=500, default="https://media.istockphoto.com/id/1260122654/photo/autumn-landscape-beautiful-city-park-with-fallen-yellow-leaves.jpg?s=612x612&w=0&k=20&c=EVuX7Mp6nqzHaGijUPS98KpNsF6j_6Q4-vhmY9x8U-0=")
    photo_url_image = models.URLField(max_length=500, default="https://ichef.bbci.co.uk/news/660/cpsprodpb/48DD/production/_107435681_perro1.jpg")

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
        return f"seguidor: {self.user_id.username} - siguiendo a: {self.following_user_id.username}"
