from channels.binding.websockets import WebsocketBinding
from .models import Category


class CategoryBinding(WebsocketBinding):
    model = Category
    stream = "fortune"
    fields = ["id"]

    @classmethod
    def group_names(cls, instance):
        return ["fortune-ws"]
