from rest_framework import serializers

from .models import Channel, Server


class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = '__all__'


class ServerSerializer(serializers.ModelSerializer):
    channels = ChannelSerializer(many=True)

    class Meta:
        model = Server
        fields = '__all__'
