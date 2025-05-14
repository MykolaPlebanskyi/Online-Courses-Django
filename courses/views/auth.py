from django.shortcuts import redirect
from django.contrib.auth import logout
from courses.forms import RegistrationForm, LoginForm
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login


class SignupView(FormView):
    template_name = "courses/signup.html"
    form_class = RegistrationForm
    success_url = '/'

    def form_valid(self, form):
        form.save()

        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']

        user = authenticate(self.request, username=username, password=password)

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
            form.add_error(None, 'Invalid username or password')
            return self.form_invalid(form)


def signout(request):
    logout(request)
    return redirect("home")
