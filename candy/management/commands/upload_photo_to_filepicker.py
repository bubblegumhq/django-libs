import logging
from optparse import make_option
from django.core.management.base import BaseCommand
from filepicker.bubpicker import FilePicker

FP = FilePicker()

LOGGER = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Load an image into filepicker and return the url'
    option_list = BaseCommand.option_list + (
        make_option('--url',
                    action='store',
                    dest='url'),
    )

    def handle(self, *args, **options):
        photo_url = options.get("url")
        try:
            photo = FP.createFilePickerFromURL(photo_url)
            print photo
        except Exception, e:
            LOGGER.error("Error trying to load image into filepicker %s" % photo_url,exc_info=1)
