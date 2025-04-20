import customtkinter as ctk
from PIL import Image

class DashboardView(ctk.CTk):
    def __init__(self, user):
        super().__init__()
        self.user = user
        
        # Configuration de la fenêtre
        self.title(f"One Health - Bienvenue {user.full_name}")
        self.geometry("800x600")
        
        self._setup_ui()

        # Gestion de la fermeture
        self.protocol("WM_DELETE_WINDOW", self._on_close)
    

    def _setup_ui(self):
        # Style
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")
        
        # Layout principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        # En-tête avec infos utilisateur
        header_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        header_frame.pack(fill="x", pady=10)
        
        # Message de bienvenue personnalisé
        welcome_msg = f"Bienvenue, {self.user.full_name}!\n"
        welcome_msg += f"Rôle: {self.user.role.name}\n"
        welcome_msg += self._get_role_specific_message()
        
        ctk.CTkLabel(
            header_frame,
            text=welcome_msg,
            font=("Arial", 14),
            justify="left"
        ).pack(side="left", padx=10)

        # Contenu spécifique au rôle
        self._setup_role_specific_ui()

    def _get_role_specific_message(self):
        messages = {
            "admin": "Vous avez accès à toutes les fonctionnalités du système.",
            "medecin": "Accès aux dossiers patients et prescriptions.",
            "nurse": "Accès aux soins et suivis patients.",
            "secretaire": "Accès à la gestion des rendez-vous."
        }
        return messages.get(self.user.role.name.lower(), "Bienvenue dans l'application One Health.")

    def _setup_role_specific_ui(self):
        """Ajoute des composants spécifiques au rôle"""
        if self.user.role.name.lower() == "admin":
            self._setup_admin_ui()
        elif self.user.role.name.lower() == "medecin":
            self._setup_doctor_ui()
        # ... autres rôles

    def _setup_admin_ui(self):
        # Exemple pour l'admin
        tabview = ctk.CTkTabview(self.main_frame)
        tabview.pack(expand=True, fill="both", padx=10, pady=10)
        
        tabview.add("Utilisateurs")
        tabview.add("Statistiques")
        tabview.add("Paramètres")

    def _on_close(self):
            """Ferme proprement l'application"""
            self.destroy()