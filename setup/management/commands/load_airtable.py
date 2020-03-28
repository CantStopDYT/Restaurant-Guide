from django.core.management.base import BaseCommand
from setup import load


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        load.load_airtable()