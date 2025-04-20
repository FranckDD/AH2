from repositories.patient_repository import PatientRepository
from models.patient import Patient

class PatientController:
    def __init__(self, db_manager):
        self.repo = PatientRepository(db_manager)
    
    def create_patient(self, patient_data, current_user):
        # Validation des données
        required = ['first_name', 'last_name', 'birth_date', 'gender']
        for field in required:
            if not patient_data.get(field):
                raise ValueError(f"Champ requis: {field}")
        
        # Vérification des permissions
        if current_user.role not in ['app_medical', 'app_secretaire']:
            raise PermissionError("Droits insuffisants")
        
        # Appel de la procédure stockée
        return self.repo.create_patient(patient_data, current_user.id)