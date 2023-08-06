from django.conf.urls import url
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.query import QuerySet

from dev_sup import utils

from .fields import ColorField
from .validators import validate_color, validate_url
from django.utils.translation import gettext as _


class NavbarElement(models.Model):
    # Model of navigation bar element
    name = models.CharField(max_length=30, blank=False,
                            unique=True, verbose_name=_("name"))
    displayed_name = models.CharField(
        max_length=30, blank=False, verbose_name=_("displayed name"))
    active = models.BooleanField(default=False, verbose_name=_("active"))
    on_main_navbar = models.BooleanField(
        default=False, verbose_name=_("show on main navbar"))
    on_navbar_position = models.PositiveIntegerField(
        blank=True, null=True, verbose_name=_("position on main navbar"))

    class Meta:
        verbose_name = _('navbar element')
        verbose_name_plural = _('navbar elements')

    def __str__(self):

        if hasattr(self, 'dropdownmenu'):
            return "Menu-" + self.name
        elif hasattr(self, 'link'):
            return "Link-"+self.name
        else:
            return self.name


class Link(NavbarElement):
    # Model of link navigation bar element
    url = models.CharField(blank=False, null=True, max_length=200, validators=[
                           validate_url], verbose_name=_("url"))

    class Meta:
        verbose_name = _('link')
        verbose_name_plural = _('links')

    def __str__(self):
        return self.name


class DropDownMenu(NavbarElement):
    # Model of drop down menu element
    item_list = models.ManyToManyField(
        "NavbarElement", related_name="navbar_elements", blank=True, verbose_name=_("items"))

    class Meta:
        verbose_name = _('drop down menu')
        verbose_name_plural = _('drop down menus')

    def __str__(self):
        return self.name

    @property
    def ordered_item_list(self):
        return self.item_list.order_by("displayed_name")


class Site(models.Model):
    # Model of site
    name = models.CharField(max_length=30, blank=False,
                            unique=True, verbose_name=_("name"))
    slug = models.SlugField(blank=False, null=True,
                            max_length=200, unique=True, verbose_name=_("slug"))
    active = models.BooleanField(default=False, verbose_name=_("active"))
    template_name = models.CharField(
        max_length=30, blank=False, unique=True, verbose_name=_("template name"))
    tracking = models.BooleanField(default=True, verbose_name=_("tracking"))
    view_name = models.CharField(max_length=60, verbose_name=_("view name"))
    custom_view = models.BooleanField(
        default=False, verbose_name=_("custom view function"))

    link = models.ForeignKey(Link, on_delete=CASCADE,
                             blank=True, null=True, verbose_name=_("link"))

    class Meta:
        verbose_name = _('site')
        verbose_name_plural = _('sites')

    def save(self, on_nav_bar=False, *args, **kwargs):
        self.view_name = self.slug.replace("-", "_")
        self.template_name = self.slug + ".html"

        if('just_save' in kwargs):
            kwargs.pop("just_save")
            self.__create_link(on_nav_bar)
            super().save(*args, **kwargs)
        else:
            if self._state.adding:
                utils.create_template(self.template_name)
                self.__create_link(on_nav_bar, *args, **kwargs)
                if self.custom_view:
                    utils.create_view_function(self.view_name)
            else:
                old_site = Site.objects.filter(pk=self.pk).get()
                super().save(*args, **kwargs)
                utils.update_template(
                    old_site.template_name, self.template_name)
                utils.update_function_name(old_site.view_name, self.view_name)

    def __create_link(self, on_nav_bar):
        link = Link(name=self.name, displayed_name=self.name, active=self.active,
                    on_main_navbar=on_nav_bar, url="/"+self.slug)
        link.save()
        self.link = link
        super().save()
        # TODO Co jak jest aktualizacja, czy zmieniać też dane linku? To trzeba by połączyć obiekty


class StyleQuerySet(QuerySet):
    # Custom query set for Style
    def update(self, *args, **kwargs):
        # Updates Style date, ensures there will be only one style with active = True
        if "active" in kwargs:
            if kwargs["active"] == True:
                Style.objects.filter(active=True).update(active=False)
        super().update(*args, **kwargs)


class Style(models.Model):
    # Site color schema model
    name = models.CharField(max_length=30, blank=False,
                            unique=True, verbose_name=_("name"))
    primary_color = ColorField(
        default="#1A5FB4", verbose_name=_("primary color"))
    secondary_color = ColorField(
        default="#99C1F1", verbose_name=_("secondary color"))

    primary_complementary_color = ColorField(
        verbose_name=_("primary complementary color"))
    secondary_complementary_color = ColorField(
        verbose_name=_("secondary complementary color"))

    dark_body_background = ColorField(verbose_name=_("dark body background"))
    dark_background = ColorField(verbose_name=_("dark background"))

    active = models.BooleanField(default=False, verbose_name=_("active"))
    colored_dark = models.BooleanField(
        default=False, help_text=_("Generates background colors for dark theme, based on primary color. If not set, generates gray background."), verbose_name=_("colored dark"))

    objects = StyleQuerySet.as_manager()

    class Meta:
        verbose_name = _('style')
        verbose_name_plural = _('styles')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Saves style to database, ensures only one there is only one style with active = True
        self.primary_complementary_color = self.__generate_complementary(
            self.primary_color)

        self.secondary_complementary_color = self.__generate_complementary(
            self.secondary_color)

        self.dark_body_background = self.__generate_darker(
            self.primary_color, 0.75)
        self.dark_background = self.__generate_darker(self.primary_color, 0.65)

        try:
            super().save(*args, **kwargs)
        except Exception as er:
            return er
        else:
            if(self.active):
                Style.objects.filter(active=True).exclude(
                    pk=self.pk).update(active=False)

    def __generate_complementary(self, primary_color):
        # Generates complementary color to given 'primary_color'
        comp_color = int("ffffff", base=16) - \
            int(primary_color.replace("#", ""), base=16)
        hex_color = "{0:#0{1}x}".format(comp_color, 8)

        return "#"+hex_color[2:]

    def __generate_darker(self, color, how_much):
        def darken(chanel, how_much):
            val = int(chanel, 16)
            return (int(val-(val*how_much)))

        r = darken(color[1:3], how_much)
        g = darken(color[3:5], how_much)
        b = darken(color[5:7], how_much)

        r1 = "{0:#0{1}x}".format(r, 4)[2:4]
        g1 = "{0:#0{1}x}".format(g, 4)[2:4]
        b1 = "{0:#0{1}x}".format(b, 4)[2:4]

        return "#{}{}{}".format(r1, g1, b1)
