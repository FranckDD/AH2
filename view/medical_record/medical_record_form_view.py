# view/medical_record/medical_record_form_view.py
import tkinter as tk
import customtkinter as ctk
from datetime import datetime

class MedicalRecordFormView(ctk.CTkFrame):
    def __init__(self, parent, controller, current_user, record_id=None):
        super().__init__(parent)
        self.controller   = controller
        self.current_user = current_user
        self.record_id    = record_id

        # Layout en grille
        self.grid_columnconfigure(1, weight=1)

        # Titre
        title = "Éditer Soin Médical" if record_id else "Ajouter Soin Médical"
        ctk.CTkLabel(self, text=title, font=(None, 20, "bold"))\
            .grid(row=0, column=0, columnspan=2, pady=10)

        # Liste des champs (clé -> libellé)
        fields = [
            ("Patient ID",         "patient_id"),
            ("Date Consultation",  "consultation_date"),
            ("Statut matrimonial",  "marital_status"),
            ("Tension artérielle", "bp"),
            ("Température",        "temperature"),
            ("Poids (kg)",         "weight"),
            ("Taille (cm)",        "height"),
            ("Antécédents",        "medical_history"),
            ("Allergies",          "allergies"),
            ("Symptômes",          "symptoms"),
            ("Diagnostic",         "diagnosis"),
            ("Traitement",         "treatment"),
            ("Gravité",            "severity"),
            ("Notes",              "notes"),
            ("Motif code",         "motif_code"),
        ]
        self.entries = {}
        for idx, (label, key) in enumerate(fields, start=1):
            ctk.CTkLabel(self, text=label+":")\
                .grid(row=idx, column=0, padx=10, pady=5, sticky="e")
            e = ctk.CTkEntry(self, placeholder_text=label)
            e.grid(row=idx, column=1, padx=10, pady=5, sticky="ew")
            self.entries[key] = e

        # Boutons Enregistrer / Supprimer
        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=len(fields)+1, column=0, columnspan=2, pady=15)
        ctk.CTkButton(btn_frame, text="Enregistrer", command=self._on_save)\
            .pack(side="left", padx=10)
        if self.record_id:
            ctk.CTkButton(btn_frame, text="Supprimer", fg_color="#D32F2F",
                          command=self._on_delete).pack(side="right", padx=10)

        # Si édition, charger la fiche existante
        if self.record_id:
            self._load_record()

    def _load_record(self):
        rec = self.controller.get_medical_record(self.record_id)
        if not rec:
            return
        for key, widget in self.entries.items():
            val = getattr(rec, key, "")
            # formate la date si besoin
            if key == "consultation_date" and val:
                val = val.strftime("%Y-%m-%d %H:%M:%S")
            widget.delete(0, tk.END)
            widget.insert(0, val or "")

    def _collect_data(self):
        d = {}
        for key, widget in self.entries.items():
            text = widget.get().strip()
            d[key] = text or None
        # conversion types
        if d.get("consultation_date"):
            try:
                d["consultation_date"] = datetime.fromisoformat(d["consultation_date"])
            except ValueError:
                d["consultation_date"] = None
        for num in ("temperature","weight","height"):
            if d.get(num):
                try:
                    d[num] = float(d[num])
                except:
                    d[num] = None
        return d

    def _on_save(self):
        data = self._collect_data()
        if self.record_id:
            self.controller.update_medical_record(self.record_id, data, current_user=self.current_user)
        else:
            self.controller.create_medical_record(data, current_user=self.current_user)
        # puis retour éventuel

    def _on_delete(self):
        if self.record_id:
            self.controller.delete_medical_record(self.record_id)
        # puis retour éventuel
