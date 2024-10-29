import json

from django.http.response import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view

from base import models
from base.api.serializers import (
    RoomSerializer, TopicWithRoomSerializer, DetailedUserSerializer, TopicSerializer,
)


def get_routes(request):
    routes = [
        'GET /api',
        'GET /api/rooms',
        'GET /api/rooms/:id',
        'GET /api/topics',
    ]
    return JsonResponse(routes, safe=False)


@api_view(['GET'])
def get_rooms(request):
    rooms = models.Room.objects.all()
    serializer = RoomSerializer(instance=rooms, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_room(request, id):
    room = models.Room.objects.get(pk=id)
    serializer = RoomSerializer(instance=room, many=False)
    return Response(serializer.data)


@api_view(['GET'])
def get_topics(request):
    topics = list(models.Topic.objects.all())
    # topic_names = [topic.name for topic in topics]
    # return HttpResponse(json.dumps(topic_names))
    serializer = TopicWithRoomSerializer(instance=topics, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_user(request, id):
    user = models.User.objects.get(pk=id)
    serializer = DetailedUserSerializer(instance=user, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def create_topic(request):
    serializer = TopicSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)
