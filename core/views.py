from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from .models import MyUser, Course, Roles
from .classes import Auth

class LogInPage(View):
    def get(self,request):
        return render(request, template_name="core/login.html")
    def post(self, request):
        email = request.POST['name']
        password = request.POST['password']
        auth = Auth(email, password)

        if not auth.logIn():
            return render(request, template_name="core/login.html", context={"message": "Wrong email or password"})
        else:
            request.session["email"] = email
            return redirect("/courses/")

class Homepage(View):
    def get(self,request):
        return render(request, "core/homepage.html")
    def post(self,request):
        return render(request, template_name="core/homepage.html")