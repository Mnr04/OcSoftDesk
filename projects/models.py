from django.db import models
from users.models import User

class Project(models.Model):
    project_type = [
        ('BACKEND', 'Back-end'),
        ('FRONTEND', 'Front-end'),
        ('IOS', 'iOS'),
        ('ANDROID', 'Android'),
    ]

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    type = models.CharField(max_length=20, choices=project_type)
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.title

class Contributor(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)
    class Meta:
        unique_together = ('user', 'project')

