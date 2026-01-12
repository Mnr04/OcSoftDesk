from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, IssueViewSet, ContributorViewSet

router = DefaultRouter()

router.register('projects', ProjectViewSet, basename='project')
router.register('issues', IssueViewSet, basename='issue')
router.register('contributors', ContributorViewSet, basename='contributor')


urlpatterns = [
    path('', include(router.urls)),
]