from .views import VideoListView, SearchResultsView, FilterByViews, VideoDetailView, Sync
from django.urls import path

urlpatterns = [
    path('', VideoListView.as_view(), name='home'),
    path('search/', SearchResultsView.as_view(), name='search_results'),
    path('sort-by-views/', FilterByViews.as_view(), name='sort_views'),
    path('video-detail/<slug>/', VideoDetailView.as_view(), name='video_detail'),
    path('sync/', Sync, name='sync'),
]