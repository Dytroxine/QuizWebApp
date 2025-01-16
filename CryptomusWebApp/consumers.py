from channels.generic.websocket import AsyncWebsocketConsumer
import json

class QuizConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.quiz_id = self.scope['url_route']['kwargs']['quiz_id']
        self.group_name = f"quiz_{self.quiz_id}"

        # Присоединяемся к группе
        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Покидаем группу
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def start_quiz(self, event):
        # Отправляем сообщение клиенту
        await self.send(text_data=json.dumps({
            "type": "start_quiz",
            "quiz_id": event["quiz_id"],
            "message": "Квиз начат!",
        }
        )
        )

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
