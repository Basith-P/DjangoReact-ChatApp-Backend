from rest_framework import serializers

from .models import Channel, Server


class ChannelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Channel
        fields = '__all__'


class ServerSerializer(serializers.ModelSerializer):
    members_count = serializers.SerializerMethodField()
    channels = ChannelSerializer(many=True)

    class Meta:
        model = Server
        exclude = ("members",)

    def get_members_count(self, obj):
        if hasattr(obj, "members_count"):
            return obj.members_count
        return None

    def to_representation(self, instance):
        data = super().to_representation(instance)
        members_count = self.context.get("members_count")
        if not members_count:
            data.pop("members_count", None)
        return data
