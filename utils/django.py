try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

import os

from django.contrib.staticfiles.finders import FileSystemFinder
from django.core.files.storage import FileSystemStorage


class AssetsFinder(FileSystemFinder):
    """Find static files installed with bower"""

    def __init__(self, apps=None, *args, **kwargs):
        self.locations = []
        self.storages = OrderedDict()

        root = self._get_bower_components_location()
        if root is not None:
            prefix = ''
            self.locations.append((prefix, root))

            filesystem_storage = FileSystemStorage(location=root)
            filesystem_storage.prefix = prefix
            self.storages[root] = filesystem_storage

    def _get_bower_components_location(self):
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

        for name in ['assets', ]:
            path = os.path.join(base_dir, name)
            if os.path.exists(path):
                return path
