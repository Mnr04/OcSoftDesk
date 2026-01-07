from django.db import models
from users.models import User
import uuid

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

class Issue(models.Model):
    priority = [('LOW', 'Low'), ('MEDIUM', 'Medium'), ('HIGH', 'High')]
    type = [('BUG', 'Bug'), ('FEATURE', 'Feature'), ('TASK', 'Task')]
    status = [('TODO', 'To Do'), ('IN_PROGRESS', 'In Progress'), ('DONE', 'Done')]

    title = models.CharField(max_length=128)
    description = models.TextField(max_length=2048)
    type = models.CharField(max_length=8, choices=type)
    priority = models.CharField(max_length=10, choices=priority)
    status = models.CharField(max_length=15, choices=status, default='TODO')
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    project = models.ForeignKey(to=Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Comment(models.Model):
    description = models.TextField(max_length=2048)
    created_time = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    issue = models.ForeignKey(to=Issue, on_delete=models.CASCADE)
    uuid = models.UUID(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"Commentaire de {self.author}"