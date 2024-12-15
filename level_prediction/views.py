from django.shortcuts import render
import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder, StandardScaler
from django.http import HttpResponse
from django.core.paginator import Paginator
from level_prediction.models import Features, Exercice

import os
from django.conf import settings

def features_list(request):
    features = Features.objects.all()

    features = features.order_by('id') 
    page_number = request.GET.get('page', 1)  
    paginator = Paginator(features, 8)  
    page_obj = paginator.get_page(page_number)

    query_params = request.GET.copy()  
    query_params['page'] = page_obj.number  
    pagination_url = query_params.urlencode()  

    return render(request, 'features_list.html', {
        'features': page_obj,
        'pagination_url': pagination_url, 
    })

from django.core.paginator import Paginator

def exercices_list(request):
    # Get filter values from the GET request
    Name = request.GET.get('name', '')

    # Start with all Exercices
    exercices = Exercice.objects.all()

    # Apply filters if they are set
    if Name:
        exercices = exercices.filter(Name=Name)

    # Implement pagination with 5 items per page
    exercices = exercices.order_by('id')  # Order by ID or any other field
    page_number = request.GET.get('page', 1)  # Default to page 1 if not specified
    paginator = Paginator(exercices, 5)  # 5 items per page
    page_obj = paginator.get_page(page_number)

    # Return the filtered and paginated data to the template
    return render(request, 'exercices.html', {'exercices': page_obj, 'name': Name})

def powerbi_dashboard(request):
    embed_url = "https://app.powerbi.com/view?r=eyJrIjoiNWM5MGU0YjYtYTM2Zi00YWYxLWE5YWMtZGI5NjI5ZWY0YWJlIiwidCI6ImRiZDY2NjRkLTRlYjktNDZlYi05OWQ4LTVjNDNiYTE1M2M2MSIsImMiOjl9&navContentPaneEnabled=false"
    return render(request, 'dashboard.html', {'embed_url': embed_url})

# def my_simple_view(request):
#     return render(request, 'user_form.html')

def sidebar(request):
    return render(request, 'sidebar.html')


# Construct the path to the model file
svm_model_path = os.path.join(settings.BASE_DIR, 'level_prediction', 'ML', 'svm_model.pkl')
scaler_path = os.path.join(settings.BASE_DIR, 'level_prediction', 'ML', 'scaler.pkl')
label_encoders_path = os.path.join(settings.BASE_DIR, 'level_prediction', 'ML', 'label_encoders.pkl')

# Chargez le modèle et les outils de transformation ici
svm_model = joblib.load(svm_model_path)
scaler = joblib.load(scaler_path)
label_encoders = joblib.load(label_encoders_path)

from django.shortcuts import redirect
from django.urls import reverse

def predict_experience(request):
    if request.method == "POST":
        try:
            # Extract form data into a DataFrame
            input_data = pd.DataFrame([{
                'Age': request.POST.get("Age"),
                'Gender': request.POST.get("Gender"),
                'Weight': request.POST.get("Weight"),
                'Height': request.POST.get("Height"),
                'Max_BPM': request.POST.get("Max_BPM"),
                'Avg_BPM': request.POST.get("Avg_BPM"),
                'Resting_BPM': request.POST.get("Resting_BPM"),
                'Session_Duration': request.POST.get("Session_Duration"),
                'Calories_Burned': request.POST.get("Calories_Burned"),
                'Workout_Type': request.POST.get("workout_type"),
                'Fat_Percentage': request.POST.get("Fat_Percentage"),
                'Water_Intake': request.POST.get("Water_Intake"),
                'Workout_Frequency': request.POST.get("Workout_Frequency"),
                'BMI': request.POST.get("BMI"),
            }])

            # Encode categorical features using the same label encoders as during training
            for col, le in label_encoders.items():
                if col in input_data.columns:
                    input_data[col] = le.transform(input_data[col])

            # Scale the data using the saved scaler
            input_data_scaled = scaler.transform(input_data)

            # Predict the experience level (returns a numeric value 1, 2, or 3)
            prediction = svm_model.predict(input_data_scaled)

            # Map the numeric prediction to the experience level label
            experience_level_map = {
                1: 'Beginner',
                2: 'Intermediate',
                3: 'Advanced'
            }

            # Get the experience level as a label (e.g., 'Beginner', 'Intermediate', 'Advanced')
            experience_level = experience_level_map.get(prediction[0], 'Unknown')

        except Exception as e:
            experience_level = f"Erreur: {str(e)}"

        # Redirect to result page with experience_level as a GET parameter
        return redirect(reverse('result_page') + f'?experience_level={experience_level}')
    
    return render(request, 'user_form.html')

def result_page(request):
    experience_level = request.GET.get('experience_level', 'No result')
    return render(request, 'result_page.html', {'experience_level': experience_level})
