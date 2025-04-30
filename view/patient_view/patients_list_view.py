# views/patients/patient_list_view.py
import customtkinter as ctk
from tkinter import ttk
from utils.pdf_export import export_patients_to_pdf

class PatientListView(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Barre recherche + export
        top = ctk.CTkFrame(self)
        top.pack(fill='x', pady=5, padx=5)
        self.search_entry = ctk.CTkEntry(top, placeholder_text="Recherche...")
        self.search_entry.pack(side='left', padx=(0,5))
        ctk.CTkButton(top, text="🔍", command=self.refresh).pack(side='left')
        ctk.CTkButton(top, text="Export PDF", command=self.export_pdf).pack(side='right')

        # Tableau
        cols = ("ID","Code","Nom","Prénom","Naissance","Téléphone")
        self.tree = ttk.Treeview(self, columns=cols, show='headings')
        for c in cols:
            self.tree.heading(c, text=c)
        self.tree.pack(fill='both', expand=True, padx=5, pady=5)

        # Pagination
        nav = ctk.CTkFrame(self)
        nav.pack(fill='x', pady=5)
        self.page = 1
        ctk.CTkButton(nav, text="←", width=30, command=self.prev_page).pack(side='left', padx=5)
        ctk.CTkButton(nav, text="→", width=30, command=self.next_page).pack(side='right', padx=5)

        self.refresh()

    def refresh(self):
        search = self.search_entry.get().strip() or None
        data = self.controller.list_patients(page=self.page, per_page=15, search=search)
        for i in self.tree.get_children(): self.tree.delete(i)
        for p in data:
            self.tree.insert('', 'end', values=(
                p.patient_id, p.code_patient, p.last_name, p.first_name,
                p.birth_date, p.contact_phone
            ))

    def prev_page(self):
        if self.page > 1:
            self.page -= 1
            self.refresh()

    def next_page(self):
        self.page += 1
        self.refresh()

    def export_pdf(self):
        # récupère la page courante de résultats
        search = self.search_entry.get().strip() or None
        data = self.controller.list_patients(page=self.page, per_page=1000, search=search)
        export_patients_to_pdf(data, title="Liste des Patients")
