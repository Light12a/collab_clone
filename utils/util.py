
import json

import pytz
from datetime import date, datetime


class ObjAwareEncoder(json.JSONEncoder):
    """ Mechanism to json serialize non default objects within restful apps

    To make use of this encoder, before main() set:
    import json
    json._default_encoder = ObjAwareEncoder()
    """
    def default(self, obj):
        # Convert datetime module objects to isoformat
        if isinstance(obj, (datetime, date)):
            # datetime inherits from date. To filter out dates we need
            # to filter out non datetimes.
            if not isinstance(obj, datetime):
                # Convert date objects to datetime. Defaults to midnight
                obj = datetime.combine(obj, datetime.min.time())
            obj = obj.replace(tzinfo=pytz.UTC)
            return obj.isoformat()
        # Convert Sets to Lists
        elif isinstance(obj, set):
            return list(obj)
        return super(ObjAwareEncoder, self).default(obj)
