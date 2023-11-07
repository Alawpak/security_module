# # middleware.py
# from django.utils import timezone
# from django.contrib.auth import logout


# class CheckAccountExpirationMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         # Verificar si el usuario está autenticado
#         if request.user.is_authenticated:
#             user = request.user

#             # Verificar si la cuenta ha expirado
#             if user.fecha_fin and timezone.now() > user.fecha_fin:
#                 logout(request)
#                 # Puedes redirigir a una página de expiración de cuenta si lo deseas
#                 # return redirect('pagina_de_expiracion')

#         response = self.get_response(request)
#         return response
