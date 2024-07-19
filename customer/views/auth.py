from email.message import EmailMessage

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import send_mail, EmailMessage
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View
from django.views.generic import FormView
from customer.models import CustomUserManager

from customer.forms import LoginForm, EmailForm
from customer.forms import RegisterModelForm
from customer.managers import CustomUserManager
from customer.forms import EmailForm,RegisterModelForm,LoginForm,RegisterModelForm
from customer.token import account_activation_token


def login_page(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('customers')
    else:
        form = LoginForm()

    return render(request, 'auth/login.html', {'form': form})


def logout_page(request):
    if request.method == 'GET   ':
        logout(request)
        return redirect('customers')
    return render(request,'auth/logout.html')



def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUserManager.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, CustomUserManager.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Your account has been activated successfully!😊')
        return redirect('customers')
    else:
        messages.error(request, 'Activation link is invalid!')
        return redirect('register')


def activate_email(request, user, to_email):
    subject = 'Activate your account'
    message = render_to_string('authentication/template_activate_account.html', {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.id)),
        'protocol': 'https' if request.is_secure() else 'http',
        'token': account_activation_token.make_token(user),
    })
    email = EmailMessage(subject, message, to=[to_email])
    try:
        email.send()
        messages.success(request,
                         'Activation email has been sent. You have 5 minut to activate your account. '
                         'Please check your email')
    except Exception as e:
        messages.error(request, f'Sorry, there was an error sending the activation email: {str(e)}')


def register_page(request):
    if request.method == 'POST':
        form = RegisterModelForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            activate_email(request, user, to_email=form.cleaned_data['email'])
            return redirect('customers')

    else:
        form = RegisterModelForm()

    return render(request, 'auth/register.html', {'form': form})


# def register(request):
#     form=RegisterModelForm()
#     if request.method == 'POST':
#         form=RegisterModelForm(request.POST)
#         if form.is_valid():
#             user=form.save(commit=False)
#             password=form.cleaned_data['password']
#             user.set_password(password)
#             user.save()
#             login(request, user)
#             return redirect('customers')
#     else:
#         form=RegisterModelForm()
#     return render(request, 'auth/register.html', {'form' : form } )



class LoginPageView(View):

    def get(self, request):
        form = LoginForm()
        return render(request, 'auth/login.html', {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('customers')

        return render(request, 'auth/login.html', {'form': form})


class LoginPage(LoginView):
    template_name = 'auth/login.html'
    redirect_authenticated_user = True
    authentication_form = LoginForm

    # success_url = reverse_lazy('customers')

    def get_success_url(self):
        return reverse_lazy('customers')


class RegisterFormView(FormView):
    template_name = 'auth/register.html'
    form_class = RegisterModelForm
    success_url = reverse_lazy('customers')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.email = form.cleaned_data['email']
        user.password = form.cleaned_data['password']
        user.save()
        login(self.request, user)
        return redirect('customers')




class SendEmailView(View):
    def get(self, request):
        form = EmailForm()
        context = {'form': form}
        return render(request, 'app/send-email.html', context)

    def post(self, request):
        form = EmailForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email_from = form.cleaned_data['email_from']
            email_to = [form.cleaned_data['email_to']]
            message = form.cleaned_data['message']
            try:
                send_mail(subject, message, email_from, email_to)
                messages.success(request, 'Message sent successfully.')
                return redirect('customers')
            except Exception as e:
                messages.error(request, f'Error sending message: {e}')

        context = {'form': form}
        return render(request, 'app/send-email.html', context)