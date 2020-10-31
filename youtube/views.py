from django.shortcuts import render
from .models import Video
from django.views.generic import ListView, DetailView
from .forms import SyncForm
from django.db.models import Q
from googleapiclient.discovery import build
import os

api_key = os.environ.get('yt_api_key')
youtube = build('youtube', 'v3', developerKey=api_key)
playlist_id = 'UU6TWeFeoh_oQLxv15hswNxQ'

# Create your views here.
def home(request):
	context = {
		'videos': Video.objects.all().order_by('-date_posted'),
	}

	return render(request, 'youtube/home.html', context)

class VideoListView(ListView):
	model = Video
	template_name = 'youtube/home.html'
	context_object_name = 'videos'

	paginate_by = 9
	ordering = ['-date_posted']

class SearchResultsView(ListView):
	model = Video
	template_name = 'youtube/search_results.html'

	def get_queryset(self):
		query = self.request.GET.get('q')
		video_list = Video.objects.filter(
			Q(title__icontains=query)
		)
		return video_list

class FilterByViews(ListView):
	model = Video
	template_name = 'youtube/sort_views.html'
	context_object_name = 'videos'

	ordering = ['-views']
	paginate_by = 9

class VideoDetailView(DetailView):
	model = Video

def Sync(request):
	cxt = {}
	#Getting all the views and urls of the current videos in the playlist
	if request.method=="POST":
		videos = []

		nextPageToken = None
		while True:
			pl_request = youtube.playlistItems().list(
				part='contentDetails, snippet',
				playlistId=playlist_id,
				maxResults=80,
				pageToken=nextPageToken
			)

			pl_response = pl_request.execute()

			vid_ids = {}
			for item in pl_response['items']:
				videoId = item['contentDetails']['videoId']
				vid_ids[videoId] = {'title': item['snippet']['title'],'description': item['snippet']['description'], 'date_posted': item['snippet']['publishedAt'], 'thumbnail': item['snippet']['thumbnails']['medium']['url']}


			vid_request = youtube.videos().list(
				part="statistics",
				id=','.join(vid_ids)
			)

			vid_response = vid_request.execute()


			for item in vid_response['items']:
				vid_views = item['statistics']['viewCount']

				vid_id = item['id']
				yt_link = f'https://www.youtube.com/watch?v={vid_id}'
				description = vid_ids[vid_id]['description']
				title = vid_ids[vid_id]['title']
				date_posted = vid_ids[vid_id]['date_posted']
				thumbnail = vid_ids[vid_id]['thumbnail']

				videos.append(
					{
						'views': int(vid_views),
						'url': yt_link,
						'description': description,
						'title': title,
						'date_posted': date_posted,
						'thumbnail': thumbnail,
						'slug': vid_id
					}
				)

			nextPageToken = pl_response.get('nextPageToken')

			if not nextPageToken:
				break

		videos.sort(key=lambda vid: vid['views'], reverse=True)

		vids = []
		vidId = []
		nextPageToken = None
		
		# Updating the current views
		for video in videos:
			try:
				# Video.objects.get(video=video['url'])
				r = Video.objects.get(video=video['url'])

				r.views = video['views']
				# r.thumbnail = video['thumbnail']
				# r.slug = video['slug']
				r.save()
			except Video.DoesNotExist:
				# Creating the new video
				v = Video(video=video['url'], title=video['title'], date_posted=video['date_posted'], description=video['description'], views=video['views'], thumbnail=video['thumbnail'], slug=video['slug'])
				v.save() 
		
		cxt['args'] = videos

		# return render(request, 'youtube/sync.html', cxt)
	return render(request, 'youtube/sync.html', cxt)