from django.shortcuts import render

from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Features, Exercice

def features_list(request):
    # Get filter values from the GET request
    gender = request.GET.get('gender', '')
    experience_level = request.GET.get('experience_level', '')
    workout_type = request.GET.get('workout_type', '')

    # Start with all features
    features = Features.objects.all()

    # Apply filters if they are set
    if gender:
        features = features.filter(Gender=gender)
    if experience_level:
        features = features.filter(Experience_Level=experience_level)
    if workout_type:
        features = features.filter(Workout_Type=workout_type)

    # Implement pagination with 8 items per page
    features = features.order_by('id')  # Order by ID or any other field
    page_number = request.GET.get('page', 1)  # Default to page 1 if not specified
    paginator = Paginator(features, 8)  # **8 items per page**
    page_obj = paginator.get_page(page_number)

    # Prepare the pagination URL with filters
    query_params = request.GET.copy()
    query_params['page'] = page_obj.number  # Update the page number in the query params
    pagination_url = query_params.urlencode()  # Generate the URL with current filters and page number

    return render(request, 'features_list.html', {
        'features': page_obj,
        'pagination_url': pagination_url,  # Pass the URL to the template for pagination links
        'gender': gender,
        'experience_level': experience_level,
        'workout_type': workout_type
    })
    
def exercices_list(request):
    # Get filter values from the GET request
    Name = request.GET.get('name', '')
    

    # Start with all Exercices
    exercices = Exercice.objects.all()

    # Apply filters if they are set
    if Name:
        exercices = exercices.filter(Name=Name)

    # Implement pagination with 8 items per page
    exercices = exercices.order_by('id')  # Order by ID or any other field
    page_number = request.GET.get('page', 1)  # Default to page 1 if not specified
    paginator = Paginator(exercices, 5)  # **5 items per page**
    page_obj = paginator.get_page(page_number)

    return render(request, 'exercices.html', {'exercices': page_obj})

def powerbi_dashboard(request):
    embed_url = "https://app.powerbi.com/view?r=eyJrIjoiNWM5MGU0YjYtYTM2Zi00YWYxLWE5YWMtZGI5NjI5ZWY0YWJlIiwidCI6ImRiZDY2NjRkLTRlYjktNDZlYi05OWQ4LTVjNDNiYTE1M2M2MSIsImMiOjl9&navContentPaneEnabled=false"
    return render(request, 'dashboard.html', {'embed_url': embed_url})

