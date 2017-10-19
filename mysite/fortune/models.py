from django.db import models


class Category (models.Model):
    """ """
    category = models.CharField(max_length=100, default="default", unique=True)

    @classmethod
    def load(cls, pack_name):
        """ load a package into a category. This function is from
        django-fortune, and I am anoid that we didnt publish ours
        """
        if pack_name.lower() not in get_available_pack_names():
            raise UnavailablePackError
        fortunes_path = get_fortunes_path()
        pack_filename = str(fortunes_path.joinpath(pack_name))
        with transaction.atomic():
            try:
                pack = cls.objects.create(name=pack_name)
            except IntegrityError:
                raise PackAlreadyLoadedError
            with open(pack_filename, 'r') as pack_file:
                fortunes = pack_file.read()
                for fortune in [f[:-1] for f in fortunes.split('\n%')]:
                    if fortune:  # No empty fortunes.
                        Fortune.objects.create(text=fortune, pack=pack)

    def unload(self):
        self.delete()


class Fortune(models.Model):
    """Fortune class to store our random fortunes"""
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="fortunes")
    text = models.TextField(primary_key=True,)

    class Meta:
        """ """
        unique_together = ('category', 'text')

    def __unicode__(self):
        return self.text

    @classmethod
    def random_fortune(cls):
        """ """
        fortune = cls.objects.order_by("?").first()
        return fortune

    @classmethod
    def fortune(cls):
        """ """
        fortune = cls.random_fortune()
        if fortune:
            return fortune.text
        else:
            return "Fortunes are not loaded, yet."
