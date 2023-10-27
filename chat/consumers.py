import json
from asgiref.sync import sync_to_async

from django.contrib.auth.models import AbstractBaseUser
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .models import ChatMessage
from .serializers import ChatMessageSerializer


class ChatConsumer(AsyncWebsocketConsumer):
    """This Consumer is for handling the Chat Feature of Padi.
    It was built around the concept every user should have a room for private DMs with channels
    for Devices or User connections.
    """

    direct_message_name_identifier = "chat_%s"

    async def check_user_is_authenticated(self) -> type[AbstractBaseUser]:
        """Checks if the user is authenticated, then returns the user

        Returns:
            type[AbstractBaseUser]: The user base model
        """
        user = self.scope["user"]
        if not user.id:
            await self.accept()
            await self.send(
                json.dumps(
                    {
                        "error": "Invalid, Expired or Null Token",
                        "detail": "You need to be authenticated to have access to this feature",
                    }
                )
            )
            await self.close()
        else:
            return user

    async def connect(self):
        """Event Listener on user connection for WebSocket"""
        user = await self.check_user_is_authenticated()

        try:
            # Use User ID to either create or join a room unique to them(via id) for their private DMs
            self.room_name = self.direct_message_name_identifier % user.id
            await self.channel_layer.group_add(self.room_name, self.channel_name)

            # I purposely create this pass below here, indicating possibly in the future you can create groups
            # then check all the groups the user belongs to, then add the user to the group on connection.
            pass

            await self.accept()

            # Over here, you will check for all saved messages that haven't been sent to the channel or user
            # and then send, user in the sense you want only a user to be able to receive messages and not channels
            # the user belongs to(this way you could use the 'last_seen' timestamp to figure out which messages to send before updating the last seen)
            # the channel in the sense you want every single channel(devices the user is connected on - (much better approach))
            # to be able to receive the messages(this way the channel(device) has to be the one to send it's last app use time(or last message timestamp))
        except Exception:
            await self.close()  # not a valid chat for this user -> close conn

    async def disconnect(self, code):
        # leave channel group if joined
        if hasattr(self, "room_name"):
            await self.channel_layer.group_discard(self.room_name, self.channel_name)

    async def receive(self, text_data):
        """Event Listener on user message send

        Args:
            text_data: Payload sent to the connection
        """
        # create a feature for users to be able to retrieve last messages partially based on timestamp, or fully(all messages of the user)
        user = await self.check_user_is_authenticated()
        try:
            data = json.loads(text_data)
            # Attaches User ID to data to depict as the sender
            data["sender"] = user.id
        except json.JSONDecodeError as e:
            await self.send(
                json.dumps({"error": "Invalid JSON data format", "detail": str(e)})
            )
            return
        message_serializer = ChatMessageSerializer(data=data)

        if not await sync_to_async(message_serializer.is_valid)():
            await self.send(json.dumps(message_serializer.errors))
            return
        else:
            try:
                # Technically user_id(until group feature is probably added)
                message = message_serializer.data
                recipient_room_id = message.get("recipient_room_id")
                # create message then send to channel group
                # msg_obj = await self.create_message(message, sender, uuid)

                await self.channel_layer.group_send(
                    self.direct_message_name_identifier % recipient_room_id,
                    {
                        "type": "chat.message",
                        "message": message.get("message_body"),
                        "sender_id": message.get("sender"),
                        "sender_channel_name": self.channel_name,
                    },
                )
            except Exception as e:
                print(e)
                # TODO: log error here
                await self.send(
                    json.dumps(
                        {
                            "type": "error",
                            "data": {
                                "message": "There was an error sending your message"
                            },
                        }
                    )
                )

    async def chat_message(self, event):
        # ignore message if sent to self
        if self.channel_name != event["sender_channel_name"]:
            print("does not match")
            await self.send(
                json.dumps(
                    {
                        "type": "chat_message",
                        "data": {
                            "message": event["message"],
                            "sender_id": event["sender_id"],
                        },
                    }
                ),
            )
