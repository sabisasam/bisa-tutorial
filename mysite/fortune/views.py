from django.shortcuts import render

from fortune.models import Category, get_available_pack_names, PackAlreadyLoadedError, UnavailablePackError


def index(request):
    """
    Belongs to the Fortune page which shows a quote, a saying or something similar.
    """
    packs = get_available_pack_names()
    packs = [pack for pack in packs if not pack.endswith('.dat') and not pack.endswith('.pdat')]
    for pack in packs:
        try:
            Category.load(pack)
        except PackAlreadyLoadedError:
            pass
        except UnavailablePackError:
            pass
    return render(request, 'fortune/index.html')
