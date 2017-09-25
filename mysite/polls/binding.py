from channels.binding.websockets import WebsocketBinding
from .models import Question


class QuestionBinding(WebsocketBinding):
    model = Question
    stream = "question"
    fields = ["question_text", "pub_date", "archived", "created", "id"]

    @classmethod
    def group_names(cls, instance):
        return ["management-binding"]
