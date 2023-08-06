import re


def index(r):

    return {"test": "testss"}, r


def hehe(r):
    return {}, r


def about(request):
    context = {
        "about_us": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce magna nulla, sagittis eu tincidunt dictum, gravida ut libero. Cras dictum imperdiet velit maximus fringilla. Pellentesque eleifend nunc nunc, a sollicitudin neque pharetra ac. Sed vitae nisi tellus. Cras hendrerit dolor sed leo accumsan pulvinar. Sed nec ante eget urna auctor tristique vitae id lacus. Nulla dolor odio, scelerisque nec neque quis, sagittis tempor felis. Nunc sit amet arcu ipsum. Mauris hendrerit a ligula sed blandit. Morbi eleifend tincidunt sem, vitae ultricies nulla varius ac. In blandit velit luctus nisl porta ornare. Vivamus ac purus a ante rutrum dictum id id. ",
        "mission": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Fusce magna nulla, sagittis eu tincidunt dictum, gravida ut libero. Cras dictum imperdiet velit maximus fringilla. Pellentesque eleifend nunc nunc, a sollicitudin neque pharetra ac. Sed vitae nisi tellus. Cras hendrerit dolor sed leo accumsan pulvinar. Sed nec ante eget urna auctor tristique vitae id lacus. Nulla dolor odio, scelerisque nec neque quis, sagittis tempor felis. Nunc sit amet arcu ipsum. Mauris hendrerit a ligula sed blandit. Morbi eleifend tincidunt sem, vitae ultricies nulla varius ac. In blandit velit luctus nisl porta ornare. Vivamus ac purus a ante rutrum dictum id id. "
    }
    return context, request


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


def testy(request):
    context = {}
    return context, request
