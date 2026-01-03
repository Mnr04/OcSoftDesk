from django.urls import path
from .views import project_view, contributor_view, issue_view

urlpatterns = [
    path('projects/', project_view, name='project-list'),
    path('projects/<int:pk>/', project_view, name='project-detail'),

    path('contributors/', contributor_view, name='contributor-list'),
    path('contributors/<int:pk>/', contributor_view, name='contributor-detail'),

    path('issues/', issue_view, name='issue-list'),
    path('issues/<int:pk>/', issue_view, name='issue-detail'),

]