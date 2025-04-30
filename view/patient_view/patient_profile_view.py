import tkinter as tk
import customtkinter as ctk
from tkinter import ttk

class PatientProfileView(ctk.CTkFrame):
    def __init__(self, parent, controller, patient_id):
        super().__init__(parent)
        self.controller = controller
        self.patient_id = patient_id

        # Onglets
        self.tabview = ctk.CTkTabview(self)
        for tab in ("Informations","Rendez-vous","Prescriptions","Examens labo","Consult. spirituelles"):
            self.tabview.add(tab)
        self.tabview.pack(fill="both", expand=True, padx=10, pady=10)

        # Construire chaque onglet
        self._build_info_tab()
        self._build_simple_list_tab("Rendez-vous", self.controller.get_appointments)
        self._build_simple_list_tab("Prescriptions", self.controller.get_prescriptions)
        self._build_simple_list_tab("Examens labo", self.controller.get_lab_results)
        self._build_simple_list_tab("Consult. spirituelles", self.controller.get_spiritual_consultations)

        # Charger les données
        self.load_patient()

    def _build_info_tab(self):
        info = self.tabview.tab("Informations")
        labels = [
            ("Code patient", "code_patient"),
            ("Prénom", "first_name"),
            ("Nom", "last_name"),
            ("Date Naiss.", "birth_date"),
            ("Genre", "gender"),
            ("Téléphone", "contact_phone"),
            ("Assurance", "assurance"),
            ("Résidence", "residence"),
            ("Nom Père", "father_name"),
            ("Nom Mère", "mother_name"),
            ("Créé le", "created_at"),
            ("Par", "created_by_name"),
        ]
        self.info_vars = {}
        for i, (txt, key) in enumerate(labels):
            ctk.CTkLabel(info, text=txt+":").grid(row=i, column=0, padx=5, pady=3, sticky="e")
            var = ctk.CTkLabel(info, text="")
            var.grid(row=i, column=1, padx=5, pady=3, sticky="w")
            self.info_vars[key] = var

    def _build_simple_list_tab(self, tab_name, fetch_func):
        """
        Pour les listes : Rendez-vous, Prescriptions, etc.
        fetch_func doit accepter patient_id et renvoyer une liste de dicts.
        """
        tab = self.tabview.tab(tab_name)
        cols = {
            "Rendez-vous": ("appointment_date","doctor_name","reason"),
            "Prescriptions": ("medication","dosage","start_date","end_date"),
            "Examens labo": ("test_type","test_date","status"),
            "Consult. spirituelles": ("prescription","consultation_date","notes")
        }[tab_name]
        tree = ttk.Treeview(tab, columns=cols, show="headings")
        for c in cols:
            tree.heading(c, text=c.replace("_"," ").title())
        tree.pack(fill="both", expand=True, padx=5, pady=5)
        setattr(self, f"tree_{tab_name.replace(' ','_')}", tree)
        setattr(self, f"fetch_{tab_name}", fetch_func)

    def load_patient(self):
        # Charger infos générales
        data = self.controller.get_patient(self.patient_id)
        if not data: return
        for key, var in self.info_vars.items():
            val = data.get(key)
            if isinstance(val, (list, dict)):
                var.configure(text=str(val))
            else:
                var.configure(text=val)

        # Charger chaque liste
        for tab_name in ("Rendez-vous","Prescriptions","Examens labo","Consult. spirituelles"):
            fetch = getattr(self, f"fetch_{tab_name}")
            tree  = getattr(self, f"tree_{tab_name.replace(' ','_')}")
            # Effacer l'existant
            for item in tree.get_children():
                tree.delete(item)
            # Insérer les nouvelles lignes
            for row in fetch(self.patient_id):
                tree.insert("", "end", values=tuple(row[col] for col in tree["columns"]))
