from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password
from store.models import Customer
from django.views import View
from django.urls import reverse_lazy
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from store.helpers import email_verification_token, validate_name, validate_password
from django.core.mail import send_mail
from django.utils.encoding import force_bytes, force_str

class Signup(View):
    template_name = 'signup.html'
    success_url = reverse_lazy('store:home')
    
    def get(self, request):
        if 'customer' in request.session:
            request.session['alert_message'] = 'Already on your account'
            return redirect(self.success_url)
        ctx = {}
        if 'form_errors' in request.session:
            ctx['form_errors'] = request.session['form_errors']
            ctx['form'] = request.session['form']
            del request.session['form_errors']
            del request.session['form']
        return render(request, self.template_name, ctx)

    def post(self, request):
        postData = request.POST
        name = postData.get('name')
        last_name = postData.get('last_name')
        email = postData.get('email')
        password = postData.get('password')
        password2 = postData.get('password2')

        form = {
            'name': name,
            'last_name': last_name,
            'email': email
        }
  
        customer = Customer(name=name,
                            last_name=last_name,
                            email=email,
                            password=password)
        form_errors = self.validate_customer(customer, password2)
  
        if form_errors:
            ctx = {
                'form': form,
                'form_errors': form_errors
            }
            for key, value in ctx.items():
                request.session[key] = value
            return redirect('store:signup')
        else:
            customer.password = make_password(customer.password)
            customer.save()
            self._send_email_verification(customer)
            request.session['alert_message'] = 'We have sent the mail'
            return redirect('store:home')
  
    def validate_customer(self, customer, password2):
        form_errors = {}
        try:
            validate_name(customer.name, 'name', 'name')
        except ValidationError as e:
            form_errors[e.params['bad_field']] = e.message
        try:
            validate_name(customer.last_name, 'last name', 'last_name')
        except ValidationError as e:
            form_errors[e.params['bad_field']] = e.message
        try:
            validate_email(customer.email)
        except ValidationError as e:
            form_errors['email'] = 'Not valid mail'
        try:
            validate_password(customer.password, 'password', 'password')
        except ValidationError as e:
            form_errors[e.params['bad_field']] = e.message
        
        if customer.exists_with_email():
            form_errors['email'] = 'Email already registered'
        if customer.password != password2:
            form_errors['password'] = 'Passwords do not match'
  
        return form_errors
    
    def _send_email_verification(self, user):
        current_site = get_current_site(self.request)
        subject = 'Active su cuenta'
        body = render_to_string(
            'verification.html',
            {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': email_verification_token.make_token(user),
            }
        )
        send_mail(subject=subject, message=body, from_email='aimarket@admin', recipient_list=[user.email], html_message=body)

class Login(View):
    template_name = 'login.html'
    success_url = 'store:home'
  
    def get(self, request):
        if 'customer' in request.session:
            request.session['alert_message'] = 'Already on your account'
            return redirect(self.success_url)
        ctx = {}
        if 'form_error' in request.session: 
            ctx['form_error'] = request.session['form_error']
            del request.session['form_error']
            
        return render(request, self.template_name, ctx)
  
    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            if customer.is_active:
                check = check_password(password, customer.password)
                if check:
                    request.session['customer'] = customer.id
                    return redirect(self.success_url)
                else:
                    error_message = 'Incorrect email or password'
            else:
                error_message = 'Account must be activated'
        else:
            error_message = 'Incorrect email or password'
  
        request.session['form_error'] = error_message
        return redirect('store:login')
  
def logout(request):
    request.session.clear()
    return redirect('store:login')

class ActivateView(View):

    def get_user_from_email_verification_token(self, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = Customer.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,
                Customer.DoesNotExist):
            return None

        if user is not None and email_verification_token.check_token(user, token):
            return user

        return None

    def get(self, request, uidb64, token):
        user = self.get_user_from_email_verification_token(uidb64, token)
        user.is_active = True
        user.save()
        request.session['alert_message'] = 'Your account has been activated'
        return redirect('store:home')