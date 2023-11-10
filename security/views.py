from django.contrib.auth import authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from .models import CustomUser
from django.contrib.auth import update_session_auth_hash
from .forms import CustomPasswordChangeForm, LoginForm


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
                now = timezone.now()

                # if it's authenticated
                if user:
                    if self_user.is_active:
                        if self_user.fecha_fin and now > self_user.fecha_fin:
                            self_user.is_active = False
                            self_user.save()
                            messages.error(request,
                                           'Su cuenta ha expirado. Fecha fin ya pasó')
                        elif self_user.fecha_inicio and self_user.fecha_inicio > now:
                            messages.error(
                                request, 'La fecha de inicio de sesión aún no llega. Sea paciente')
                        else:
                            login(request, user)
                            return redirect('/admin')
                    else:
                        messages.error(
                            request, 'Su cuenta está desactivada')
                elif self_user and not self_user.is_active:
                    messages.error(
                        request, 'Su cuenta está desactivada. Ponerse en contacto con el admin')
                else:
                    messages.error(
                        request, 'Contraseña incorrecta')
            except ObjectDoesNotExist:
                messages.error(
                    request, 'El usuario no existe')

    context = {**data}
    return render(request, 'admin/login.html', context)


def change_password(request):
    username = request.user.login_usuario
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect('/admin')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'admin/change_password.html', {'form': form, 'username': username})
