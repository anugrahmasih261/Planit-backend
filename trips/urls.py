from django.urls import path
from .views import (
    TripListView, TripDetailView,
    ActivityListView, ActivityDetailView,
    invite_user, vote_activity, join_trip
)

urlpatterns = [
    path('', TripListView.as_view(), name='trip-list'),
    path('<int:pk>/', TripDetailView.as_view(), name='trip-detail'),
    path('<int:trip_id>/activities/', ActivityListView.as_view(), name='activity-list'),
    path('<int:trip_id>/activities/<int:pk>/', ActivityDetailView.as_view(), name='activity-detail'),
    path('<int:trip_id>/invite/', invite_user, name='invite-user'),
    path('<int:trip_id>/activities/<int:activity_id>/vote/', vote_activity, name='vote-activity'),
    path('join/', join_trip, name='join-trip'),
]

