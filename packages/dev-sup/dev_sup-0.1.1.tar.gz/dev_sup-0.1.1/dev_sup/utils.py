import sys
from os import path

from os import path, makedirs
from django.conf import settings
import shutil

base_path = "dev_sup/templates/dev_sup/templates"

__function_texts = {
    "--default": """
def {}(request):
    context = {{}}
    return context, request

""",
    "about": """
def about(request):
    context = {
        "about_us": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce magna nulla, sagittis eu tincidunt dictum, gravida ut libero. Cras dictum imperdiet velit maximus fringilla. Pellentesque eleifend nunc nunc, a sollicitudin neque pharetra ac. Sed vitae nisi tellus. Cras hendrerit dolor sed leo accumsan pulvinar. Sed nec ante eget urna auctor tristique vitae id lacus. Nulla dolor odio, scelerisque nec neque quis, sagittis tempor felis. Nunc sit amet arcu ipsum. Mauris hendrerit a ligula sed blandit. Morbi eleifend tincidunt sem, vitae ultricies nulla varius ac. In blandit velit luctus nisl porta ornare. Vivamus ac purus a ante rutrum dictum id id. ",
        "mission": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce magna nulla, sagittis eu tincidunt dictum, gravida ut libero. Cras dictum imperdiet velit maximus fringilla. Pellentesque eleifend nunc nunc, a sollicitudin neque pharetra ac. Sed vitae nisi tellus. Cras hendrerit dolor sed leo accumsan pulvinar. Sed nec ante eget urna auctor tristique vitae id lacus. Nulla dolor odio, scelerisque nec neque quis, sagittis tempor felis. Nunc sit amet arcu ipsum. Mauris hendrerit a ligula sed blandit. Morbi eleifend tincidunt sem, vitae ultricies nulla varius ac. In blandit velit luctus nisl porta ornare. Vivamus ac purus a ante rutrum dictum id id. "
    }
    return context, request

""",
    "contact": """
def contact(request):
    context = {
        'phone': '123456789',
        'mail': 'example@dev_sup.com',
        'address': {
            "street": "Street",
            "number": "12",
            "city": "City",
            "zip": "00-000",
            "country": "Country"
        }
    }
    return context, request

"""
}


def find_template(name):
    # Finds template file with file named 'name'
    for dir_path in sys.path:
        location = path.join(dir_path, base_path, name)
        if path.exists(location):
            return location


def create_template(template_name, source_template="empty.html"):
    # Creates template file as copy of 'source_file'
    source = find_template(source_template)

    destaination = path.join(
        settings.BASE_DIR, "dev_sup/templates/generated/")
    if not path.exists(destaination):
        makedirs(destaination)
    if path.exists(destaination):
        dest_file = path.join(destaination, template_name)
        shutil.copyfile(source, dest_file)
    else:
        raise Exception(
            "Direcory 'template/genereated' does not exist and is impossible to crete")


def update_template(old_template_name, new_template_name):
    # Updates template file's name
    source = path.join(
        settings.BASE_DIR, "dev_sup/templates/generated/", old_template_name)

    destaination = path.join(
        settings.BASE_DIR, "dev_sup/templates/generated/", new_template_name)
    shutil.move(source, destaination)


def update_function_name(old_func_name, new_func_name):
    # Updates view function's name
    views_dir = path.join(
        settings.BASE_DIR, "dev_sup/")

    if not path.exists(views_dir):
        raise Exception(
            "Direcory 'dev_sup/dev_views.py' does not exist")
    else:
        view_file_path = path.join(views_dir, "dev_views.py")
        with open(view_file_path, "r") as view_file:
            all_lines = view_file.read()

        all_lines = all_lines.replace("def {}".format(old_func_name),
                                      "def {}".format(new_func_name))

        with open(view_file_path, "w") as view_file:
            view_file.write(all_lines)


def create_view_function(function_name):
    # Creates view function in file with custom views
    views_dir = path.join(
        settings.BASE_DIR, "dev_sup/")
    if not path.exists(views_dir):
        makedirs(views_dir)
    if path.exists(views_dir):
        view_file_path = path.join(views_dir, "dev_views.py")
        with open(view_file_path, "a") as view_file:
            if function_name in __function_texts:
                view_file.write(__function_texts[function_name])
            else:
                view_file.write(
                    __function_texts["--default"].format(function_name))
    else:
        raise Exception(
            "Direcory 'dev_sup/dev_views.py' does not exist and is impossible to crete")
