from django.contrib.auth.models import User
from django.db import models


class Follow(models.Model):
    user = models.ForeignKey(
        User, related_name="following", on_delete=models.CASCADE
    )
    following = models.ForeignKey(
        User, related_name="followers", on_delete=models.CASCADE
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "following")

    def __str__(self):
        return f"{self.user} follows {self.following}"
