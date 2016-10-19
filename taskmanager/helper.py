from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json


class JsonResponse(HttpResponse):
    def __init__(self, content={}, status=None, content_type='application/json'):
        super(JsonResponse,self).__init__(json.dumps(content,cls=DjangoJSONEncoder),
                                           status=status, content_type=content_type)





	