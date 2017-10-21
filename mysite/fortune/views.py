from django.shortcuts import render

from fortune.models import Category, get_fortunes_path, get_available_pack_names, PackAlreadyLoadedError, UnavailablePackError


def index(request):
    """
    Belongs to the Fortune page which shows a quote.
    """
    trouble = ['arrested',
               'codehappy',
               'commandlinefu',
               'community',
               'firefly',
               'futurama',
               'gems',
               'joel-on-software',
               'oneliners',
               'osp_rules',
               'parksandrec',
               'paul-graham',
               'shlomif',
               'shlomif-fav'] # Those are causing UnicodeDecodeError or IntegrityError.
    packs = get_available_pack_names()
    packs = [pack for pack in packs if not pack.endswith('.dat') and not pack.endswith('.pdat')]
    packs = [pack for pack in packs if pack not in trouble]
    for pack in packs:
        print(pack)
        try:
            Category.load(pack)
        except PackAlreadyLoadedError:
            pass
        except UnavailablePackError:
            pass
    return render(request, 'fortune/index.html')
