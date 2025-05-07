import tkinter as tk
import customtkinter as ctk
from PIL import Image
import os
import models

# Tes vues existantes
from view.doctor_views.doctors_dashboard_view import DoctorsDashboardView
from view.doctor_views.doctors_list_view import DoctorsListView
from view.doctor_views.doctors_edit_view import DoctorsEditView

from .patient_view.patients_dashboard_view import PatientsDashboardView
from .patient_view.patients_list_view import PatientListView
from .patient_view.patients_edit_view import PatientsEditView

from view.appointment_views.appointments_dashboard_view import AppointmentsDashboardView
from view.appointment_views.appointments_list_view import AppointmentsListView
from view.appointment_views.appointments_book_view import AppointmentsBookView

# Vues Dossier Médical
from view.medical_record.medical_record_form_view import MedicalRecordFormView
from view.medical_record.medical_record_list_view import MedicalRecordListView

# Vues Prescription
from view.prescription_views.prescription_form import PrescriptionFormView
from view.prescription_views.prescription_list_view import PrescriptionListView

#Auth_controller 
from repositories.patient_repo import PatientRepository
from controller.patient_controller    import PatientController

# Appliquer thème
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class DashboardView(ctk.CTkFrame):
    def __init__(self, parent, user, on_logout=None):
        super().__init__(parent)
        self.parent = parent
        self.user = user
        # juste après self.user = user
        repo = PatientRepository()
        self.patient_controller = PatientController(repo, user)
        self.on_logout = on_logout
        self.sidebar_expanded = True
        self.active_menu_btn = None

        # Configuration grille
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

        self._build_sidebar()
        self._build_topbar()
        self._build_content()

        # Affichage initial
        self.show_doctors_dashboard()

    def _build_sidebar(self):
        self.sidebar = ctk.CTkFrame(
            self, width=200, fg_color="#F8F9FA",
            border_width=1, border_color="#E0E0E0"
        )
        self.sidebar.grid(row=0, column=0, rowspan=2, sticky="nsew")
        self.sidebar.grid_propagate(False)

        # Toggle
        self.toggle_btn = ctk.CTkButton(
            self.sidebar, text="<", width=30,
            fg_color="transparent", command=self.toggle_sidebar
        )
        self.toggle_btn.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Logo + titre
        img = Image.open(os.path.join("assets", "logo_light.png"))
        logo_img = ctk.CTkImage(light_image=img, dark_image=img, size=(32,32))
        self.logo_label = ctk.CTkLabel(
            self.sidebar, image=logo_img, text=" One Health",
            compound="left", text_color="#333",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.logo_label.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        # Liste des boutons de section
        self.menu_buttons = []
        def make_section(row, title, items, toggle_fn):
            btn = ctk.CTkButton(
                self.sidebar, text=title, fg_color="transparent",
                text_color="#333", anchor="w", command=toggle_fn
            )
            btn.grid(row=row, column=0, padx=10, pady=5, sticky="ew")
            self.menu_buttons.append(btn)
            frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
            for txt, cmd in items:
                sub = ctk.CTkButton(
                    frame, text=txt, fg_color="transparent",
                    text_color="#333", anchor="w",
                    command=lambda c=cmd, b=btn: (self._set_active_menu(b), c())
                )
                sub.pack(fill="x", padx=25, pady=2)
                sub.bind("<Enter>", lambda e, w=sub: w.configure(text_color="#007bff"))
                sub.bind("<Leave>", lambda e, w=sub: w.configure(text_color="#333"))
            return btn, frame

        # Sections
        self.docs_btn, self.docs_sub = make_section(2, "Médecins", [
            ("Dashboard Médecins", self.show_doctors_dashboard),
            ("Liste Médecins", self.show_doctors_list),
            ("Ajouter/Éditer Médecin", self.show_doctors_edit),
        ], self._toggle_docs_sub)

        self.pats_btn, self.pats_sub = make_section(4, "Patients", [
            ("Dashboard Patients", self.show_patients_dashboard),
            ("Liste Patients", self.show_patients_list),
            ("Ajouter Patient", self.show_patient_add),
        ], self._toggle_pats_sub)

        self.apps_btn, self.apps_sub = make_section(6, "RDV", [
            ("Dashboard RDV", self.show_appointments_dashboard),
            ("Liste RDV", self.show_appointments_list),
            ("Prendre RDV", self.show_appointments_book),
        ], self._toggle_apps_sub)

        self.medrec_btn, self.medrec_sub = make_section(8, "Dossier Médical", [
            ("Enregistrer MR", self.show_medical_record_form),
            ("Liste MR", self.show_medical_record_list),
        ], self._toggle_medrec_sub)

        self.presc_btn, self.presc_sub = make_section(10, "Prescription", [
            ("Nouvelle Prescription", self.show_prescription_form),
            ("Liste Prescriptions", self.show_prescription_list),
        ], self._toggle_presc_sub)

    def _build_topbar(self):
        self.topbar = ctk.CTkFrame(
            self, height=60, fg_color="#007bff",
            corner_radius=0, border_width=1, border_color="#E0E0E0"
        )
        # topbar spans full width
        self.topbar.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.topbar.grid_propagate(False)
        for idx, w in enumerate((0,0,0,1,0,0)):
            self.topbar.grid_columnconfigure(idx, weight=w)

        # Logo + titre à gauche
        img_tb = Image.open(os.path.join("assets", "logo_light.png"))
        logo_tb_img = ctk.CTkImage(light_image=img_tb, dark_image=img_tb, size=(24,24))
        label_tb = ctk.CTkLabel(
            self.topbar, image=logo_tb_img, text=" One Health",
            compound="left", text_color="white",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        label_tb.grid(row=0, column=0, padx=10)

        # Burger
        burger = ctk.CTkButton(
            self.topbar, text="☰", width=30, height=30,
            fg_color="transparent", text_color="white",
            command=self.toggle_sidebar
        )
        burger.grid(row=0, column=1, padx=5)

        # Recherche plus courte
        self.search_entry = ctk.CTkEntry(
            self.topbar, placeholder_text="🔍 Rechercher…",
            width=150
        )
        self.search_entry.grid(row=0, column=2, padx=10)

        # Spacer
        spacer = ctk.CTkLabel(self.topbar, text="", fg_color="transparent")
        spacer.grid(row=0, column=3, sticky="ew")

        # Notifications
        notif = ctk.CTkButton(
            self.topbar, text="🔔", width=30, height=30,
            fg_color="transparent", text_color="white"
        )
        notif.grid(row=0, column=4, padx=5)

        # Profil
        self.profile_btn = ctk.CTkButton(
            self.topbar, text=self.user.full_name + " ▼",
            width=120, fg_color="transparent", text_color="white",
            command=self._open_profile_menu
        )
        self.profile_btn.grid(row=0, column=5, padx=10)

        # Menu contextuel
        self.profile_menu = tk.Menu(self.profile_btn, tearoff=0)
        for label, cmd in [("Paramètres", self._show_settings),
                           ("Éditer Profil", self._show_edit_profile),
                           ("Changer MDP", self._show_change_password)]:
            self.profile_menu.add_command(label=label, command=cmd)
        self.profile_menu.add_separator()
        self.profile_menu.add_command(label="Déconnexion", command=self._logout)

    def _build_content(self):
        # Contenu défilable avec CTkScrollableFrame
        self.content = ctk.CTkScrollableFrame(
            self, fg_color="#F5F5F5", corner_radius=0
        )
        self.content.grid(row=1, column=1, sticky="nsew", padx=(0,10), pady=(0,10))
        self.content.grid_columnconfigure(0, weight=1)

    def toggle_sidebar(self):
        if self.sidebar_expanded:
            self.sidebar.configure(width=60)
            self.toggle_btn.configure(text=">")
            self.logo_label.configure(text="")
            for btn in self.menu_buttons:
                btn.configure(text="")
            self._hide_all_submenus()
        else:
            self.sidebar.configure(width=200)
            self.toggle_btn.configure(text="<")
            self.logo_label.configure(text=" One Health")
            titles = ["Médecins","Patients","RDV","Dossier Médical","Prescription"]
            for btn, txt in zip(self.menu_buttons, titles): btn.configure(text=txt)
        self.sidebar_expanded = not self.sidebar_expanded

    def _hide_all_submenus(self):
        for f in [self.docs_sub, self.pats_sub, self.apps_sub, self.medrec_sub, self.presc_sub]: f.grid_forget()

    def _toggle_docs_sub(self):
        self._hide_all_submenus();
        self.docs_sub.grid(row=3, column=0, sticky="nw") if not self.docs_sub.winfo_ismapped() else self.docs_sub.grid_forget()
    def _toggle_pats_sub(self):
        self._hide_all_submenus();
        self.pats_sub.grid(row=5, column=0, sticky="nw") if not self.pats_sub.winfo_ismapped() else self.pats_sub.grid_forget()
    def _toggle_apps_sub(self):
        self._hide_all_submenus();
        self.apps_sub.grid(row=7, column=0, sticky="nw") if not self.apps_sub.winfo_ismapped() else self.apps_sub.grid_forget()
    def _toggle_medrec_sub(self):
        self._hide_all_submenus();
        self.medrec_sub.grid(row=9, column=0, sticky="nw") if not self.medrec_sub.winfo_ismapped() else self.medrec_sub.grid_forget()
    def _toggle_presc_sub(self):
        self._hide_all_submenus();
        self.presc_sub.grid(row=11, column=0, sticky="nw") if not self.presc_sub.winfo_ismapped() else self.presc_sub.grid_forget()

    def _clear_content(self):
        for w in self.content.winfo_children(): w.destroy()


    def _set_active_menu(self, btn):
        if self.active_menu_btn: self.active_menu_btn.configure(text_color="#333")
        btn.configure(text_color="#007bff"); self.active_menu_btn = btn

    # Médecins
    def show_doctors_dashboard(self):
        self._clear_content(); self._set_active_menu(self.docs_btn)
        DoctorsDashboardView(self.content).grid(sticky="nsew", padx=10, pady=10)
    def show_doctors_list(self):
        self._clear_content(); self._set_active_menu(self.docs_btn)
        DoctorsListView(self.content).grid(sticky="nsew", padx=10, pady=10)
    def show_doctors_edit(self):
        self._clear_content(); self._set_active_menu(self.docs_btn)
        DoctorsEditView(self.content).grid(sticky="nsew", padx=10, pady=10)

    # Patients
    def show_patients_dashboard(self):
        self._clear_content(); self._set_active_menu(self.pats_btn)
        PatientsDashboardView(self.content).grid(sticky="nsew", padx=10, pady=10)
    def show_patients_list(self):
        self._clear_content(); self._set_active_menu(self.pats_btn)
        PatientListView(self.content, self).grid(sticky="nsew", padx=10, pady=10)
    def show_patients_edit(self, patient_id=None):
        self._clear_content(); self._set_active_menu(self.pats_btn)
        PatientsEditView(self.content, self, self.user, patient_id).grid(sticky="nsew", padx=10, pady=10)

    # RDV
    def show_appointments_dashboard(self):
        self._clear_content(); self._set_active_menu(self.apps_btn)
        AppointmentsDashboardView(self.content).grid(sticky="nsew", padx=10, pady=10)
    def show_appointments_list(self):
        self._clear_content(); self._set_active_menu(self.apps_btn)
        AppointmentsListView(self.content).grid(sticky="nsew", padx=10, pady=10)
    def show_appointments_book(self):
        self._clear_content(); self._set_active_menu(self.apps_btn)
        AppointmentsBookView(self.content).grid(sticky="nsew", padx=10, pady=10)

    # Dossier Médical
    def show_medical_record_form(self):
        self._clear_content(); self._set_active_menu(self.medrec_btn)
        MedicalRecordFormView(
            self.content,
            controller=self.parent.controller).grid(sticky="nsew", padx=10, pady=10)
    def show_medical_record_list(self):
        self._clear_content(); self._set_active_menu(self.medrec_btn)
        MedicalRecordListView(self.content, controller=self.parent.controller).grid(sticky="nsew", padx=10, pady=10)

    # Prescription
    def show_prescription_form(self):
        self._clear_content(); self._set_active_menu(self.presc_btn)
        PrescriptionFormView(self.content, controller=self.parent.controller, current_user=self.user).grid(sticky="nsew", padx=10, pady=10)
    def show_prescription_list(self):
        self._clear_content(); self._set_active_menu(self.presc_btn)
        PrescriptionListView(self.content, controller=self.parent.controller).grid(sticky="nsew", padx=10, pady=10)

    # Profil
    def _open_profile_menu(self):
        x = self.profile_btn.winfo_rootx(); y = self.profile_btn.winfo_rooty() + self.profile_btn.winfo_height()
        self.profile_menu.tk_popup(x, y)
    def _show_settings(self): pass
    def _show_edit_profile(self): pass
    def _show_change_password(self): pass
    def _logout(self):
        if callable(self.on_logout): self.on_logout()

    def show_patient_add(self):
        self._clear_content()
        self._set_active_menu(self.pats_btn)
        from .patient_view.patient_form_view import PatientFormView
        form = PatientFormView(
            self.content,
            controller=self.patient_controller,  # <-- ici
            current_user=self.user,
            patient_id=None
        )
        form.grid(sticky="nsew", padx=10, pady=10)
