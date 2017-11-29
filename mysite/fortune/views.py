import threading

from django.shortcuts import render

from .models import Category, get_available_pack_names, get_fortunes_path, PackAlreadyLoadedError, UnavailablePackError


def index(request):
    """
    Belongs to "Fortune Page - Overview" which lists links to
    different versions of the Fortune Page.
    """
    return render(request, 'fortune/index.html')


def load_fortune_packs():
    packs = get_available_pack_names()
    packs = [pack for pack in packs if not pack.endswith('.dat') and not pack.endswith('.pdat')]
    for pack in packs:
        try:
            Category.load(pack)
        except PackAlreadyLoadedError:
            pass
        except UnavailablePackError:
            pass


def fortune_normal(request):
    """
    Belongs to "Fortune Page - Normal" which shows a quote, a
    saying or something similar.
    """
    load_fortune_packs()
    return render(request, 'fortune/fortune.normal.html')


class LoadFortunePacksThread(threading.Thread):
    def run(self):
        load_fortune_packs()


def fortune_websocket(request):
    """
    Belongs to "Fortune Page - Websocket" which shows a quote,
    a saying or something similar and works with websockets.
    """
    LoadFortunePacksThread().start()
    num_packs = 0
    fortune_path = get_fortunes_path()
    for pack_path in fortune_path.iterdir():
        if not str(pack_path).endswith('.dat') and not str(pack_path).endswith('.pdat'):
            num_packs += 1
    return render(request, 'fortune/fortune.websocket.html', {'num_packs': num_packs})


def fortune_rabbitmq(request):
    """
    Belongs to "Fortune Page - RabbitMQ" which can get and
    show a fortune that was sent by a client.
    """
    return render(request, 'fortune/fortune.rabbitmq.html')
