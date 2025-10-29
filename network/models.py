from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings

class User(AbstractUser):
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        through='Follow',
        through_fields=('to_user', 'from_user'),
        blank=True,
    )

    def __str__(self):
        return self.username

class Follow(models.Model):
    from_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='outgoing_follows'
    )
    to_user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='incoming_follows'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('from_user', 'to_user')
        indexes = [
            models.Index(fields=['from_user']),
            models.Index(fields=['to_user']),
        ]

    def __str__(self):
        return f"{self.from_user} → {self.to_user}"


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return f"Post by {self.author.username} at {self.timestamp}"