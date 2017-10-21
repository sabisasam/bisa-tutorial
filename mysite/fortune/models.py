import os
import sys

from django.apps import apps
from django.db import models, transaction
from django.db.utils import IntegrityError

if sys.version_info[0] == 2:
    from pathlib2 import Path
else:
    from pathlib import Path


def get_fortunes_path():
    """
    Return the path to the fortunes data packs.
    """
    app_config = apps.get_app_config("fortune")
    return Path(os.sep.join([app_config.path, "cookies"]))


def get_available_pack_names():
    """
    Return a list of (lower-cased) names if available (unloaded) packs.
    """
    installed_pack_names = [pack.category.lower() for pack in Category.objects.all()]
    fortunes_path = get_fortunes_path()
    for path in fortunes_path.iterdir():
        if path.is_dir():
            pass
        elif path.suffix == ".dat":
            pass
        elif path.name.lower() in installed_pack_names:
            pass
        else:
            yield path.name.lower()


class PackAlreadyLoadedError(Exception):
    pass


class UnavailablePackError(Exception):
    pass


class Category(models.Model):
    """ """
    category = models.CharField(max_length=100, default="default", unique=True)

    @classmethod
    def load(cls, pack_name):
        """
        Load a package into a category. This function is from django-fortune.
        """
        if pack_name.lower() not in get_available_pack_names():
            raise UnavailablePackError
        fortunes_path = get_fortunes_path()
        pack_filename = str(fortunes_path.joinpath(pack_name))
        with transaction.atomic():
            try:
                pack = cls.objects.create(category=pack_name)
            except IntegrityError:
                raise PackAlreadyLoadedError
            with open(pack_filename, 'r') as pack_file:
                fortunes = pack_file.read()
                for fortune in [f[:-1] for f in fortunes.split('\n%')]:
                    if fortune:  # No empty fortunes.
                        Fortune.objects.create(text=fortune, category=pack)

    def unload(self):
        self.delete()


class Fortune(models.Model):
    """
    Fortune class to store our random fortunes.
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="fortunes")
    text = models.TextField(primary_key=True)

    class Meta:
        """ """
        unique_together = ('category', 'text')

    def __unicode__(self):
        return self.text

    @classmethod
    def fortune(cls):
        """ """
        fortune = cls.objects.order_by("?").first()
        if fortune:
            return fortune.text
        else:
            return "Fortunes are not loaded, yet."
