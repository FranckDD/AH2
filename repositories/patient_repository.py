class PatientRepository:
    def __init__(self, db_manager):
        self.db = db_manager
    
    def create_patient(self, patient_data, user_id):
        """
        Crée un patient via la procédure stockée PostgreSQL en utilisant des tuples
        
        Args:
            patient_data (dict): Doit contenir:
                - first_name (str)
                - last_name (str)
                - birth_date (str/date)
                - gender (str)
                - contact_phone (str)
                - residence (str)
                - national_id (str, optionnel)
                - assurance (str, optionnel)
            user_id (int): ID utilisateur (pour audit)
            
        Returns:
            bool: True si succès
            
        Raises:
            ValueError: Si données manquantes
            Exception: Erreurs DB
        """
        # Validation des champs obligatoires
        required = ['first_name', 'last_name', 'birth_date', 
                  'gender', 'contact_phone', 'residence']
        missing = [field for field in required if field not in patient_data]
        if missing:
            raise ValueError(f"Champs obligatoires manquants: {', '.join(missing)}")

        # Préparation des paramètres sous forme de tuple
        params = (
            patient_data['first_name'],
            patient_data['last_name'],
            patient_data['birth_date'],
            patient_data['gender'],
            patient_data['contact_phone'],
            patient_data['residence'],
            patient_data.get('national_id'),  # Optionnel
            patient_data.get('assurance')     # Optionnel
        )

        # Exécution avec gestion propre des ressources
        with self.db.get_connection() as conn:
            try:
                conn.execute(
                    "CALL create_patient(%s, %s, %s, %s, %s, %s, %s, %s)",
                    params  # Tuple de paramètres positionnels
                )
                conn.commit()
                return True
            except Exception as e:
                conn.rollback()
                # Log technique détaillé
                print(f"[ERREUR DB] create_patient failed: {e}\nParams: {params}")
                raise  # Propagation contrôlée