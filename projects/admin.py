from django.contrib import admin
from .models import Project, Contributor, Issue
# Register your models here.

admin.site.register(Project)
admin.site.register(Contributor)
admin.site.register(Issue)
