# views/patients/patient_form_view.py
import tkinter as tk
import customtkinter as ctk
from datetime import datetime

class PatientFormView(ctk.CTkFrame):
    def __init__(self, parent, controller, current_user, patient_id=None):
        super().__init__(parent)
        self.controller   = controller
        self.current_user = current_user
        self.patient_id   = patient_id

        # Grille des champs
        fields = [
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
        self.vars = {}
        for i,(label,key) in enumerate(fields):
            ctk.CTkLabel(self, text=label).grid(row=i, column=0, padx=5, pady=5, sticky='e')
            if key=="gender":
                var = tk.StringVar(value="Autre")
                widget = ctk.CTkOptionMenu(self, values=["Homme","Femme","Autre"], variable=var)
                widget.grid(row=i, column=1, padx=5, pady=5, sticky='w')
                self.vars[key] = var
            else:
                e = ctk.CTkEntry(self)
                e.grid(row=i, column=1, padx=5, pady=5, sticky='ew')
                self.vars[key] = e

        btn = ctk.CTkButton(self, text="Enregistrer", command=self._save)
        btn.grid(row=len(fields), column=0, columnspan=2, pady=10)

        if patient_id:
            self._load()

    def _load(self):
        p = self.controller.get_patient(self.patient_id)
        for key,widget in self.vars.items():
            val = p.get(key)
            if key=="birth_date" and val:
                val = val.strftime("%Y-%m-%d")
            if isinstance(widget, tk.StringVar):
                widget.set(val or "Autre")
            else:
                widget.delete(0,'end')
                widget.insert(0,val or "")

    def _save(self):
        data = {}
        for key,widget in self.vars.items():
            if isinstance(widget, tk.StringVar):
                data[key] = widget.get()
            else:
                data[key] = widget.get().strip() or None
        # conversion date
        try:
            data['birth_date'] = datetime.strptime(data['birth_date'],"%Y-%m-%d").date()
        except:
            data['birth_date'] = None

        if self.patient_id:
            self.controller.update_patient(self.patient_id, data)
        else:
            new_id = self.controller.create_patient(data)
            self.patient_id = new_id
        # retour à la liste
        self.master.show_patient_list()
