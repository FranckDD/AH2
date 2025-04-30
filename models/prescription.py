import psycopg2
from datetime import date
from typing import Optional

class Prescription:
    VALID_STATUSES = {'active', 'completed', 'cancelled'}
    
    def __init__(self, db_connection):
        self.conn = db_connection
        self.cursor = self.conn.cursor()
    
    def create(self, prescription_data: dict) -> dict:
        """Crée une nouvelle prescription"""
        required_fields = ['patient_id', 'medication', 'dosage', 'frequency', 'duration']
        for field in required_fields:
            if field not in prescription_data:
                raise ValueError(f"Le champ {field} est obligatoire")

        query = """
            INSERT INTO prescriptions (
                patient_id, medical_record_id, medication, dosage, 
                frequency, duration, start_date, end_date, status,
                prescribed_by, prescribed_by_name, notes
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """
        
        try:
            self.cursor.execute(query, (
                prescription_data['patient_id'],
                prescription_data.get('medical_record_id'),
                prescription_data['medication'],
                prescription_data['dosage'],
                prescription_data['frequency'],
                prescription_data['duration'],
                prescription_data.get('start_date', date.today()),
                prescription_data.get('end_date'),
                prescription_data.get('status', 'active'),
                prescription_data.get('prescribed_by'),
                prescription_data.get('prescribed_by_name'),
                prescription_data.get('notes')
            ))
            result = self.cursor.fetchone()
            self.conn.commit()
            return self._row_to_dict(result)
        except psycopg2.Error as e:
            self.conn.rollback()
            raise e

    def update(self, prescription_id: int, update_data: dict) -> Optional[dict]:
        """Met à jour une prescription existante"""
        if 'status' in update_data and update_data['status'] not in self.VALID_STATUSES:
            raise ValueError("Statut invalide")

        set_clause = []
        values = []
        for key, value in update_data.items():
            set_clause.append(f"{key} = %s")
            values.append(value)
        
        values.append(prescription_id)
        
        query = f"""
            UPDATE prescriptions
            SET {', '.join(set_clause)}
            WHERE prescription_id = %s
            RETURNING *
        """
        
        try:
            self.cursor.execute(query, values)
            result = self.cursor.fetchone()
            self.conn.commit()
            return self._row_to_dict(result) if result else None
        except psycopg2.Error as e:
            self.conn.rollback()
            raise e

    def get_by_id(self, prescription_id: int) -> Optional[dict]:
        """Récupère une prescription par son ID"""
        query = "SELECT * FROM prescriptions WHERE prescription_id = %s"
        self.cursor.execute(query, (prescription_id,))
        result = self.cursor.fetchone()
        return self._row_to_dict(result) if result else None

    def get_by_patient(self, patient_id: int) -> list:
        """Récupère toutes les prescriptions d'un patient"""
        query = "SELECT * FROM prescriptions WHERE patient_id = %s ORDER BY start_date DESC"
        self.cursor.execute(query, (patient_id,))
        return [self._row_to_dict(row) for row in self.cursor.fetchall()]

    def _row_to_dict(self, row) -> dict:
        """Convertit une ligne de base de données en dictionnaire"""
        return {
            'prescription_id': row[0],
            'patient_id': row[1],
            'medical_record_id': row[2],
            'medication': row[3],
            'dosage': row[4],
            'frequency': row[5],
            'duration': row[6],
            'start_date': row[7],
            'end_date': row[8],
            'status': row[9],
            'prescribed_by': row[10],
            'prescribed_by_name': row[11],
            'notes': row[12]
        }

    def close(self):
        """Ferme la connexion à la base de données"""
        self.cursor.close()
        self.conn.close()