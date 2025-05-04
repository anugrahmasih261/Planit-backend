from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import get_object_or_404
from .models import Trip, TripParticipant, Activity, ActivityVote
from .serializers import TripSerializer, ActivitySerializer, InviteUserSerializer, VoteSerializer
from users.models import User

class TripListView(generics.ListCreateAPIView):
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Include trips where user is either creator or participant
        return Trip.objects.filter(
            participants__user=self.request.user
        ).distinct().order_by('-created_at')
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

class TripDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TripSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Trip.objects.filter(participants__user=self.request.user)


#old one

# class ActivityListView(generics.ListCreateAPIView):
#     serializer_class = ActivitySerializer
#     permission_classes = [permissions.IsAuthenticated]
    
#     def get_queryset(self):
#         trip_id = self.kwargs['trip_id']
#         return Activity.objects.filter(
#             trip_id=trip_id, 
#             trip__participants__user=self.request.user
#         ).order_by('date', 'time')
    
#     def perform_create(self, serializer):
#         trip = get_object_or_404(
#             Trip, 
#             id=self.kwargs['trip_id'], 
#             participants__user=self.request.user
#         )
#         serializer.save(trip=trip, created_by=self.request.user)



#new one

class ActivityListView(generics.ListCreateAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        trip_id = self.kwargs['trip_id']
        return Activity.objects.filter(
            trip_id=trip_id, 
            trip__participants__user=self.request.user
        ).order_by('date', 'time')
    
    def perform_create(self, serializer):
        trip = get_object_or_404(
            Trip, 
            id=self.kwargs['trip_id'], 
            participants__user=self.request.user
        )
        serializer.save(trip=trip, created_by=self.request.user)




class ActivityDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ActivitySerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        trip_id = self.kwargs['trip_id']
        return Activity.objects.filter(
            trip_id=trip_id, 
            trip__participants__user=self.request.user
        )

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def invite_user(request, trip_id):
    trip = get_object_or_404(Trip, id=trip_id, created_by=request.user)
    serializer = InviteUserSerializer(data=request.data)
    
    if serializer.is_valid():
        user = User.objects.get(email=serializer.validated_data['email'])
        
        if TripParticipant.objects.filter(trip=trip, user=user).exists():
            return Response(
                {'detail': 'User is already a participant'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        TripParticipant.objects.create(trip=trip, user=user)
        return Response(
            {'detail': 'User invited successfully'}, 
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def vote_activity(request, trip_id, activity_id):
    activity = get_object_or_404(
        Activity,
        id=activity_id,
        trip_id=trip_id,
        trip__participants__user=request.user
    )
    
    serializer = VoteSerializer(data=request.data)
    if serializer.is_valid():
        vote, created = ActivityVote.objects.update_or_create(
            activity=activity,
            user=request.user,
            defaults={'vote': serializer.validated_data['vote']}
        )
        return Response(
            {'detail': 'Vote recorded'}, 
            status=status.HTTP_201_CREATED
        )
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def join_trip(request):
    trip_code = request.data.get('trip_code')
    if not trip_code:
        return Response(
            {'detail': 'Trip code is required'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    trip = get_object_or_404(Trip, trip_code=trip_code)
    
    if TripParticipant.objects.filter(trip=trip, user=request.user).exists():
        return Response(
            {'detail': 'Already a participant'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    TripParticipant.objects.create(trip=trip, user=request.user)
    return Response(
        {'detail': 'Joined trip successfully'}, 
        status=status.HTTP_201_CREATED
    )