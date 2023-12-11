from rest_framework_mongoengine import serializers

from chat.models import ChatMessage


class ChatMessageSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ChatMessage
        exclude = [
            "id",
            "room_name",
            "timestamp",
            # I exempted the last two below because it seems
            "message_type",
            "status",
        ]
        read_only_fields = ("sender_timezone_offset",)


class ChatMessageForServerSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ChatMessage
        fields = []
        read_only_fields = ["intent", "message_body", "sender_timestamp", "timestamp"]
