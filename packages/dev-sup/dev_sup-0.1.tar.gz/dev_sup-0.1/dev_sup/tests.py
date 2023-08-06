from django.test import TestCase
from django.core.exceptions import ValidationError
from django.db import transaction
from .validators import *
from .models import *


class ValidatorsTestCase(TestCase):
    def test_url_validation_1(self):
        self.assertRaises(ValidationError, validate_url, "test")

    def test_url_validation_2(self):
        self.assertNotRaises(ValidationError, validate_url, "/test")

    def test_url_validation_3(self):
        self.assertNotRaises(ValidationError, validate_url, "www.test.pl")

    def test_url_validation_4(self):
        self.assertNotRaises(ValidationError, validate_url, "https://test.pl")

    def test_url_validation_5(self):
        self.assertNotRaises(ValidationError, validate_url, "http://test.pl")


class LinkTestCase(TestCase):

    def test_link_url_1(self):
        link = Link(
            url="test"
        )
        try:
            link.full_clean()
        except ValidationError as e:
            self.assertTrue('url' in e.message_dict)

    def test_link_url_2(self):
        link = Link(
            url="/test"
        )
        try:
            link.full_clean()
        except ValidationError as e:
            self.assertTrue('url' not in e.message_dict)

    def test_link_url_3(self):
        link = Link(
            url="www.test.pl"
        )
        try:
            link.full_clean()
        except ValidationError as e:
            self.assertTrue('url' not in e.message_dict)

    def test_link_url_4(self):
        link = Link(
            url="https://test.com"
        )
        try:
            link.full_clean()
        except ValidationError as e:
            self.assertTrue('url' not in e.message_dict)

    def test_link_url_5(self):
        link = Link(
            url="http://test.com"
        )
        try:
            link.full_clean()
        except ValidationError as e:
            self.assertTrue('url' not in e.message_dict)


class SiteTestCase(TestCase):

    def test_site_view_name_1(self):
        site = Site(
            slug="test-slug-name"
        )
        site.save()

        self.assertTrue(site.view_name == "test_slug_name")

    def test_site_template_name_1(self):
        site = Site(
            slug="test-slug-name"
        )
        site.save()

        self.assertTrue(site.template_name == "test-slug-name.html")

    def test_site_link_1(self):
        site = Site(slug="slug")
        site.save()

        self.assertTrue(site.link is not None)

    def test_site_on_nav_bar_1(self):
        site = Site(slug="slug")
        site.save()

        self.assertTrue(site.link.on_main_navbar == False)

    def test_site_on_nav_bar_2(self):
        site = Site(slug="slug")
        site.save(on_nav_bar=True)

        self.assertTrue(site.link.on_main_navbar == True)


class StyleTestCase(TestCase):

    def test_style_one_active_1(self):
        style = Style(active=True)
        style.save()

        self.assertTrue(Style.objects.filter(active=True).count() == 1)

    def test_tyle_complementary_color_1(self):
        style = Style(primary_color="#1ecbe1")
        style.save()

        self.assertTrue(style.primary_complementary_color == "#e1341e")

    def test_tyle_complementary_color_2(self):
        style = Style(primary_color="#5134cb")
        style.save()

        self.assertTrue(style.primary_complementary_color == "#aecb34")

    def test_tyle_complementary_color_3(self):
        style = Style(primary_color="#29d67f")
        style.save()

        self.assertTrue(style.primary_complementary_color == "#d62980")

    def test_tyle_complementary_color_4(self):
        style = Style(secondary_color="#1ecbe1")
        style.save()

        self.assertTrue(style.secondary_complementary_color == "#e1341e")

    def test_tyle_complementary_color_5(self):
        style = Style(secondary_color="#5134cb")
        style.save()

        self.assertTrue(style.secondary_complementary_color == "#aecb34")

    def test_tyle_complementary_color_6(self):
        style = Style(secondary_color="#29d67f")
        style.save()

        self.assertTrue(style.secondary_complementary_color == "#d62980")
