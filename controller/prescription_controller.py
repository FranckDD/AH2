from typing import Optional, Tuple
from functools import wraps
import logging
from models.prescription import Prescription
from service.prescription_service import PrescriptionService

# Définir les exceptions personnalisées directement dans le fichier
class PermissionDeniedError(Exception):
    """Exception pour les accès non autorisés"""
    pass

class InvalidInputError(Exception):
    """Exception pour les données d'entrée invalides"""
    pass

class PrescriptionController:
    def __init__(self):
        self.service = PrescriptionService()
        self.logger = logging.getLogger(__name__)
        self.current_user = None

    def set_current_user(self, user):
        """Définit l'utilisateur actuellement authentifié"""
        self.current_user = user

    def require_permission(self, permission_name: str):
        """Décorateur pour vérifier les permissions (version corrigée)"""
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                # Le premier argument est 'self' pour les méthodes d'instance
                self_instance = args[0]
                if not self_instance.current_user or not hasattr(self_instance.current_user, 'has_permission') or \
                   not self_instance.current_user.has_permission(permission_name):
                    self_instance.logger.warning(
                        f"Tentative d'accès non autorisée à {func.__name__} "
                        f"par {getattr(self_instance.current_user, 'username', 'anonymous')}"
                    )
                    raise PermissionDeniedError(f"Permission '{permission_name}' requise")
                return func(*args, **kwargs)
            return wrapper
        return decorator

    @require_permission('create_prescription')
    def create_prescription(self, prescription_data: dict) -> Tuple[bool, Optional[Prescription], Optional[str]]:
        """
        Crée une nouvelle prescription
        Args:
            prescription_data: {
                'patient_id': int,
                'medication': str,
                'dosage': str,
                'frequency': str,
                'duration': str,
                'medical_record_id': Optional[int],
                'start_date': Optional[date],
                'end_date': Optional[date],
                'notes': Optional[str]
            }
        Returns:
            Tuple: (success: bool, prescription: Optional[Prescription], error_message: Optional[str])
        """
        try:
            # Validation améliorée
            required_fields = {
                'patient_id': int,
                'medication': str,
                'dosage': str,
                'frequency': str,
                'duration': str
            }
            
            for field, field_type in required_fields.items():
                if field not in prescription_data:
                    raise InvalidInputError(f"Champ obligatoire manquant: {field}")
                if not isinstance(prescription_data[field], field_type):
                    raise InvalidInputError(f"Type invalide pour {field}, attendu: {field_type.__name__}")

            # Ajout des métadonnées
            prescription_data.update({
                'created_by': self.current_user.user_id,
                'prescriber_name': f"{self.current_user.full_name} ({getattr(self.current_user, 'role', 'N/A')})"
            })

            prescription = self.service.create_prescription(prescription_data)
            
            self.logger.info(
                f"Prescription créée avec succès (ID: {prescription.prescription_id}) "
                f"par {self.current_user.username}"
            )
            return True, prescription, None

        except InvalidInputError as e:
            self.logger.warning(f"Erreur de validation: {str(e)}")
            return False, None, str(e)
        except Exception as e:
            self.logger.error(f"Erreur création prescription: {str(e)}", exc_info=True)
            return False, None, "Erreur interne lors de la création"

    @require_permission('view_prescriptions')
    def get_patient_prescriptions(self, patient_id: int) -> Tuple[bool, Optional[list], Optional[str]]:
        """Récupère toutes les prescriptions d'un patient"""
        try:
            if not isinstance(patient_id, int) or patient_id <= 0:
                raise InvalidInputError("ID patient invalide")

            prescriptions = self.service.get_prescriptions_by_patient(patient_id)
            return True, prescriptions, None
        except InvalidInputError as e:
            return False, None, str(e)
        except Exception as e:
            self.logger.error(f"Erreur récupération prescriptions: {str(e)}", exc_info=True)
            return False, None, "Erreur lors de la récupération"

    @require_permission('update_prescription')
    def update_prescription_status(self, prescription_id: int, new_status: str) -> Tuple[bool, Optional[str]]:
        """Met à jour le statut d'une prescription"""
        VALID_STATUSES = {'active', 'completed', 'cancelled'}
        
        try:
            if not isinstance(prescription_id, int) or prescription_id <= 0:
                raise InvalidInputError("ID prescription invalide")
            
            if new_status not in VALID_STATUSES:
                raise InvalidInputError(f"Statut invalide. Valeurs autorisées: {VALID_STATUSES}")

            update_data = {
                'status': new_status,
                'updated_by': self.current_user.user_id,
                'updated_at': 'NOW()'  # Serait converti par le service
            }

            success = self.service.update_prescription(prescription_id, update_data)
            return success, None
            
        except InvalidInputError as e:
            self.logger.warning(f"Erreur validation: {str(e)}")
            return False, str(e)
        except Exception as e:
            self.logger.error(f"Erreur mise à jour: {str(e)}", exc_info=True)
            return False, "Erreur interne"