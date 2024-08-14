from django.shortcuts import redirect, render, get_object_or_404
from app.models import Categories, Course
from app.decorators import course_access_required
from django.urls import reverse
import logging

from app.models import Notice

logger = logging.getLogger(__name__)

def BASE(request):
    return render(request, 'base.html')


def HOME(request):
    category = Categories.objects.all().order_by('id')[0:20]
    course = Course.objects.all().order_by('id')[0:100]
    announcement = Notice.objects.first()
    context = {
        'category' : category,
        'course' : course,
        'announcement': announcement
    }
    return render(request, 'main/home.html',context)
def CONTACT_US(request):
    return render(request, 'main/contact_us.html')

def SEARCH_COURSE(request):
    query = request.GET.get('query', '')
    course = Course.objects.filter(course_title__icontains=query)
    context = {
        'course': course,
    }
    return render(request, 'search/search.html', context)


@course_access_required
def COURSE_DETAILS(request, slug):
    logger.info('Attempting to access course with slug: %s', slug)
    
    # Fetch the course and check for existence
    course = Course.objects.filter(slug=slug).first()
    if not course:
        logger.warning('Course not found for slug: %s', slug)
        return redirect(reverse('404'))

    # Log course details for debugging
    logger.info('Course found: %s', course)
    
    # Fetch lessons and log the count
    lessons = course.lessons.all()
    logger.info('Number of lessons found: %d', lessons.count())

    return render(request, 'course/course_details.html', {'course': course, 'lessons': lessons})

def PAGE_NOT_FOUND(request):
    return render(request, 'error/404.html')
