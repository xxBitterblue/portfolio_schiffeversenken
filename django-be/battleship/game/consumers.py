import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class GameConsumer(WebsocketConsumer):
    def connect(self):
        self.game_name = self.scope['url_route']['kwargs']['game_id']
        self.game_group_name = 'game_%s' % self.game_name

        # Join room group
        async_to_sync(self.channel_layer.group_add)(
            self.game_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        # Leave room group
        async_to_sync(self.channel_layer.group_discard)(
            self.game_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Send message to room group
        async_to_sync(self.channel_layer.group_send)(
            self.game_group_name,
            {
                'type': message,
                'message': message
            }
        )

    # Receive message from room group
    def start_game(self, event):
        message = event['content']

        # Send message to WebSocket
        self.send(text_data=json.dumps({
            'type': 'start_game',
            'message': message
        }))

    def attack_evaluation(self, event):
        message = event['content']

        self.send(text_data=json.dumps({
            'type': 'attack_evaluation',
            'message': message
        }))

    def launch_game(self, event):
        message = event['content']

        self.send(text_data=json.dumps({
            'type': 'launch_game',
            'message': message
        }))

    def score_changed(self, event):
        message = event['content']

        self.send(text_data=json.dumps({
            'type': 'score_changed',
            'message': message
        }))

    def game_finished(self, event):
        message = event['content']

        self.send(text_data=json.dumps({
            'type': 'game_finished',
            'message': message
        }))
