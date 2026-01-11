from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ContributorViewSet, IssueViewSet

router = DefaultRouter()

router.register('projects', ProjectViewSet, basename='project')
router.register('contributors', ContributorViewSet, basename='contributor')
router.register('issues', IssueViewSet, basename='issue')

urlpatterns = [
    path('', include(router.urls)),
]