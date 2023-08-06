from .models import NavbarElement, Style
from django.conf import settings


def navbar(request):
    # Context processor injecting active navbar elements to show on navigation bar
    nav_elems = NavbarElement.objects.filter(
        active=True, on_main_navbar=True).order_by("on_navbar_position")
    return {"nav_elems": nav_elems}


def colors(request):
    # Context processor injecting color schema from active Style element
    try:
        style = Style.objects.filter(active=True).get()

        if(style.colored_dark):
            darkmode_body_background = style.dark_body_background
            darkmode_background = style.dark_background
        else:
            darkmode_body_background = "#101010"
            darkmode_background = "#202020"

        return {
            "navbar_background": style.primary_color,
            "navbar_mainmenu_color": style.primary_complementary_color,
            "navbar_submenu_background": style.secondary_color,
            "navbar_inner_dropdown_background":  style.secondary_color,
            "navbar_inner_dropdown_foreground":  style.secondary_complementary_color,
            "link_hover": "white",
            "darkmode_body_background": darkmode_body_background,
            "darkmode_background": darkmode_background,
        }
    except:
        return{}


def google_analytics(request):
    # Context processor injecting Google Analytics tag if set in Settings.py
    tag = getattr(settings, "GOOGLE_ANALYTICS_TAG", None)

    if tag is not None:
        return {"google_tag": tag}
    return {}


def all(request):
    # All context processors
    context = {}
    context.update(navbar(request))
    context.update(colors(request))
    context.update(google_analytics(request))
    return context
