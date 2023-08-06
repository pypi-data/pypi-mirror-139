from django.contrib import admin
from .models import *
from django import forms
from django.core.validators import ValidationError
from os import path, makedirs
from .utils import find_template
from django.contrib import messages
from django.utils.translation import gettext as _


@admin.action(description=_('Deactivate all selected links'))
def deactivate(modeladmin, request, queryset):
    # Admin action for deactivating selected elements
    queryset.update(active=False)


@admin.action(description=_('Activate all selected links'))
def activate(modeladmin, request, queryset):
    # Admin action activating selected elements
    queryset.update(active=True)


@admin.action(description=_('Activate selected style'))
def activate_style(modeladmin, request, queryset):
    # Admin action activating selected style - ONLY ONE
    if(len(queryset) == 1):
        queryset.update(active=True)
    else:
        messages.error(request, _("Select only ONE style."))


@admin.action(description=_('Show all selected links on navbar'))
def show_on_nav_bar(modeladmin, request, queryset):
    # Admin action showing selected elements on navigation bar
    queryset.update(on_main_navbar=True)


@admin.action(description=_('Hide all selected links on navbar'))
def hide_on_nav_bar(modeladmin, request, queryset):
    # Admin action hiding selected elements on navigation bar
    queryset.update(on_main_navbar=False)


@admin.action(description=_('Enable tracking'))
def enable_tracking(modeladmin, request, queryset):
    # Admin action enabling tracking in selected Elements
    queryset.update(tracking=True)


@admin.action(description=_('Disable tracking'))
def disable_tracking(modeladmin, request, queryset):
    # Admin action disabling tracking in selected Elements
    queryset.update(tracking=False)


class DropDownMenuForm(forms.ModelForm):
    # Form for creating and editing Drop Down menu in Django Admin
    class Meta:
        model = DropDownMenu
        fields = ("name", "displayed_name", "active", "on_main_navbar",
                  "on_navbar_position", "item_list")

    def clean(self, *args, **kwargs):
        # Cleans data from form
        cleaned_data = super().clean()

        name = cleaned_data['name']
        to_remove = []
        for ne in cleaned_data['item_list']:
            if hasattr(ne, 'dropdownmenu'):
                if ne.name == name:
                    to_remove.append(ne)
                else:
                    conflicting_item = self._check_item_list(ne, name)
                    if conflicting_item:
                        to_remove.append(ne)
        if to_remove:
            raise ValidationError(
                "Conflicting dropdown menus - {}.".format(", ".join([str(i) for i in to_remove])))

    def _check_item_list(self, parent, name):
        # Checks item list for endless recursive loops.
        item_list = parent.dropdownmenu.item_list.all()
        for item in item_list:
            if hasattr(item, 'dropdownmenu'):
                if item.name == name:
                    return True
                if self._check_item_list(item, name):
                    return True
        return False


@admin.register(DropDownMenu)
class DropDownMenuAdmin(admin.ModelAdmin):
    # DropDownMenu model used in Django Admin panel
    filter_horizontal = ('item_list',)
    list_display = ('name', 'displayed_name', 'active',
                    'on_main_navbar', 'on_navbar_position')
    ordering = ('on_navbar_position', 'name')
    actions = [activate, deactivate, show_on_nav_bar, hide_on_nav_bar]

    form = DropDownMenuForm

    def get_form(self, request, *args, **kwargs):
        # Returns DropDownMenuAdmin form
        form = super(DropDownMenuAdmin, self).get_form(
            request, *args, **kwargs)
        return form


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    # Link model used in Django Admin panel
    list_display = ('name', 'displayed_name', 'active',
                    'on_main_navbar', 'on_navbar_position')
    ordering = ('on_navbar_position', 'name')

    actions = [activate, deactivate, show_on_nav_bar, hide_on_nav_bar]


@admin.register(Site)
class SiteAdmin(admin.ModelAdmin):
    # Site model used in Django Admin panel
    list_display = ("name", "active", "tracking")

    fields = ("name", "slug", "active", "tracking", "custom_view")

    ordering = ("name",)

    actions = [activate, deactivate, enable_tracking, disable_tracking]

    list_filter = ["active", "tracking"]


@admin.register(Style)
class StyleAdmin(admin.ModelAdmin):
    # Style model used in Django Admin panel
    ordering = ("name",)

    fields = ("name", "primary_color", "secondary_color",
              "active", "colored_dark")
    list_display = ("name", "active")
    ordering = ("-active", "name")
    actions = (activate_style,)
