from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.views import logout as Signout
from django.views.generic import TemplateView
from django.views.generic.list import ListView
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.utils.translation import ugettext as _
from django.http import Http404, HttpResponseRedirect

from userena.forms import (SignupForm, SignupFormOnlyEmail, AuthenticationForm,
                           ChangeEmailForm, EditProfileForm)
from userena.models import UserenaSignup
from userena.decorators import secure_required
from userena.utils import signin_redirect, get_profile_model, get_user_profile
from userena import signals as userena_signals
from userena import settings as userena_settings

# this mathods works for signup process

def signup(request, signup_form=SignupForm,
           template_name='userena/signup_form.html', success_url=None,
           extra_context=None):

    if userena_settings.USERENA_DISABLE_SIGNUP:
        raise PermissionDenied

    # If no usernames are wanted and the default form is used, fallback to the
    # default form that doesn't display to enter the username.
    if userena_settings.USERENA_WITHOUT_USERNAMES and (signup_form == SignupForm):
        signup_form = SignupFormOnlyEmail
  
    form = auth_form()

    if request.method == 'POST':
        form = auth_form(request.POST, request.FILES)
        if form.is_valid():
            identification, password, remember_me = (form.cleaned_data['identification'],
                                                     form.cleaned_data['password'],
                                                     form.cleaned_data['remember_me'])
            user = authenticate(identification=identification,
                                password=password)
            if user.is_active:
                login(request, user)
                if remember_me:
                    request.session.set_expiry(userena_settings.USERENA_REMEMBER_ME_DAYS[1] * 86400)
                else: request.session.set_expiry(0)

                if userena_settings.USERENA_USE_MESSAGES:
                    messages.success(request, _('You have been signed in.'),
                                     fail_silently=True)

                #send a signal that a user has signed in
                userena_signals.account_signin.send(sender=None, user=user)
                
                redirect_to = redirect_signin_function(
                    request.GET.get(redirect_field_name,
                                    request.POST.get(redirect_field_name)), user)
                return HttpResponseRedirect(redirect_to)
            else:
                return redirect(reverse('userena_disabled',
                                        kwargs={'username': user.username}))

    if not extra_context: extra_context = dict()
    extra_context.update({
        'form': form,
        'next': request.GET.get(redirect_field_name,
                                request.POST.get(redirect_field_name)),
    })
    return ExtraContextTemplateView.as_view(template_name=template_name,
                                            extra_context=extra_context)(request)

@secure_required
def signin(request, auth_form=AuthenticationForm,
           template_name='userena/signin_form.html',
           redirect_field_name=REDIRECT_FIELD_NAME,
           redirect_signin_function=signin_redirect, extra_context=None):
 form = auth_form()

    if request.method == 'POST':
        form = auth_form(request.POST, request.FILES)
        if form.is_valid():
            identification, password, remember_me = (form.cleaned_data['identification'],
                                                     form.cleaned_data['password'],
                                                     form.cleaned_data['remember_me'])
            user = authenticate(identification=identification,
                                password=password)
            if user.is_active:
                login(request, user)
                if remember_me:
                    request.session.set_expiry(userena_settings.USERENA_REMEMBER_ME_DAYS[1] * 86400)
                else: request.session.set_expiry(0)

                if userena_settings.USERENA_USE_MESSAGES:
                    messages.success(request, _('You have been signed in.'),
                                     fail_silently=True)

                #send a signal that a user has signed in
                userena_signals.account_signin.send(sender=None, user=user)
                
                redirect_to = redirect_signin_function(
                    request.GET.get(redirect_field_name,
                                    request.POST.get(redirect_field_name)), user)
                return HttpResponseRedirect(redirect_to)
            else:
                return redirect(reverse('userena_disabled',
                                        kwargs={'username': user.username}))

    if not extra_context: extra_context = dict()
    extra_context.update({
        'form': form,
        'next': request.GET.get(redirect_field_name,
                                request.POST.get(redirect_field_name)),
    })
    return ExtraContextTemplateView.as_view(template_name=template_name,
                                            extra_context=extra_context)(request)

@secure_required
def signout(request, next_page=userena_settings.USERENA_REDIRECT_ON_SIGNOUT,
            template_name='userena/signout.html', *args, **kwargs):
    if request.user.is_authenticated() and userena_settings.USERENA_USE_MESSAGES: # pragma: no cover
        messages.success(request, _('You have been signed out.'), fail_silently=True)
    userena_signals.account_signout.send(sender=None, user=request.user)
    return Signout(request, next_page, template_name, *args, **kwargs)
