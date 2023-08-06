from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Site


@receiver(post_delete, sender=Site)
def item_list_changed(sender, instance, **kwargs):
    # Deleting link connected to Site, on Site deleting
    try:
        link = instance.link
        if(link is not None):
            link.delete()
    except:
        print("Trying to delete link, but it's NoneType")
