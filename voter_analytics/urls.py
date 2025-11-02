# voter_analytics/urls.py
# Amy Ho, aho@bu.edu

from django.urls import path
from . import views 
 
urlpatterns = [
    # map the URL (empty string) to the view
	path(r'', views.VotersListView.as_view(), name='home'),
    path(r'search/', views.search_view, name='search'),
    path(r'voter', views.VotersListView.as_view(), name='voters_list'),
    path(r'voter/<int:pk>', views.VoterDetailView.as_view(), name='voter_detail'),
]
 