from rest_framework.serializers import ModelSerializer, SlugRelatedField, StringRelatedField

from base.models import Room, User, Topic


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'bio']


class TopicSerializer(ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'name']


class RoomSerializer(ModelSerializer):
    host = UserSerializer(many=False, read_only=True)
    topic = TopicSerializer(many=False, read_only=True)
    participants = SlugRelatedField(slug_field='username', many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['name', 'description', 'host', 'topic', 'participants']


class TopicWithRoomSerializer(ModelSerializer):
    rooms = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Room
        fields = ['name', 'rooms']


class DetailedUserSerializer(ModelSerializer):
    hosted_rooms = StringRelatedField(many=True, read_only=True)
    rooms = StringRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['name', 'username', 'email', 'bio', 'hosted_rooms', 'rooms']
