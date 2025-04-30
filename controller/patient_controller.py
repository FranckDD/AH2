# controllers/patient_controller.py
import logging
from functools import wraps

class PatientController:
    def __init__(self, repo, current_user):
        self.repo = repo
        self.user = current_user
        self.logger = logging.getLogger(__name__)

    def create_patient(self, data: dict):
        required = ['first_name', 'last_name', 'birth_date']
        if not all(data.get(f) for f in required):
            raise ValueError("Champs obligatoires manquants")
        try:
            return self.repo.create_patient(data, self.user)
        except Exception as e:
            self.logger.error(f"Erreur création patient: {e}")
            raise

    def update_patient(self, patient_id: int, data: dict):
        try:
            return self.repo.update_patient(patient_id, data, self.user)
        except Exception as e:
            self.logger.error(f"Erreur maj patient {patient_id}: {e}")
            raise

    def delete_patient(self, patient_id: int):
        try:
            return self.repo.delete_patient(patient_id)
        except Exception as e:
            self.logger.error(f"Erreur suppression patient {patient_id}: {e}")
            raise

    def get_patient(self, patient_id: int):
        return self.repo.get_by_id(patient_id)

    def list_patients(self, page=1, per_page=10, search=None):
        return self.repo.list_patients(page, per_page, search)
