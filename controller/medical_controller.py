from repositories.medical_repo import MedicalRecordRepository

# controllers/medical_controller.py
class MedicalRecordController:
    def __init__(self):
        self.repo = MedicalRecordRepository()

    def list_records(self, **kwargs):
        return self.repo.list(**kwargs)

    def create_record(self, data):
        return self.repo.create(data)
    # update, delete...
