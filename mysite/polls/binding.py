from channels.binding.websockets import WebsocketBinding
from .models import Question


class QuestionBinding(WebsocketBinding):
    model = Question
    stream = "management"
    fields = ["question_text", "id"]

    @classmethod
    def group_names(cls, instance):
        return ["management-binding"]
