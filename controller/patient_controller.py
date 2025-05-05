# controllers/patient_controller.py
import logging
class PatientController:
    def __init__(self, repo, current_user):
        self.repo = repo
        self.user = current_user
        self.logger = logging.getLogger(__name__)

    def create_patient(self, data: dict) -> tuple[int,str]:
        required = ['first_name', 'last_name', 'birth_date']
        if any(not data.get(f) for f in required):
            raise ValueError("Champs obligatoires manquants")
        return self.repo.create_patient(data, self.user)

    def update_patient(self, patient_id: int, data: dict) -> tuple[int, str]:
        return self.repo.update_patient(patient_id, data, self.user)

    def delete_patient(self, patient_id: int) -> bool:
        return self.repo.delete_patient(patient_id)

    def get_patient(self, patient_id: int) -> dict:
        return self.repo.get_by_id(patient_id)

    def list_patients(self, page=1, per_page=10, search=None):
        return self.repo.list_patients(page, per_page, search)