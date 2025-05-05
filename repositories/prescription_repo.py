# repositories/prescription_repo.py
from sqlalchemy import text
from models.database import DatabaseManager
from sqlalchemy.orm import Session
from models.prescription import Prescription    # ← import ajouté

class PrescriptionRepository:
    def __init__(self):
        self.db = DatabaseManager("postgresql://postgres:Admin_2025@localhost/AH2")
        self.session = self.db.get_session()

    def list(self, patient_id=None, page=1, per_page=20):
        q = self.session.query(Prescription)
        if patient_id:
            q = q.filter_by(patient_id=patient_id)
        return q.offset((page-1)*per_page).limit(per_page).all()

    def get(self, prescription_id):
        return self.session.get(Prescription, prescription_id)

    def create(self, data):
        # appelle ta proc SQL
        sql = text("CALL public.create_prescription(:patient_id, :medication, ...)")
        self.session.execute(sql, data)
        self.session.commit()
