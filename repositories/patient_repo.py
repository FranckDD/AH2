# repositories/patient_repository.py
from datetime import date
from sqlalchemy import text
from sqlalchemy.orm import Session
from models.database import DatabaseManager
from models.patient import Patient

class PatientRepository:
    def __init__(self):
        self.db: DatabaseManager = DatabaseManager("postgresql://postgres:Admin_2025@localhost/AH2")
        self.session: Session    = self.db.get_session()

    def generate_patient_code(self,
                              birth_date: date,
                              last_name: str,
                              first_name: str,
                              mother_name: str) -> str:
        prefix = "AH2-"
        year   = birth_date.strftime('%y')
        month  = birth_date.strftime('%m')
        day    = birth_date.strftime('%d')
        letter_last   = (last_name[0] if last_name else 'X').upper()
        letter_mother = (mother_name[0] if mother_name else 'X').upper()
        return f"{prefix}{year}{month}{day}{letter_last}{letter_mother}"

    def create_patient(self, data: dict, current_user) -> int:
        # génère le code
        code = self.generate_patient_code(
            birth_date   = data['birth_date'],
            last_name    = data['last_name'],
            first_name   = data['first_name'],
            mother_name  = data.get('mother_name', '')
        )
        # appel de la proc stockée
        sql = text("""CALL public.create_patient(
            :code_patient, :first_name, :last_name, :birth_date, 
            :gender, :contact_phone, :residence,
            :national_id, :assurance, :father_name, :mother_name
        )""")
        params = {
            'code_patient': code,
            'first_name'  : data['first_name'],
            'last_name'   : data['last_name'],
            'birth_date'  : data['birth_date'],
            'gender'      : data.get('gender'),
            'contact_phone': data.get('contact_phone'),
            'residence'   : data.get('residence'),
            'national_id' : data.get('national_id'),
            'assurance'   : data.get('assurance'),
            'father_name' : data.get('father_name'),
            'mother_name' : data.get('mother_name'),
        }
        self.session.execute(sql, params)
        # récupérer l'ID auto-incrémenté
        new_id = self.session.execute(
            text("SELECT currval('patients_patient_id_seq') AS id")
        ).scalar_one()
        self.session.commit()
        return new_id

    def update_patient(self, patient_id: int, data: dict, current_user) -> int:
        sql = text("""CALL public.update_patient(
            :patient_id,
            :first_name, :last_name, :birth_date, :gender,
            :national_id, :contact_phone, :assurance, :residence,
            :father_name, :mother_name
        )""")
        params = {
            'patient_id'  : patient_id,
            'first_name'  : data.get('first_name'),
            'last_name'   : data.get('last_name'),
            'birth_date'  : data.get('birth_date'),
            'gender'      : data.get('gender'),
            'national_id' : data.get('national_id'),
            'contact_phone': data.get('contact_phone'),
            'assurance'   : data.get('assurance'),
            'residence'   : data.get('residence'),
            'father_name' : data.get('father_name'),
            'mother_name' : data.get('mother_name'),
        }
        result = self.session.execute(sql, params)
        self.session.commit()
        return result.rowcount

    def delete_patient(self, patient_id: int) -> int:
        sql = text("CALL public.delete_patient(:patient_id)")
        self.session.execute(sql, {'patient_id': patient_id})
        self.session.commit()
        # si ta proc ne renvoie pas rowcount, tu peux vérifier via SELECT
        return 1

    def get_by_id(self, patient_id: int) -> dict:
        return self.session.query(Patient)\
            .filter(Patient.patient_id == patient_id).one_or_none().__dict__

    def list_patients(self, page: int=1, per_page: int=10, search: str=None):
        query = self.session.query(Patient)
        if search:
            term = f"%{search}%"
            query = query.filter(
                Patient.first_name.ilike(term) |
                Patient.last_name.ilike(term)  |
                Patient.national_id.ilike(term)
            )
        return query.order_by(Patient.last_name)\
                    .offset((page-1)*per_page).limit(per_page).all()
