from django.core.management.base import BaseCommand
from contacts.models import Contact, Tag
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Clear all contacts and related data'

    def handle(self, *args, **options):
        # Delete all contacts
        Contact.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted all contacts'))
        
        # Delete all tags
        Tag.objects.all().delete()
        self.stdout.write(self.style.SUCCESS('Deleted all tags'))
        
        # Delete non-superuser users
        non_superusers = User.objects.filter(is_superuser=False)
        count = non_superusers.count()
        non_superusers.delete()
        self.stdout.write(self.style.SUCCESS(f'Deleted {count} non-superuser accounts'))
