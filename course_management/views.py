# Create your views here.
from django.shortcuts import render, redirect
from django.views import View

from user_management.models import MyUser, Roles
from course_management.models import Course
#t

# def list(request):
#    return render(request, 'course_list.html')
class CoursesView(View):
    def get(self, request):
        m = request.session["email"]
        courses = Course.objects.all()
        userRole = MyUser.objects.get(email=m).role
        isAdmin = False
        if userRole == Roles.Admin:
            isAdmin = True
        return render(request, "course_management/courses.html", {"courses": courses, "role": isAdmin})

    def post(self, request):
        m = request.session["email"]
        toDelete = request.POST.get("delete", "")

        c = request.POST.get('create', "")
        if c == "create_redirect":
            return redirect("/create_course/")

        courses = Course.objects.all()
        if toDelete != "":
            Course.objects.get(courseID=toDelete).delete()
        userRole = MyUser.objects.get(email=m).role
        isAdmin = False
        if userRole == Roles.Admin:
            isAdmin = True
        return render(request, "course_management/courses.html", {"courses": courses, "role": isAdmin})

class CreateCoursesView(View):
    def get(self, request):
        return render(request, "course_management/create_course.html")
    def post(self, request):
        return render(request, "course_management/create_course.html")

def add_course_view(request):
    if request.method == 'POST':
        # Assuming you have a form with fields for title, description, instructor, and requirements
        title = request.POST.get('title')
        instructor = request.POST.get('instructor')
        ta = request.POST.get('ta')
        description = request.POST.get('description')
        requirements = request.POST.get('requirements')

        # Create an instance of the Course model and call the add_course method to save it to the database
        if Course.objects.filter(title=request.POST.get('title')).exists():
            # if the course already exists, do nothing
            return render(request, 'course_management/create_course.html')

        Course().add_course(title=title,
                            instructor=instructor,
                            ta=ta,
                            description=description,
                            requirements=requirements)

        # Optionally, you can redirect to a success page or render a response
        # return render(request, 'success.html')
    return render(request, 'course_management/create_course.html')

def list(request):
  # Query all courses from the database
  courses = Course.objects.all()

  # Pass the queried courses to the HTML template
  return render(request, 'course_management/course_list.html', {'courses': courses})