import datetime
from enum import Enum
from mongoengine import *

connect(
    db="message",
)


class ChatMessage(Document):
    class RoomTypes(Enum):
        SELF_MESSAGE = "SM"  # Self Message
        DIRECT_MESSAGE = "DM"  # Direct Message
        GROUP_MESSAGE = "GM"  # Group Message

    # Room name, for DMs it is technically unique by nature of the User ID(e.g. chat_1)
    room_name = StringField()
    # This is technically the user id, (If My.Padi has or will have the concept of groups, it will be uniquely generated for groups)
    recipient_room_id = StringField()
    message_type = EnumField(RoomTypes, default=RoomTypes.DIRECT_MESSAGE)
    sender_id = IntField()
    message_body = StringField(max_length=500)
    sender_timestamp = DateTimeField(null=True)
    timestamp = DateTimeField(default=datetime.datetime.utcnow)
    # Time the message was sent to the recipient
    receipient_received_from_server_timestamp = DateTimeField(null=True)

    def __str__(self):
        return self.message
