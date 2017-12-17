import html

from django.test import TestCase
from django.urls import reverse

from .models import (get_available_pack_names, Category, Fortune, UnavailablePackError,
                     PackAlreadyLoadedError, CategoryAlreadyUnloadedError)


def create_sample_category_and_fortune():
    category = Category.objects.create(category='cat')
    fortune = Fortune.objects.create(text='Meow!', category=category)
    return category, fortune


class CategoryModelTests(TestCase):
    """
    Contains tests for Category model.
    """

    def test_load_with_unavailable_pack(self):
        """
        Function load raises UnavailablePackError for nonexistent packs.
        """
        self.assertRaises(UnavailablePackError, Category.load, '')

    def test_load_with_already_loaded_pack(self):
        """
        Function load raises PackAlreadyLoadedError for already loaded packs.
        """
        category = create_sample_category_and_fortune()[0]
        self.assertRaises(PackAlreadyLoadedError, Category.load, category.category)

    def test_load_with_not_yet_loaded_pack(self):
        """
        Function load creates a Category object with the pack's name as category
        and a Fortune object for each fortune contained in the given pack.
        """
        packs = list(get_available_pack_names())
        Category.load(packs[0])
        category = Category.objects.get(category=packs[0])
        self.assertIs(type(category), Category)
        fortune = Fortune.objects.filter(category=category).first()
        self.assertIs(type(fortune), Fortune)

    def test_unload_with_already_deleted_category(self):
        """
        Function unload raises CategoryAlreadyUnloadedError for already deleted
        categories.
        """
        category = create_sample_category_and_fortune()[0]
        category.unload()
        self.assertRaises(CategoryAlreadyUnloadedError, category.unload)

    def test_unload_with_not_yet_deleted_category(self):
        """
        Function unload causes deletion of the Category object as well as all the
        Fortune objects related to that category.
        """
        category = create_sample_category_and_fortune()[0]
        category.unload()
        self.assertEqual(list(Category.objects.filter(category=category.category)), [])
        self.assertEqual(list(Fortune.objects.filter(category=category)), [])


class FortuneModelTests(TestCase):
    """
    Contains tests for Fortune model.
    """

    def test_fortune_with_no_existing_fortune(self):
        """
        Function fortune returns "Fortunes are not loaded, yet." if there is no
        existing fortune.
        """
        fortune = Fortune.fortune()
        self.assertEqual(fortune, "Fortunes are not loaded, yet.")

    def test_fortune_with_existing_fortune(self):
        """
        Function fortune returns the text of an existing, random fortune.
        """
        create_sample_category_and_fortune()
        self.assertEqual(Fortune.fortune(), 'Meow!')

    def test_fortune_with_unavailable_category(self):
        """
        Function fortune returns the text of an existing, random fortune of no
        specific category (can be any category).
        """
        category = create_sample_category_and_fortune()[0]
        fortune = Fortune.fortune('dog')
        fortune_obj = Fortune.objects.get(text=fortune)
        self.assertNotEqual(fortune_obj.category.category, 'dog')

    def test_fortune_with_available_category(self):
        """
        Function fortune returns the text of an existing, random fortune of the
        given category.
        """
        category = create_sample_category_and_fortune()[0]
        fortune = Fortune.fortune('dog')
        fortune_obj = Fortune.objects.get(text=fortune)
        self.assertNotEqual(fortune_obj.category.category, 'dog')


def get_fortune_from_response(response):
    """
    Returns the fortune which is contained in the given response. This function
    uses the fact that fortunes are within a HTML pre tag.
    """
    content = response.content.decode('utf-8')
    index_start = content.find('<pre>') + len('<pre>')
    index_end = content.find('</pre>')
    fortune = content[index_start:index_end]
    fortune = html.unescape(fortune)
    return fortune


class FortuneIndexViewTests(TestCase):
    """
    Contains tests for index view.
    """

    def test_no_existing_fortune(self):
        """
        If no fortune exists, an appropriate message is displayed.
        """
        response = self.client.get(reverse('fortune:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Fortunes are not loaded, yet.")

    def test_existing_fortune(self):
        """
        An existing fortune is displayed on the index page.
        """
        category, fortune = create_sample_category_and_fortune()
        response = self.client.get(reverse('fortune:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, fortune.text)


class FortuneNormalViewTests(TestCase):
    """
    Contains tests for fortune_normal view.
    """

    def test_no_packs_loaded(self):
        """
        If all packs aren't loaded yet, then loading the page will cause loading
        all packs. After that, an existing fortune will be displayed.
        """
        packs = list(get_available_pack_names())
        response = self.client.get(reverse('fortune:fortune-normal'))
        categories = [pack.category.lower() for pack in Category.objects.all()]
        self.assertEqual(categories, packs)
        packs = list(get_available_pack_names())
        self.assertEqual(packs, [])
        fortune = get_fortune_from_response(response)
        self.assertIs(type(Fortune.objects.get(text=fortune)), Fortune)

    def test_some_packs_loaded(self):
        """
        If just some packs are loaded, then loading the page will cause loading
        all not yet loaded packs. Then, an existing fortune will be displayed.
        """
        packs = list(get_available_pack_names())
        Category.load(packs[0])
        response = self.client.get(reverse('fortune:fortune-normal'))
        categories = [pack.category.lower() for pack in Category.objects.all()]
        self.assertEqual(categories, packs)
        packs = list(get_available_pack_names())
        self.assertEqual(packs, [])
        fortune = get_fortune_from_response(response)
        self.assertIs(type(Fortune.objects.get(text=fortune)), Fortune)

    def test_all_packs_loaded(self):
        """
        If all packs are loaded, then loading the page won't load any packs. An
        existing, random fortune will be displayed.
        """
        packs = list(get_available_pack_names())
        for pack in packs:
            Category.load(pack)
        response = self.client.get(reverse('fortune:fortune-normal'))
        categories = [pack.category.lower() for pack in Category.objects.all()]
        self.assertEqual(categories, packs)
        fortune = get_fortune_from_response(response)
        self.assertIs(type(Fortune.objects.get(text=fortune)), Fortune)


class FortuneWebsocketTests(TestCase):
    """
    Contains tests for fortune_websocket view.
    """

    def test_no_packs_loaded(self):
        """
        If all packs aren't loaded yet, then visiting the page will cause loading
        all packs in the background. Meanwhile the message "Fortunes are not
        loaded, yet." is displayed on the page. After all packs are loaded, the
        message will be replaced by an existing fortune.
        """

    def test_some_packs_loaded(self):
        """
        If just some packs are loaded, then visiting the page will cause loading
        all not yet loaded packs in the background. The page will display an
        existing fortune while loading those packs and won't change it after
        finishing loading.
        """

    def test_all_packs_loaded(self):
        """
        If all packs are loaded, then visiting the page won't cause loading any
        packs. An existing, random fortune will be displayed.
        """


class FortuneRabbitmqTests(TestCase):
    """
    Contains tests for fortune_rabbitmq view.
    """
