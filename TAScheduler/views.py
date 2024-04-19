from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import UpdateView

from TAScheduler.forms import CreateUserForm, MyUserUpdateForm
from TAScheduler.models import MyUser

from TAScheduler.models import MyUser
from TAScheduler.classes import Auth

class LogInPage(View):
    def get(self,request):
        return render(request, template_name="login.html")
    def post(self, request):
        auth = Auth()
        email = request.POST['name']
        password = request.POST['password']

        if not auth.logIn(email, password):
            return render(request, template_name="login.html", context={"message": "Wrong email or password"})
        else:
            request.session["email"] = email
            return redirect("/homepage/") # temporary

class Homepage(View):
    def get(self,request):
        return render(request, "homepage.html")

    def post(self, request):
        return render(request, "homepage.html")

class EditAccountView(UpdateView):
    model = MyUser
    form_class = MyUserUpdateForm
    template_name = 'user_management/edit_account.html'
    success_url = reverse_lazy('home')  # Update with your success URL

    def get_object(self):
        return self.request.user

def CreateUserView(request):
    def create_user(request):
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('user_created')
        else:
            form = CreateUserForm()
        return render(request, 'create_user.html', {'form': form})

    def user_created(request):
        return render(request, 'templates/HomePages/AdminHome.html')