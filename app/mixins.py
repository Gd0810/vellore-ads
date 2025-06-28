import os
from django.conf import settings

class ImageCleanupMixin:
    def delete_old_file(self, field_name):
        try:
            old = self.__class__.objects.get(pk=self.pk)
            old_file = getattr(old, field_name)
            new_file = getattr(self, field_name)

            if old_file and old_file != new_file and os.path.isfile(old_file.path):
                os.remove(old_file.path)
        except self.__class__.DoesNotExist:
            pass  # First time object is saved

    def delete_file_on_delete(self, field_name):
        file = getattr(self, field_name)
        if file and os.path.isfile(file.path):
            os.remove(file.path)
