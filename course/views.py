from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Course


# def list(request):
#    return render(request, 'course_list.html')

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
            return render(request, 'create_course.html')

        Course().add_course(title=title,
                            instructor=instructor,
                            ta=ta,
                            description=description,
                            requirements=requirements)

        # Optionally, you can redirect to a success page or render a response
        # return render(request, 'success.html')
    return render(request, 'create_course.html')

def list(request):
  # Query all courses from the database
  courses = Course.objects.all()

  # Pass the queried courses to the HTML template
  return render(request, 'course_list.html', {'courses': courses})