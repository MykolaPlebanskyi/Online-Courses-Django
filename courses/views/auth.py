from django.shortcuts import render , redirect
from django.contrib.auth import logout , login
from courses.forms import RegistrationForm , LoginForm
from django.views import View
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login


class SignupView(FormView):
    template_name = "courses/signup.html"
    form_class = RegistrationForm
    success_url = '/'

    def form_valid(self, form):
        # Save the form data to create a new user
        form.save()

        # Authenticate the new user
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']  # or 'password2', as per your preference
        
        user = authenticate(self.request, username=username, password=password)

        # Log the user in if authentication succeeds
        if user is not None:
            login(self.request, user)
        
        return super().form_valid(form)
    

class LoginView(FormView):
    template_name = "courses/login.html"
    form_class = LoginForm
    success_url = '/'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password')
        
        user = authenticate(self.request, username=username, password=password)
        
        if user is not None:
            login(self.request, user)
            next_page = self.request.GET.get('next')
            if next_page is not None:
                return redirect(next_page)
            return super().form_valid(form)
        else:
            # Handle invalid login credentials here
            # For example, you could set an error message in the form
            form.add_error(None, 'Invalid username or password')
            return self.form_invalid(form)  


def signout(request ):
    logout(request)
    return redirect("home")

