from sqlalchemy import text
from models.database import DatabaseManager
import logging

class PrescriptionRepository:
    def __init__(self):
        self.db = DatabaseManager("postgresql://postgres:Admin_2025@localhost/AH2")
        self.session = self.db.get_session()
        self.logger = logging.getLogger(__name__)

    def create_prescription(self, prescription_data):
        try:
            stmt = text("""
                CALL create_prescription(
                    :patient_id, :medication, :dosage, :frequency,
                    :duration, :medical_record_id, :start_date,
                    :end_date, :notes
                )
            """)
            self.session.execute(stmt, {
                'patient_id': prescription_data['patient_id'],
                'medication': prescription_data['medication'],
                'dosage': prescription_data['dosage'],
                'frequency': prescription_data['frequency'],
                'duration': prescription_data['duration'],
                'medical_record_id': prescription_data.get('medical_record_id'),
                'start_date': prescription_data.get('start_date'),
                'end_date': prescription_data.get('end_date'),
                'notes': prescription_data.get('notes')
            })
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            self.logger.error(f"Erreur création prescription: {str(e)}")
            raise