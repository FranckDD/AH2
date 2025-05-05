from repositories.prescription_repo import PrescriptionRepository

# controllers/prescription_controller.py
class PrescriptionController:
    def __init__(self):
        self.repo = PrescriptionRepository()

    def list_prescriptions(self, **kwargs):
        return self.repo.list(**kwargs)

    def create_prescription(self, data):
        return self.repo.create(data)
    # update, delete...
