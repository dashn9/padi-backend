from rest_framework import serializers

from chat.models import ChatMessage


class ChatMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChatMessage
        exclude = [
            "id",
            "room_name",
            "receipient_received_from_server_timestamp",
            "timestamp",
        ]
