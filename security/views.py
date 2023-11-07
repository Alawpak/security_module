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
                self_user = CustomUser.objects.get(id=user_id.id)

                currentDate = timezone.localtime(timezone.now()).date()
                now = timezone.now()

                if self_user.is_active and user:

                    if self_user.fecha_fin and now > self_user.fecha_fin:
                        self_user.is_active = False
                        self_user.save()
                        messages.error(request,
                                       'Su cuenta ha expirado')
                    elif self_user.fecha_inicio and self_user.fecha_inicio > now:
                        messages.error(
                            request, 'La fecha de inicio de sesión aún no llega. Sea paciente')
                    else:
                        login(request, user)
                        return redirect('/admin')
                else:
                    messages.error(
                        request, 'Su cuenta está desactivada. Póngase en contacto con el administrador.')

            except ObjectDoesNotExist:
                messages.error(
                    request, 'El usuario no existe en la base de datos')

    context = {**data}
    return render(request, 'admin/login.html', context)
