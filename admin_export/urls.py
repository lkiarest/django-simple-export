from django.http import HttpResponse
from django.urls import path


def default_handler(request, *args):
    return HttpResponse('warning: no handler for {}.{}'.format(args[0], args[1]))


urlpatterns = [
    path('<str:app_label>/<str:model_name>/export', default_handler, name='dae_export')
]
