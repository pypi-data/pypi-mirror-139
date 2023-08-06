from django.http import HttpResponse
from django.template import loader, TemplateDoesNotExist
from .models import *
from django.shortcuts import get_object_or_404, redirect, render
import importlib.util
from django.conf import settings
from os import path
import sys


def index(request):
    # Index view
    try:
        template = loader.get_template(
            'generated/index.html')

        context, request = _exec_custom_view_function(request, "index")

        return HttpResponse(template.render(context, request))
    except TemplateDoesNotExist:
        template = loader.get_template('dev_sup/index.html')
        return HttpResponse(template.render({"site_tracking": True}, request))


def site(request, slug):
    # Displays site from Site model with matching 'slug'
    if slug == "admin":
        return redirect("/admin")

    site = get_object_or_404(Site, active=True, slug=slug)
    context = {}

    if site.custom_view:
        context, request = _exec_custom_view_function(request, site.view_name)

    try:
        template = loader.get_template(
            'generated/'+site.template_name)

        context.update({
            "site_tracking": site.tracking,
            "site_name": site.name
        })

        HttpResponse(template.render(context, request))

        return HttpResponse(template.render(context, request))
    except TemplateDoesNotExist:
        print("Template nie istnieje")


def _exec_custom_view_function(request, view_name):
    # Runs custom view function
    spec = importlib.util.spec_from_file_location(
        "dev_views", path.join(settings.BASE_DIR, "dev_sup/dev_views.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    res = getattr(module, view_name)
    try:
        context, request = res(request)
    except TypeError:
        raise TypeError(
            "Function '{}' must return context dictionary and request.".format(view_name))
    except ValueError:
        raise ValueError(
            "Function '{}' must return context dictionary and request.".format(view_name))

    return context, request


def handler400(request):
    # View of 400 error
    response = render(request, '400.html')
    response.status_code = 400
    return response


def handler403(request):
    # View of 403 error
    response = render(request, '403.html')
    response.status_code = 403
    return response


def handler404(request):
    # View of 404 error
    response = render(request, '404.html')
    response.status_code = 404
    return response


def handler500(request):
    # View of 500 error
    response = render(request, '500.html')
    response.status_code = 500
    return response
