from rest_framework import serializers
from .models import Trip, TripParticipant, Activity, ActivityVote
from users.models import User
import random
import string

class TripParticipantSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.CharField(source='user.email', read_only=True)
    
    class Meta:
        model = TripParticipant
        fields = ['id', 'user', 'username', 'email', 'joined_at']

class ActivityVoteSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    
    class Meta:
        model = ActivityVote
        fields = ['id', 'user', 'vote', 'voted_at']





# new one

class ActivitySerializer(serializers.ModelSerializer):
    trip = serializers.PrimaryKeyRelatedField(read_only=True)
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    votes = ActivityVoteSerializer(many=True, read_only=True)
    upvotes = serializers.SerializerMethodField()
    downvotes = serializers.SerializerMethodField()
    
    class Meta:
        model = Activity
        fields = ['id', 'trip', 'title', 'date', 'time', 'category', 
                 'estimated_cost', 'notes', 'created_by', 'created_at',
                 'votes', 'upvotes', 'downvotes']
        extra_kwargs = {
            'estimated_cost': {'required': False, 'allow_null': True},
            'time': {'required': False, 'allow_null': True},
            'notes': {'required': False, 'allow_null': True},
            'date': {'required': True}
        }
    
    def get_upvotes(self, obj):
        return obj.votes.filter(vote=True).count()
    
    def get_downvotes(self, obj):
        return obj.votes.filter(vote=False).count()



class TripSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)
    participants = TripParticipantSerializer(many=True, read_only=True)
    activities = ActivitySerializer(many=True, read_only=True)
    
    class Meta:
        model = Trip
        fields = ['id', 'name', 'start_date', 'end_date', 'group_budget',
                 'created_by', 'created_at', 'trip_code', 'participants', 'activities']
        extra_kwargs = {
            'trip_code': {'required': True}
        }
    
    def validate(self, data):
        if 'trip_code' in data and Trip.objects.filter(trip_code=data['trip_code']).exists():
            raise serializers.ValidationError({'trip_code': 'This trip code is already in use.'})
        return data
    
    def create(self, validated_data):
        # Remove created_by if it somehow got included
        validated_data.pop('created_by', None)
        
        trip = Trip.objects.create(
            **validated_data,
            created_by=self.context['request'].user
        )
        
        # Add creator as participant
        TripParticipant.objects.create(trip=trip, user=self.context['request'].user)
        return trip

class InviteUserSerializer(serializers.Serializer):
    email = serializers.EmailField()
    
    def validate_email(self, value):
        if not User.objects.filter(email=value).exists():
            raise serializers.ValidationError("User with this email does not exist.")
        return value

class VoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivityVote
        fields = ['vote']