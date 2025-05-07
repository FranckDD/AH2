import tkinter as tk
import customtkinter as ctk
from datetime import datetime
from tkcalendar import DateEntry

class MedicalRecordFormView(ctk.CTkFrame):
    def __init__(self, parent, controller, record_id=None):
        super().__init__(parent)
        # Unwrap controller
        if hasattr(controller, 'medical_record_controller'):
            self.controller = controller.medical_record_controller
        else:
            self.controller = controller
        self.record_id = record_id
        self.current_user = getattr(controller, 'current_user', None)

        # Layout
        self.grid_columnconfigure(1, weight=1)
        # Recherche patient
        search_frame = ctk.CTkFrame(self)
        search_frame.grid(row=0, column=0, columnspan=6, pady=5, sticky='ew')
        search_frame.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(search_frame, text="Rechercher Patient (ID ou Code):").grid(row=0, column=0)
        self.search_entry = ctk.CTkEntry(search_frame, placeholder_text="ID ou Code")
        self.search_entry.grid(row=0, column=1, padx=5, sticky='ew')
        ctk.CTkButton(search_frame, text="🔍", command=self._on_search).grid(row=0, column=2, padx=5)

        # Affichage des infos du patient trouvé
        ctk.CTkLabel(search_frame, text="ID:").grid(row=1, column=0, sticky='e', padx=5)
        self.patient_id_var = tk.StringVar()
        ctk.CTkLabel(search_frame, textvariable=self.patient_id_var).grid(row=1, column=1, sticky='w', padx=5)
        ctk.CTkLabel(search_frame, text="Code:").grid(row=1, column=2, sticky='e', padx=5)
        self.patient_code_var = tk.StringVar()
        ctk.CTkLabel(search_frame, textvariable=self.patient_code_var).grid(row=1, column=3, sticky='w', padx=5)
        ctk.CTkLabel(search_frame, text="Nom:").grid(row=1, column=4, sticky='e', padx=5)
        self.patient_name_var = tk.StringVar()
        ctk.CTkLabel(search_frame, textvariable=self.patient_name_var).grid(row=1, column=5, sticky='w', padx=5)

        # Champs de formulaire
        fields = [
            ("Date Consultation",  "consultation_date"),
            ("Statut matrimonial", "marital_status"),
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
        ]
        self.entries = {}

        # mapping statut matrimonial FR/EN → BD
        self.marital_options = [
            ("Single / Célibataire", "Single"),
            ("Married / Marié(e)",    "Married"),
            ("Divorced / Divorcé(e)", "Divorced"),
            ("Widowed / Veuf(ve)",    "Widowed")
        ]
        # mapping gravité FR/EN → BD
        self.severity_options = [
            ("Low / Faible",   "low"),
            ("Medium / Moyen", "medium"),
            ("High / Élevé",   "high")
        ]

        # Motif mapping code → label and inverse
        motifs = self.controller.list_motifs()
        # list of codes, e.g. ['consultation', ...]
        codes = [m['code'] for m in motifs]
        # map code to label_fr
        self.code_to_label = {m['code']: m['label_fr'] for m in motifs}
        # inverse map label → code
        self.label_to_code = {label:code for code,label in self.code_to_label.items()}

        for idx, (label, key) in enumerate(fields, start=2):
            ctk.CTkLabel(self, text=label+":").grid(row=idx, column=0, padx=10, pady=5, sticky='e')
            if key == 'consultation_date':
                widget = DateEntry(self, date_pattern='yyyy-mm-dd')
                widget.grid(row=idx, column=1, padx=10, pady=5, sticky='ew')
            elif key == 'marital_status':
                self.marital_var = tk.StringVar()
                widget = ctk.CTkOptionMenu(self, values=[opt[0] for opt in self.marital_options], variable=self.marital_var)
                widget.grid(row=idx, column=1, padx=10, pady=5, sticky='ew')
            elif key == 'severity':
                self.severity_var = tk.StringVar()
                widget = ctk.CTkOptionMenu(self, values=[opt[0] for opt in self.severity_options], variable=self.severity_var)
                widget.grid(row=idx, column=1, padx=10, pady=5, sticky='ew')
            elif key == 'notes':
                widget = ctk.CTkTextbox(self, width=400, height=80)
                widget.grid(row=idx, column=1, padx=10, pady=5, sticky='ew')
            else:
                widget = ctk.CTkEntry(self, placeholder_text=label)
                widget.grid(row=idx, column=1, padx=10, pady=5, sticky='ew')
            self.entries[key] = widget

        # Motif de consultation
        ctk.CTkLabel(self, text="Motif:").grid(row=idx+1, column=0, sticky='e', padx=10)
        # display labels
        labels = [self.code_to_label[code] for code in codes]
        self.motif_var = tk.StringVar(value=labels[0] if labels else '')
        self.motif_menu = ctk.CTkOptionMenu(self, values=labels, variable=self.motif_var)
        self.motif_menu.grid(row=idx+1, column=1, padx=10, pady=5, sticky='ew')

        # Boutons
        btn_frame = ctk.CTkFrame(self)
        btn_frame.grid(row=idx+2, column=0, columnspan=6, pady=15)
        ctk.CTkButton(btn_frame, text="Enregistrer", command=self._on_save).pack(side='left', padx=10)
        if self.record_id:
            ctk.CTkButton(btn_frame, text="Supprimer", fg_color="#D32F2F", command=self._on_delete).pack(side='right', padx=10)

        # Chargement si édition
        if self.record_id:
            self._load_record()

    def _on_search(self):
        q = self.search_entry.get().strip()
        rec = self.controller.find_patient(q)
        if rec:
            pid = rec['patient_id'] if isinstance(rec, dict) else rec.patient_id
            self.patient_id_var.set(str(pid))
            code = rec['code_patient'] if isinstance(rec, dict) else rec.code_patient
            self.patient_code_var.set(code)
            name = f"{rec.get('last_name','') if isinstance(rec, dict) else rec.last_name} {(rec.get('first_name','') if isinstance(rec, dict) else rec.first_name)}"
            self.patient_name_var.set(name)
        else:
            self.patient_id_var.set('')
            self.patient_code_var.set('')
            self.patient_name_var.set('')

    def _on_save(self):
        data = {}
        # 1. patient_id
        pid = self.patient_id_var.get()
        if not pid.isdigit():
            return self._show_error("Patient non sélectionné")
        data['patient_id'] = int(pid)
        # 2. consultation_date
        raw = self.entries['consultation_date'].get()
        try:
            data['consultation_date'] = datetime.strptime(raw, "%Y-%m-%d")
        except:
            data['consultation_date'] = None
        # 3. marital_status
        disp = self.marital_var.get()
        data['marital_status'] = next(val for d,val in self.marital_options if d==disp)
        # 4-7 numeric/text
        for key in ('bp','temperature','weight','height','medical_history','allergies','symptoms','diagnosis','treatment'):
            w = self.entries[key]
            data[key] = (w.get() if hasattr(w,'get') else w.get("1.0","end")).strip() or None
        # 8. severity
        disp_s = self.severity_var.get()
        data['severity'] = next(val for d,val in self.severity_options if d==disp_s)
        # 9. notes
        notes_widget = self.entries['notes']
        data['notes'] = notes_widget.get("1.0","end").strip() or None
        # 10. motif_code (map label→code)
        lab = self.motif_var.get()
        data['motif_code'] = self.label_to_code.get(lab)
        # 11‑14 audit
        if self.current_user:
            data['created_by'] = self.current_user.user_id
            data['created_by_name'] = self.current_user.username
            data['last_updated_by'] = self.current_user.user_id
            data['last_updated_by_name'] = self.current_user.username
        else:
            data['created_by'] = data['created_by_name'] = None
            data['last_updated_by'] = data['last_updated_by_name'] = None
        # call
        try:
            if self.record_id:
                self.controller.update_record(self.record_id, data)
            else:
                self.controller.create_record(data)
            self._show_info("Enregistrement réussi")
        except Exception as e:
            self._show_error(f"Erreur : {e}")

    def _on_delete(self):
        if not self.record_id: return
        try:
            self.controller.delete_record(self.record_id)
            self._show_info("Supprimé")
        except Exception as e:
            self._show_error(f"Erreur suppression : {e}")

    def _load_record(self):
        rec = self.controller.get_record(self.record_id)
        if not rec: return
        pid = rec['patient_id'] if isinstance(rec, dict) else rec.patient_id
        self.patient_id_var.set(str(pid))
        # fill entries
        for key, widget in self.entries.items():
            val = rec[key] if isinstance(rec, dict) else getattr(rec, key)
            if key == 'notes':
                widget.delete("1.0","end"); widget.insert("1.0", val or '')
            else:
                widget.delete(0, tk.END); widget.insert(0, val or '')
        # set selects
        label = self.code_to_label.get(rec['motif_code'] if isinstance(rec, dict) else rec.motif_code)
        self.motif_var.set(label)
        self.marital_var.set(next(d for d,v in self.marital_options if v==rec.get('marital_status')))
        self.severity_var.set(next(d for d,v in self.severity_options if v==rec.get('severity')))

    def _show_error(self, msg):
        ctk.CTkLabel(self, text=msg, text_color="red").grid(row=0, column=0, columnspan=6, pady=5)
    def _show_info(self, msg):
        ctk.CTkLabel(self, text=msg, text_color="green").grid(row=0, column=0, columnspan=6, pady=5)
