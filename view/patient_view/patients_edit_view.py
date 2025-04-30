import tkinter as tk
import customtkinter as ctk
from datetime import datetime

class PatientsEditView(ctk.CTkFrame):
    def __init__(self, parent, controller, current_user, patient_id=None):
        super().__init__(parent)
        self.controller   = controller
        self.current_user = current_user
        self.patient_id   = patient_id

        # Layout
        self.grid_columnconfigure(1, weight=1)

        # Titre
        title = "Éditer un patient" if patient_id else "Ajouter un patient"
        ctk.CTkLabel(self, text=title, font=(None, 20, "bold")).grid(row=0, column=0, columnspan=2, pady=10)

        # Champs
        labels = [
            ("Prénom", "first_name"),
            ("Nom", "last_name"),
            ("Date Naiss. (YYYY-MM-DD)", "birth_date"),
            ("Genre", "gender"),
            ("N° national", "national_id"),
            ("Téléphone", "contact_phone"),
            ("Assurance", "assurance"),
            ("Résidence", "residence"),
            ("Nom Père", "father_name"),
            ("Nom Mère", "mother_name"),
        ]
        self.entries = {}
        for idx, (lbl, key) in enumerate(labels, start=1):
            ctk.CTkLabel(self, text=lbl+":").grid(row=idx, column=0, padx=10, pady=5, sticky="e")
            if key == "gender":
                var = tk.StringVar(value="Autre")
                widget = ctk.CTkOptionMenu(self, values=["Homme","Femme","Autre"], variable=var)
                widget.grid(row=idx, column=1, padx=10, pady=5, sticky="ew")
                self.entries[key] = var
            else:
                e = ctk.CTkEntry(self, placeholder_text=lbl)
                e.grid(row=idx, column=1, padx=10, pady=5, sticky="ew")
                self.entries[key] = e

        # Boutons
        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=len(labels)+1, column=0, columnspan=2, pady=15)
        ctk.CTkButton(btn_frame, text="Enregistrer", command=self._on_save).pack(side="left", padx=10)
        if patient_id:
            ctk.CTkButton(btn_frame, text="Supprimer", fg_color="#D32F2F", command=self._on_delete).pack(side="right", padx=10)

        # Si on édite, charger les données
        if self.patient_id:
            self._load_patient()

    def _load_patient(self):
        data = self.controller.get_patient(self.patient_id)
        if not data: return
        # Remplit les champs
        for key, widget in self.entries.items():
            val = data.get(key)
            if key == "birth_date" and val:
                val = val.strftime("%Y-%m-%d")
            if isinstance(widget, tk.StringVar):
                widget.set(val or "Autre")
            else:
                widget.delete(0, tk.END)
                widget.insert(0, val or "")

    def _collect_data(self):
        """Récupère les données du formulaire dans un dict."""
        d = {}
        for key, widget in self.entries.items():
            if isinstance(widget, tk.StringVar):
                d[key] = widget.get()
            else:
                d[key] = widget.get().strip() or None
        # Convertir birth_date
        try:
            d['birth_date'] = datetime.strptime(d['birth_date'], "%Y-%m-%d").date()
        except:
            d['birth_date'] = None
        return d

    def _on_save(self):
        data = self._collect_data()
        if self.patient_id:
            self.controller.update_patient(self.patient_id, data, current_user=self.current_user)
        else:
            new = self.controller.create_patient(data, current_user=self.current_user)
            self.patient_id = getattr(new, 'patient_id', None) or new
        # Après enregistrement, on peut rediriger vers la liste ou le profil
        # Par exemple :
        # self.master.show_list_view()

    def _on_delete(self):
        if self.patient_id:
            self.controller.delete_patient(self.patient_id)
            # Retour à la liste :
            # self.master.show_list_view()
