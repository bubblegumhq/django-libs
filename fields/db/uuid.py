from django_extensions.db.fields import UUIDField
import shortuuid


class ShortUUIDField(UUIDField):
    def create_uuid(self):
        return shortuuid.uuid()

