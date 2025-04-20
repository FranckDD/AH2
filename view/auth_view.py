import customtkinter as ctk
from PIL import Image

class AuthView(ctk.CTk):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.dashboard = None  # Référence future

        # Configuration de la fenêtre
        self.title("One Health - Authentification")
        self.geometry("400x600")
        self.resizable(False, False)
        
        self._setup_ui()

    def _setup_ui(self):
        # Style
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("dark-blue")  # or "green", "blue"
        #ctk.set_default_color_theme("assets/theme.json")
        
        # Layout principal
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.pack(expand=True, fill="both", padx=40, pady=40)

        # Logo
        self.logo = ctk.CTkImage(
            light_image=Image.open("assets/logo_light.png"),
            dark_image=Image.open("assets/logo_dark.png"),
            size=(150, 150)
        )
        ctk.CTkLabel(self.main_frame, image=self.logo, text="").pack(pady=20)

        # Formulaire
        self.username_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Nom d'utilisateur",
            height=50,
            corner_radius=10
        )
        self.username_entry.pack(fill="x", pady=10)

        self.password_entry = ctk.CTkEntry(
            self.main_frame,
            placeholder_text="Mot de passe",
            show="•",
            height=50,
            corner_radius=10
        )
        self.password_entry.pack(fill="x", pady=10)

        # Bouton de connexion
        self.login_btn = ctk.CTkButton(
            self.main_frame,
            text="Se connecter",
            height=50,
            corner_radius=10,
            command=self._on_login
        )
        self.login_btn.pack(fill="x", pady=20)

        # Lien d'inscription
        self.register_link = ctk.CTkLabel(
            self.main_frame,
            text="Créer un compte",
            text_color="#3B82F6",
            cursor="hand2"
        )
        self.register_link.pack()
        self.register_link.bind("<Button-1>", lambda e: self._show_register())


    def _open_dashboard(self, user):
            from view.dashboard_view import DashboardView
            
            # 1. Cache la fenêtre actuelle sans la détruire
            self.withdraw()  
            
            # 2. Crée le dashboard
            dashboard = DashboardView(user)
            
            # 3. Configure la fermeture propre
            dashboard.protocol("WM_DELETE_WINDOW", lambda: self._on_dashboard_close(dashboard))
            
            # 4. Transfert le contrôle au dashboard
            dashboard.mainloop()
            
    def _on_login(self):
            try:
                username = self.username_entry.get().strip()
                password = self.password_entry.get().strip()
                
                if not username or not password:
                    raise ValueError("Tous les champs sont obligatoires")
                    
                user = self.controller.authenticate(username, password)
                if user is None:
                    raise ValueError("Identifiants incorrects")
                
                self._open_dashboard(user)
                
            except Exception as e:
                self._show_error(str(e))  # <-- Doit être dans la classe AuthView

    

    def _show_error(self, message):
            # Supprimer les anciens messages d'erreur
            for widget in self.main_frame.winfo_children():
                if isinstance(widget, ctk.CTkFrame) and widget._fg_color == "#FEE2E2":
                    widget.destroy()
            
            # Afficher le nouveau message
            error_frame = ctk.CTkFrame(self.main_frame, fg_color="#FEE2E2")
            ctk.CTkLabel(
                error_frame,
                text=message,
                text_color="#DC2626"
            ).pack(padx=10, pady=5)
            error_frame.pack(fill="x", pady=10)

    def _on_dashboard_close(self, dashboard):
        """Gère la fermeture du dashboard"""
        # 1. Détruit le dashboard
        dashboard.destroy()
        
        # 2. Réaffiche la fenêtre de login
        self.deiconify()