from django.urls import path
from .views import VideoUploadView, LLMSearchView

urlpatterns = [
    path('upload/', VideoUploadView.as_view(), name='video-upload'),
    path('search/', LLMSearchView.as_view(), name='llm-search'),
]