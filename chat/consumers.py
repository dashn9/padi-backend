import json
from asgiref.sync import sync_to_async

from django.contrib.auth.models import AbstractBaseUser
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async

from .serializers import ChatMessageSerializer
from .models import RoomTypes as MessageTypes


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
            # then check all the groups the user belongs to, then add the user's channel to the group on connection.
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

    @database_sync_to_async
    def save_chat_message_serializer(self, serializer: ChatMessageSerializer) -> None:
        """Saves a ChatMessageSerializer, Serializer save is synchronous in nature, therefore, there is a need to make the operation asynchronous

        Args:
            serializer (ChatMessageSerializer): The ChatMessage Serializer to save

        Return: None
        """
        serializer.save()

    async def parse_message(self, text_data: str, send_error=True) -> dict | None:
        """This function uses the json module to parse the data sent by the client which is in string to a dictionary

        Args:
            text_data (str): The raw stringified JSON sent by the client
            send_error (bool, optional): If parsing fails, should an error response be sent back to the client. Defaults to True.

        Raises:
            JSONDecodeError: If parsing fails and send_error was set to false

        Returns:
            dict | None: Returns a dictionary containing the parsed JSON if it was successfull, returns None if send_error was set to true and error occurs
        """
        try:
            return json.loads(text_data)
        except json.JSONDecodeError as e:
            if send_error:
                await self.send(
                    json.dumps({"error": "Invalid JSON data format", "detail": str(e)})
                )
            else:
                raise e

    async def process_message_for_client(self, data: dict) -> bool:
        """
        This function processes and handles the message and broadcasts it to the recipient based on the payload

        Args:
            data (dict): The message payload to process

        Returns:
            bool: True, if message was successfully processed
        """
        message_serializer = ChatMessageSerializer(data=data)

        if not await sync_to_async(message_serializer.is_valid)():
            await self.send(json.dumps(message_serializer.errors))
            return False
        else:
            try:
                await self.save_chat_message_serializer(message_serializer)
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
                return True
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
                return False

    async def process_message_for_server(self, data: dict) -> bool:
        """This function processes messages that was sent specifically to the server which in turn

        Args:
            data (dict): The data to be proccessed

        Raises:
            KeyError: If intent is not present in data

        Returns:
            bool: Returns true if intent was successfully worked on. false, if something went wrong
        """
        # I purposely accessed intent this way to cause an error if it's not present.
        # It has to be there if the server is the recipient of the message
        if "intent" not in data:
            raise KeyError("Intent has to be present in data")
        intent = data["intent"]
        body = data.get("intent-message")
        if intent == "fetch-all-my-messages-from-timestamp":
            pass
        elif intent == "fetch-all-my-messages":
            pass

    async def receive(self, text_data: str) -> None:
        """Event Listener on user message send

        Args:
            text_data: Payload sent to the connection
        """
        # create a feature for users to be able to retrieve last messages partially based on timestamp, or fully(all messages of the user)
        user = await self.check_user_is_authenticated()

        data = await self.parse_message(text_data=text_data)
        # Attaches User ID to data to depict as the sender
        data["sender_id"] = user.id

        if data["recipient_room_id"] == "server":
            await self.process_message_for_server(data)
        else:
            await self.process_message_for_client(data=data)

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
