import json

from django.http import JsonResponse
from django.views import View


class HomePage(View):

    def get(self, request):
        return JsonResponse(request, {'a': 'b'})
