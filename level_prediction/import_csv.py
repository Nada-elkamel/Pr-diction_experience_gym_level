import csv
import unicodedata
from level_prediction.models import Features,Exercice

def import_csv_to_db(file_path):
    """
    Importe les données d'un fichier CSV dans la base de données Django.
    """
    try:
        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Features.objects.create(
                    Age=int(row['Age']),
                    Gender=row['Gender'],
                    Weight=float(row['Weight']),
                    Height=float(row['Height']),
                    Max_BPM=int(row['Max_BPM']),
                    Avg_BPM=int(row['Avg_BPM']),
                    Resting_BPM=int(row['Resting_BPM']),
                    Session_Duration=float(row['Session_Duration']),
                    Calories_Burned=float(row['Calories_Burned']),
                    Workout_Type=row['Workout_Type'],
                    Fat_Percentage=float(row['Fat_Percentage']),
                    Water_Intake=float(row['Water_Intake']),
                    Workout_Frequency=int(row['Workout_Frequency']),  # Nom corrigé
                    Experience_Level=int(row['Experience_Level']),
                    BMI=float(row['BMI'])
                )
        print("Importation terminée avec succès.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")

def normalize_string(s):
    """
    Remplace les caractères spéciaux par leurs équivalents sans accent.
    """
    if not isinstance(s, str):
        return s  # Si ce n'est pas une chaîne, on la retourne inchangée
    return ''.join(
        c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'
    )


def import_csv_to_db_exercice(file_path):
    """
    Importe les données d'un fichier CSV dans la base de données Django,
    en normalisant les caractères spéciaux.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Exercice.objects.create(
                    Name=normalize_string(row['Name']),    # Normalisation appliquée
                    Title=normalize_string(row['title']),  # Normalisation appliquée
                    Excerpt=normalize_string(row['Excerpt'])  # Normalisation appliquée
                )
        print("Importation terminée avec succès.")
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
