from rest_framework_mongoengine import serializers

from chat.models import ChatMessage


class ChatMessageSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ChatMessage
        exclude = [
            "id",
            "room_name",
            "receipient_received_from_server_timestamp",
            "timestamp",
        ]


class ChatMessageForServerSerializer(serializers.DocumentSerializer):
    class Meta:
        model = ChatMessage
        fields = []
        read_only_fields = ["intent", "message_body", "sender_timestamp", "timestamp"]
