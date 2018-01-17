import html

from channels.test import ChannelTestCase, WSClient
from django.test import TestCase
from django.urls import reverse

from .models import (
    get_available_pack_names,
    Category,
    Fortune,
    UnavailablePackError,
    PackAlreadyLoadedError,
    CategoryAlreadyUnloadedError)
from .views import fortune_normal, load_fortune_packs


def create_sample_category_and_fortune(cat='cat', text='Meow!'):
    """
    Creates a sample category and a sample fortune for that category.
    """
    category = Category.objects.create(category=cat)
    fortune = Fortune.objects.create(text=text, category=category)
    return category, fortune


class CategoryModelTests(TestCase):
    """
    Contains tests for Category model.
    """

    def test_load_with_nonexistent_pack(self):
        """
        Function load raises UnavailablePackError for nonexistent packs.
        """
        self.assertRaises(UnavailablePackError, Category.load, '')

    def test_load_with_unknown_pack(self):
        """
        Function load raises UnavailablePackError for unknown packs.
        """
        self.assertRaises(UnavailablePackError, Category.load, 'UNKNOWN_PACK')

    def test_load_with_already_loaded_pack(self):
        """
        Function load raises PackAlreadyLoadedError for already loaded packs.
        """
        category = create_sample_category_and_fortune()[0]
        self.assertRaises(
            PackAlreadyLoadedError,
            Category.load,
            category.category)

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
        self.assertEqual(
            list(
                Category.objects.filter(
                    category=category.category)),
            [])
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
        fortune = create_sample_category_and_fortune()[1]
        self.assertEqual(Fortune.fortune(), fortune.text)

    def test_fortune_with_unavailable_category(self):
        """
        Function fortune returns the text of an existing, random fortune of an
        existing category (can be any existing category).
        """
        category = create_sample_category_and_fortune()[0]
        fortune = Fortune.fortune('dog')
        fortune_obj = Fortune.objects.get(text=fortune)
        self.assertNotEqual(fortune_obj.category.category, 'dog')
        self.assertEqual(fortune_obj.category.category, category.category)

    def test_fortune_with_available_category(self):
        """
        Function fortune returns the text of an existing, random fortune of the
        given category.
        """
        create_sample_category_and_fortune()
        create_sample_category_and_fortune(cat='dog', text='Woof!')
        fortune = Fortune.fortune('dog')
        fortune_obj = Fortune.objects.get(text=fortune)
        self.assertEqual(fortune_obj.category.category, 'dog')


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
        fortune = create_sample_category_and_fortune()[1]
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
        fake_request = ''
        response = fortune_normal(fake_request)
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
        fake_request = ''
        response = fortune_normal(fake_request)
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
        remaining_packs = list(get_available_pack_names())
        self.assertEqual(remaining_packs, [])
        fake_request = ''
        response = fortune_normal(fake_request)
        categories = [pack.category.lower() for pack in Category.objects.all()]
        self.assertEqual(categories, packs)
        fortune = get_fortune_from_response(response)
        self.assertIs(type(Fortune.objects.get(text=fortune)), Fortune)


class FortuneWebsocketTests(ChannelTestCase):
    """
    Contains tests for fortune_websocket view.
    """

    def test_no_packs_loaded(self):
        """
        If no pack got loaded yet, then visiting the page will cause loading all
        packs in the background through running load_fortune_packs as thread.
        For every created category, a message containing the category's ID will
        be sent to the fortune-ws channels group.
        """
        packs = list(get_available_pack_names())
        client = WSClient()
        client.join_group('fortune-ws')
        load_fortune_packs()
        # See if all packs got loaded.
        self.assertEqual(Category.objects.count(), len(packs))
        # See if client received messages for created categories.
        result = client.receive()
        id_of_created_category = result['payload']['pk']
        self.assertIs(
            type(
                Category.objects.get(
                    pk=id_of_created_category)),
            Category)

    def test_some_packs_loaded(self):
        """
        If just some packs are loaded, then visiting the page will cause loading
        all remaining packs in the background through running load_fortune_packs
        as thread. For every created category, a message containing the ID of
        that category will be sent to the fortune-ws channels group.
        """
        packs = list(get_available_pack_names())
        Category.load(packs[0])
        client = WSClient()
        client.join_group('fortune-ws')
        load_fortune_packs()
        # See if all remaining packs got loaded.
        self.assertEqual(Category.objects.count(), len(packs))
        # See if client received messages for created categories.
        result = client.receive()
        id_of_created_category = result['payload']['pk']
        self.assertIs(
            type(
                Category.objects.get(
                    pk=id_of_created_category)),
            Category)

    def test_all_packs_loaded(self):
        """
        If all packs are loaded, then visiting the page won't cause loading any
        packs through running load_fortune_packs as thread. Therefore, no message
        will be sent to the fortune-ws channels group.
        """
        packs = list(get_available_pack_names())
        for pack in packs:
            Category.load(pack)
        self.assertEqual(Category.objects.count(), len(packs))
        client = WSClient()
        client.join_group('fortune-ws')
        load_fortune_packs()
        # See if the number of Category objects stays the same.
        self.assertEqual(Category.objects.count(), len(packs))
        # See if client received messages.
        self.assertIsNone(client.receive())
