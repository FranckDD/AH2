from repositories.user_repo import UserRepository
from models.user import pwd_context  # Import du contexte de cryptage centralisé
from controller.patient_controller import PatientController
from repositories.patient_repo import PatientRepository
from controller.medical_controller import MedicalRecordController
from repositories.medical_repo import MedicalRecordRepository

class AuthController:
    def __init__(self):
        self.user_repo = UserRepository()
        self.current_user = None
        # sous-controllers initialisés après authentification
        self.patient_controller = None
        self.medical_record_controller = None

    def authenticate(self, username: str, password: str):
        try:
            user = self.user_repo.get_user_by_username(username)
            if not user:
                print(f"Utilisateur {username} non trouvé")
                return None
            if not user.is_active:
                print(f"Compte {username} désactivé")
                return None
            if not pwd_context.verify(password, user.password_hash):
                print(f"Échec de vérification du mot de passe pour {username}")
                return None

            self.current_user = user
            # instanciation des sous-controllers
            pat_repo = PatientRepository()
            self.patient_controller = PatientController(pat_repo, self.current_user)
            med_repo = MedicalRecordRepository()
            self.medical_record_controller = MedicalRecordController(
                repo=med_repo,
                patient_controller=self.patient_controller,
                current_user=self.current_user
            )
            return user
        except Exception as e:
            print(f"Erreur d'authentification pour {username}: {str(e)}")
            import traceback; traceback.print_exc()
            return None

    # pass-through pour Patients
    def list_patients(self, *args, **kwargs):
        return self.patient_controller.list_patients(*args, **kwargs)
    def get_patient(self, *args, **kwargs):
        return self.patient_controller.get_patient(*args, **kwargs)
    def create_patient(self, *args, **kwargs):
        return self.patient_controller.create_patient(*args, **kwargs)
    def update_patient(self, *args, **kwargs):
        return self.patient_controller.update_patient(*args, **kwargs)

    # pass-through pour Dossiers Médicaux
    def list_motifs(self, *args, **kwargs):
        return self.medical_record_controller.list_motifs(*args, **kwargs)
    def list_records(self, *args, **kwargs):
        return self.medical_record_controller.list_records(*args, **kwargs)
    def create_record(self, *args, **kwargs):
        return self.medical_record_controller.create_record(*args, **kwargs)
    def update_record(self, *args, **kwargs):
        return self.medical_record_controller.update_record(*args, **kwargs)
    def delete_record(self, *args, **kwargs):
        return self.medical_record_controller.delete_record(*args, **kwargs)
