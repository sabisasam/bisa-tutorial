import os
import random
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
    Returns the path to the fortunes data packs.
    """
    app_config = apps.get_app_config("fortune")
    return Path(os.sep.join([app_config.path, "cookies"]))


def get_available_pack_names():
    """
    Returns a list of (lower-cased) names of available (unloaded) packs.
    """
    installed_pack_names = [pack.category.lower()
                            for pack in Category.objects.all()]
    fortunes_path = get_fortunes_path()
    for path in fortunes_path.iterdir():
        if path.is_dir():
            pass
        elif path.suffix == ".dat":
            pass
        elif path.suffix == ".pdat":
            pass
        elif path.name.lower() in installed_pack_names:
            pass
        else:
            yield path.name.lower()


class PackAlreadyLoadedError(Exception):
    pass


class CategoryAlreadyUnloadedError(Exception):
    pass


class UnavailablePackError(Exception):
    pass


class Category(models.Model):
    """
    Category class to store our fortune categories.
    """
    category = models.CharField(max_length=100, default="default", unique=True)

    @classmethod
    def load(cls, pack_name):
        """
        Creates category with given pack name and loads fortunes of that
        pack into Fortune. This function is from django-fortune.
        """
        if pack_name.lower() in [pack.category.lower()
                                 for pack in Category.objects.all()]:
            raise PackAlreadyLoadedError
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
                for fortune in fortunes.split('\n%\n'):
                    if fortune:  # No empty fortunes.
                        Fortune.objects.create(text=fortune, category=pack)

    def unload(self):
        try:
            self.delete()
        except AssertionError:
            raise CategoryAlreadyUnloadedError

    def __str__(self):
        return self.category


class Fortune(models.Model):
    """
    Fortune class to store our fortunes.
    """
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="fortunes")
    text = models.TextField(unique=True)

    class Meta:
        """ """
        unique_together = ('category', 'text')

    def __unicode__(self):
        return self.text

    @classmethod
    def fortune(cls, category=''):
        """
        Returns a random fortune. If an existing category is given, the
        fortune will be of that category.
        """
        installed_pack_names = [pack.category.lower()
                                for pack in Category.objects.all()]

        if category.lower() in installed_pack_names:
            category_obj = Category.objects.get(category=category.lower())
            fortune_ids = cls.objects.filter(
                category=category_obj).values_list(
                'id', flat=True)
        else:
            fortune_ids = cls.objects.values_list('id', flat=True)

        if fortune_ids.exists():
            random_id = random.sample(list(fortune_ids), 1)
            fortune = cls.objects.get(id=random_id[0])
            return fortune.text
        else:
            return "Fortunes are not loaded, yet."
