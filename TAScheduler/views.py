from django.shortcuts import render, redirect
from django.views import View
from .models import MyUser, Course, Roles
from .classes import Auth

class LogInPage(View):
    def get(self,request):
        return render(request, template_name="login.html")
    def post(self, request):
        email = request.POST['name']
        password = request.POST['password']
        auth = Auth(email, password)

        if not auth.logIn():
            return render(request, template_name="login.html", context={"message":"Wrong email or password"})
        else:
            request.session["email"] = email
            return redirect("/courses/")

class Homepage(View):
    def get(self,request):
        return render(request, "homepage.html")
    def post(self,request):
        return render(request, template_name="homepage.html")

class CoursesView(View):
    def get(self,request):
        m = request.session["email"]
        courses = Course.objects.all()
        userRole = MyUser.objects.get(email=m).role
        isAdmin = False
        if userRole == Roles.Admin:
            isAdmin = True
        return render(request, "courses.html", {"courses": courses, "role": isAdmin})


def post(self,request):
        m = request.session["email"]
        toDelete = request.POST.get("delete", "")
        courses = Course.objects.all()
        if toDelete != "":
            Course.objects.get(courseID=toDelete).delete()
        userRole = MyUser.objects.get(email=m).role
        isAdmin = False
        if userRole == Roles.Admin:
            isAdmin = True
        return render(request, "courses.html", {"courses": courses, "role": isAdmin})
