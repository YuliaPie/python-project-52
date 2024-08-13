from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import ProtectedError
from django.http import HttpResponseRedirect
from django.views.generic import View, UpdateView, CreateView
from django.shortcuts import render, redirect, get_object_or_404
from .models import CustomUser
from .forms import UserForm, UserUpdateForm
from django.urls import reverse_lazy
from django.contrib import messages
from task_manager.tools import check_and_redirect_if_not_auth
import logging
from django.contrib.auth.decorators import login_required

logger = logging.getLogger(__name__)


class IndexView(View):

    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.all()
        return render(request, 'users/user_list.html',
                      context={
                          'users': users,
                      })


class UserCreateView(SuccessMessageMixin, CreateView):
    model = CustomUser
    form_class = UserForm
    template_name = 'users/create.html'
    success_url = reverse_lazy('login')
    success_message = "Пользователь успешно зарегистрирован."


class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = CustomUser
    form_class = UserUpdateForm
    template_name = 'users/update.html'
    success_url = reverse_lazy('users:users')
    success_message = "Пользователь успешно изменен."


def user_confirm_delete(request, user_id):
    is_authorised = check_and_redirect_if_not_auth(request)
    if is_authorised:
        return is_authorised
    user = get_object_or_404(CustomUser, id=user_id)
    if request.user.id != user.id:
        messages.error(request,
                       "У вас нет прав для изменения другого пользователя.",
                       extra_tags='danger')
        return redirect(
            'users:users')
    return render(request,
                  'users/user_confirm_delete.html',
                  {'user': user})


class UserDeleteView(View):

    def post(self, request, user_id):
        user = CustomUser.objects.get(id=user_id)
        if user:
            try:
                user.delete()
            except ProtectedError:
                messages.error(
                    request,
                    'Невозможно удалить пользователя, потому что он используется.',
                    extra_tags='danger')
                return redirect('users:users')
        messages.success(request, "Пользователь успешно удален.")
        return redirect('users:users')
