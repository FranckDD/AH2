# repositories/medical_repo.py
from sqlalchemy import text
from models.database import DatabaseManager
from sqlalchemy.orm import Session
from models.medical_record import MedicalRecord    # ← import ajouté


class MedicalRecordRepository:
    def __init__(self):
        self.db = DatabaseManager("postgresql://postgres:Admin_2025@localhost/AH2")
        self.session = self.db.get_session()

    def list(self, patient_id=None, page=1, per_page=20):
        q = self.session.query(MedicalRecord)
        if patient_id:
            q = q.filter_by(patient_id=patient_id)
        return q.offset((page-1)*per_page).limit(per_page).all()

    def get(self, record_id):
        return self.session.get(MedicalRecord, record_id)

    def create(self, data):
        sql = text("CALL public.create_medical_record(:patient_id, :marital_status, ...)")
        self.session.execute(sql, data)
        self.session.commit()
