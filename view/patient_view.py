import customtkinter as ctk
from tkinter import messagebox

class PatientView(ctk.CTkFrame):
    def __init__(self, parent, controller, user):
        super().__init__(parent)
        self.controller = controller
        self.user = user
        self.create_widgets()
    
    def create_widgets(self):
        self.grid_columnconfigure(0, weight=1)
        
        # Champs de formulaire
        self.first_name = ctk.CTkEntry(self, placeholder_text="Prénom")
        self.last_name = ctk.CTkEntry(self, placeholder_text="Nom")
        self.birth_date = ctk.CTkEntry(self, placeholder_text="AAAA-MM-JJ")
        self.gender = ctk.CTkComboBox(self, values=["Homme", "Femme", "Autre"])
        
        # Bouton de soumission
        self.submit = ctk.CTkButton(self, text="Enregistrer", command=self.submit_form)
        
        # Positionnement
        self.first_name.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        self.last_name.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        self.birth_date.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        self.gender.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        self.submit.grid(row=4, column=0, padx=5, pady=20, sticky="ew")
    
    def submit_form(self):
        data = {
            'first_name': self.first_name.get(),
            'last_name': self.last_name.get(),
            'birth_date': self.birth_date.get(),
            'gender': self.gender.get(),
            'contact_phone': '',
            'residence': ''
        }
        
        try:
            self.controller.create_patient(data, self.user)
            messagebox.showinfo("Succès", "Patient créé avec succès")
        except Exception as e:
            messagebox.showerror("Erreur", str(e))