from django.db import models
from django.contrib.auth import get_user_model


class ChatMessage(models.Model):
    SELF_MESSAGE = "SM"
    DIRECT_MESSAGE = "DM"
    GROUP_MESSAGE = "GM"

    ROOM_TYPES = [
        (SELF_MESSAGE, "Self Message"),
        (DIRECT_MESSAGE, "Direct Message"),
        (GROUP_MESSAGE, "Group Message"),
    ]

    # Room name, for DMs it is technically unique by nature of the User ID(e.g. chat_1)
    room_name = models.CharField(null=True)
    # This is technically the user id, (If My.Padi has or will have the concept of groups, it will be uniquely generated for groups)
    recipient_room_id = models.CharField()
    message_type = models.CharField(
        max_length=2, choices=ROOM_TYPES, default=DIRECT_MESSAGE
    )
    sender = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    message_body = models.CharField(max_length=500)
    sender_timestamp = models.DateTimeField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    # Time the message was sent to the recipient
    receipient_received_from_server_timestamp = models.DateTimeField(null=True)

    def __str__(self):
        return self.message
