from django.core.management.base import BaseCommand, CommandError
from dev_sup.models import *
from django.db.utils import IntegrityError
from dev_sup import utils


class Command(BaseCommand):
    help = 'Generates base project'

    def handle(self, *args, **options):
        about = None
        contact = None
        home_link = None
        style = None

        try:
            about = Site(name="About", slug="about", active=True,
                         tracking=False, custom_view=True)
            about.save(on_nav_bar=True, just_save=True)
            utils.create_template("about.html", "about.html")
            utils.create_view_function("about")
        except Exception as err:
            self.stdout.write(self.style.ERROR(
                "Unable to create 'About' page."))
            self.stderr.write(self.style.ERROR(
                err
            ))
            return

        try:
            contact = Site(name="Contact", slug="contact",
                           active=True, tracking=False, custom_view=True)
            contact.save(on_nav_bar=True, just_save=True)

            utils.create_template("contact.html", "contact.html")
            utils.create_view_function("contact")
        except Exception as err:
            about.delete()
            self.stdout.write(self.style.ERROR(
                "Unable to create 'Contact' page."))
            self.stderr.write(self.style.ERROR(
                err
            ))
            return

        try:
            Style(name="Default", active=True).save()
        except IntegrityError:
            pass
        except Exception as err:
            about.delete()
            contact.delete()
            self.stdout.write(self.style.ERROR(
                "Unable to create 'Default' style."))
            self.stderr.write(self.style.ERROR(
                err
            ))
            return

        try:
            home_link = Link(name="Home", displayed_name="Home", active=True,
                             on_main_navbar=True, url="/", on_navbar_position=0)
            home_link.save()

        except Exception as err:
            about.delete()
            contact.delete()
            style.delete()
            self.stdout.write(self.style.ERROR(
                "Unable to create 'Home' link."))
            self.stderr.write(self.style.ERROR(
                err
            ))
            return

        about.link.on_navbar_position = 1
        about.link.save()
        contact.link.on_navbar_position = 2
        contact.link.save()

        self.stdout.write(self.style.SUCCESS(
            'Successfully generated base site project'))
