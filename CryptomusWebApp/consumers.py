from channels.generic.websocket import AsyncWebsocketConsumer
import json

class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "quiz"

        if not hasattr(self.channel_layer, "group_add"):
            print("❌ Ошибка: `channel_layer` не настроен!")
            return

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def start_quiz(self, event):
        await self.send(text_data=json.dumps({
            "type": "start_quiz",
            "message": "Квиз начат!",
        }))

    async def quiz_update(self, event):
        await self.send(json.dumps({
            "type": "quiz_update",
            "question": event["question"],
            "remaining_time": event["remaining_time"]
        }))

    async def quiz_end(self, event):
        await self.send(json.dumps({
            "type": "quiz_end",
            "message": event["message"]
        }))
