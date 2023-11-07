from django.contrib.auth import authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import logout, authenticate, login
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser
from .forms import LoginForm


def login_view(request):
    data = {
        'form': LoginForm(),
    }
    if request.method == 'POST':
        authentication_form = LoginForm(data=request.POST)

        if authentication_form.is_valid():

            login_usuario = request.POST['username']
            password = request.POST['password']
            user = authenticate(
                request, login_usuario=login_usuario, password=password)
            try:
                user_id = CustomUser.objects.get(login_usuario=login_usuario)
                userA = CustomUser.objects.get(id=user_id.id)

                now = timezone.now()
                if userA.fecha_fin is not None and now > userA.fecha_fin:
                    userA.is_active = False
                else:
                    userA.is_active = True
                userA.save()

                if userA.is_active:
                    if user is not None:
                        login(request, user)
                        return redirect('/admin')
                    else:
                        messages.error(
                            request, 'Credenciales de inicio de sesión incorrectas.')
                else:
                    messages.error(
                        request, 'Su cuenta está desactivada. Póngase en contacto con el administrador.')
            except ObjectDoesNotExist:
                messages.error(
                    request, 'El usuario no existe en la base de datos')

    context = {**data}
    return render(request, 'admin/login.html', context)
