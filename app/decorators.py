from functools import wraps
from django.shortcuts import get_object_or_404, redirect
from .models import Course, CourseAccess

def course_access_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, slug, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')  # Redirect to the login page or an appropriate page

        course = get_object_or_404(Course, slug=slug)
        access = CourseAccess.objects.filter(user=request.user, course=course, access_granted=True).exists()
        if not access:
            return redirect('404')  # or render an error page

        return view_func(request, course, *args, **kwargs)
    return _wrapped_view
