import json
import six
from openapi_server.models.base_model_ import Model

try:
    # Flask 2.x still provides this
    from flask.json import JSONEncoder as BaseJSONEncoder
except ImportError:
    # Flask 3.x removed it → use Python’s built-in encoder
    from json import JSONEncoder as BaseJSONEncoder


class JSONEncoder(BaseJSONEncoder):
    include_nulls = False

    def default(self, o):
        if isinstance(o, Model):
            dikt = {}
            for attr, _ in six.iteritems(o.openapi_types):
                value = getattr(o, attr)
                if value is None and not self.include_nulls:
                    continue
                attr = o.attribute_map[attr]
                dikt[attr] = value
            return dikt
        # fall back to the parent implementation
        try:
            return super().default(o)
        except TypeError:
            return str(o)
