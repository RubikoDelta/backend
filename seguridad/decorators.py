from functools import wraps
import time
from django.http.response import JsonResponse
from http import HTTPStatus
from jose import jwt
from django.conf import settings


def logueado():
    def metodo(func):
        @wraps(func)
        def _decorator(request, *args, **kwargs):
            req = args[0]

            if not req.headers.get('Authorization') or req.headers.get('Authorization') == None:
                return JsonResponse({'Estado': 'Error', 'Mensaje': 'Sin autorizacion'}, status=HTTPStatus.UNAUTHORIZED)

            header = req.headers.get('Authorization').split(" ")
            try:
                resuelto = jwt.decode(
                    header[1], settings.SECRET_KEY, algorithms=['HS512'])
                # return JsonResponse({'id': user.id, 'nombre':user.first_name, 'token': token})
            except Exception as e:
                return JsonResponse({'Estado': 'Error', 'Mensaje': 'Sin autorizacion'}, status=HTTPStatus.UNAUTHORIZED)

            if int(resuelto['exp']) > int(time.time()):
                return func(request, *args, **kwargs)
            else:
                return JsonResponse({'Estado': 'Error', 'Mensaje': 'No autorizado'}, status=HTTPStatus.UNAUTHORIZED)
            return func(request, *args, **kwargs)
        return _decorator
    return metodo
