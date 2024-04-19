from django.shortcuts import render, redirect
from django.views import View
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