import customtkinter as ctk
import tkinter as tk
import math

# Εισαγωγή των δικών σου αρχείων
import anemosData
import anemosCALC

ro = 1.25

# Ρυθμίσεις εμφάνισης
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class WindLoadApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Ρυθμίσεις Παραθύρου ---
        self.title("Υπολογισμός Φορτίων Ανέμου σε Στέγαστρα")
        self.geometry("1100x800")
        self.resizable(True, True)

        # --- ΔΙΑΤΑΞΗ GRID (2 Στήλες) ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # ==========================================
        # ΑΡΙΣΤΕΡΗ ΠΛΕΥΡΑ: INPUTS
        # ==========================================
        self.input_scroll = ctk.CTkScrollableFrame(self, label_text="Δεδομένα Εισαγωγής")
        self.input_scroll.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # === ΤΙΤΛΟΣ ===
        self.lbl_title = ctk.CTkLabel(
            self.input_scroll,
            text="Υπολογισμός Φορτίων Ανέμου\nσε Στέγαστρα",
            font=("Roboto", 20, "bold")
        )
        self.lbl_title.pack(pady=10)

        # === 1. ΔΕΔΟΜΕΝΑ ΑΝΕΜΟΥ & ΕΔΑΦΟΥΣ ===
        self.frm_wind = ctk.CTkFrame(self.input_scroll)
        self.frm_wind.pack(fill="x", pady=10, padx=5)

        ctk.CTkLabel(self.frm_wind, text="1. Ανεμος & Έδαφος", font=("Roboto", 14, "bold")).grid(row=0, column=0,
                                                                                                 columnspan=2,
                                                                                                 sticky="w", padx=10,
                                                                                                 pady=5)

        # Ζώνη
        ctk.CTkLabel(self.frm_wind, text="Ζώνη Ανέμου:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.zones_keys = list(anemosData.greece_zones_vb0.keys())
        self.cb_zone = ctk.CTkComboBox(self.frm_wind, values=self.zones_keys, width=150)
        self.cb_zone.grid(row=1, column=1, sticky="e", padx=10, pady=5)
        self.cb_zone.set(self.zones_keys[0])

        # Έδαφος
        ctk.CTkLabel(self.frm_wind, text="Κατηγορία Εδάφους:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.terrain_keys = list(anemosData.edafos.keys())
        self.cb_terrain = ctk.CTkComboBox(self.frm_wind, values=self.terrain_keys, width=150)
        self.cb_terrain.grid(row=2, column=1, sticky="e", padx=10, pady=5)
        self.cb_terrain.set("II")

        # === 2. ΓΕΩΜΕΤΡΙΑ ===
        self.frm_geo = ctk.CTkFrame(self.input_scroll)
        self.frm_geo.pack(fill="x", pady=10, padx=5)

        ctk.CTkLabel(self.frm_geo, text="2. Γεωμετρία", font=("Roboto", 14, "bold")).grid(row=0, column=0, columnspan=4,
                                                                                          sticky="w", padx=10, pady=5)

        self.entries_geo = {}
        fields = [
            ("Πλάτος b (m):", "10.0", 0),
            ("Βάθος d (m):", "15.0", 1),
            ("Ύψος h (m):", "6.0", 2),
            ("Γωνία α (°):", "5.0", 3)
        ]

        for i, (txt, val, r) in enumerate(fields):
            ctk.CTkLabel(self.frm_geo, text=txt).grid(row=r + 1, column=0, sticky="w", padx=10, pady=2)
            ent = ctk.CTkEntry(self.frm_geo, width=80, placeholder_text=val)
            ent.insert(0, val)
            ent.grid(row=r + 1, column=1, sticky="e", padx=10, pady=2)
            key = txt.split()[1]
            self.entries_geo[key] = ent

        # === 3. ΤΥΠΟΣ & ΣΥΝΤΕΛΕΣΤΕΣ ===
        self.frm_type = ctk.CTkFrame(self.input_scroll)
        self.frm_type.pack(fill="x", pady=10, padx=5)

        ctk.CTkLabel(self.frm_type, text="3. Τύπος & Συντελεστές", font=("Roboto", 14, "bold")).grid(row=0, column=0,
                                                                                                     columnspan=2,
                                                                                                     sticky="w",
                                                                                                     padx=10, pady=5)

        # Τύπος Στέγης
        ctk.CTkLabel(self.frm_type, text="Τύπος Στέγης:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
        self.cb_roof_type = ctk.CTkComboBox(self.frm_type, values=["Μονοκλινής", "Δικλινής"], width=150)
        self.cb_roof_type.grid(row=1, column=1, sticky="w", padx=10, pady=5)
        self.cb_roof_type.set("Μονοκλινής")

        # Φ (Εμπόδια)
        ctk.CTkLabel(self.frm_type, text="Εμπόδια (φ):").grid(row=2, column=0, sticky="w", padx=10, pady=5)
        self.seg_phi = ctk.CTkSegmentedButton(self.frm_type, values=["0 (Ανοιχτό)", "1 (Κλειστό)"])
        self.seg_phi.grid(row=2, column=1, sticky="w", padx=10, pady=5)
        self.seg_phi.set("0 (Ανοιχτό)")

        # Συντελεστές
        self.frm_coeffs = ctk.CTkFrame(self.frm_type, fg_color="transparent")
        self.frm_coeffs.grid(row=3, column=0, columnspan=2, pady=5, sticky="ew")

        for idx, (lbl, default) in enumerate([("c0", "1.0"), ("cs", "1.0"), ("sd", "1.0")]):
            ctk.CTkLabel(self.frm_coeffs, text=f"{lbl}:").pack(side="left", padx=(10, 2))
            ent = ctk.CTkEntry(self.frm_coeffs, width=40)
            ent.insert(0, default)
            ent.pack(side="left", padx=2)
            if lbl == "c0":
                self.ent_c0 = ent
            elif lbl == "cs":
                self.ent_cs = ent
            elif lbl == "sd":
                self.ent_sd = ent

        # === BUTTON ===
        self.btn_calc = ctk.CTkButton(
            self.input_scroll,
            text="ΥΠΟΛΟΓΙΣΜΟΣ",
            height=50,
            font=("Roboto", 18, "bold"),
            fg_color="#1f538d", hover_color="#14375e",
            command=self.calculate_loads
        )
        self.btn_calc.pack(pady=20, padx=10, fill="x")

        # ==========================================
        # ΔΕΞΙΑ ΠΛΕΥΡΑ: RESULTS
        # ==========================================
        self.frm_results = ctk.CTkFrame(self)
        self.frm_results.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        ctk.CTkLabel(self.frm_results, text="Αποτελέσματα", font=("Roboto", 18, "bold")).pack(pady=10)

        self.txt_result = ctk.CTkTextbox(self.frm_results, font=("Consolas", 14), wrap="word")
        self.txt_result.pack(fill="both", expand=True, padx=10, pady=(0, 10))

    def log(self, text):
        self.txt_result.insert(tk.END, text + "\n")

    # --- ΒΟΗΘΗΤΙΚΗ ΣΥΝΑΡΤΗΣΗ ΓΙΑ ΤΟ ΚΟΜΜΑ ---
    def get_float_safe(self, entry_widget):
        """
        Διαβάζει το κείμενο από το Entry, αντικαθιστά το ',' με '.'
        και επιστρέφει float.
        """
        val_str = entry_widget.get()
        if not val_str: return 0.0
        # ΑΝΤΙΚΑΤΑΣΤΑΣΗ ΚΟΜΜΑΤΟΣ ΜΕ ΤΕΛΕΙΑ
        val_str = val_str.replace(',', '.')
        return float(val_str)

    def calculate_loads(self):
        self.txt_result.delete("0.0", tk.END)  # Καθαρισμός

        try:
            # 1. Λήψη Δεδομένων Εισόδου
            zone_name = self.cb_zone.get()
            vb0 = anemosData.greece_zones_vb0[zone_name]

            terrain_cat = self.cb_terrain.get()
            z0 = anemosData.edafos[terrain_cat]["z0"]
            zmin = anemosData.edafos[terrain_cat]["zmin"]

            # Χρήση της safe συνάρτησης για να πιάνει το κόμμα
            b = self.get_float_safe(self.entries_geo['b'])
            d = self.get_float_safe(self.entries_geo['d'])
            z = self.get_float_safe(self.entries_geo['h'])
            alpha = self.get_float_safe(self.entries_geo['α'])

            roof_type = self.cb_roof_type.get()
            phi_str = self.seg_phi.get()
            phi = 0 if "0" in phi_str else 1

            c0 = self.get_float_safe(self.ent_c0)
            cs = self.get_float_safe(self.ent_cs)
            c_dir = self.get_float_safe(self.ent_sd)
            c_season = cs

            # 2. Υπολογισμοί
            vb = anemosCALC.calculate_vb(vb0, c_dir, c_season)
            kr = anemosCALC.calculate_kr(z0)
            cr = anemosCALC.calculate_cr(kr, z, z0, zmin)
            vm = anemosCALC.calculate_vm(cr, c0, vb)
            Iv = anemosCALC.calculate_In(z, zmin, z0, c0)
            qp = anemosCALC.calculate_qp(Iv, ro, vm)

            # Εκτύπωση
            self.log("=== ΑΠΟΤΕΛΕΣΜΑΤΑ ΥΠΟΛΟΓΙΣΜΟΥ ===")
            self.log(f"Ζώνη: {zone_name} (Vb0={vb0} m/s)")
            self.log(f"Έδαφος: {terrain_cat} (z0={z0}, zmin={zmin})")
            self.log(f"qp(z={z}m) = {qp:.3f} kN/m²\n")

            self.log(f"--- ΣΤΕΓΑΣΤΡΟ: {roof_type.upper()} (φ={phi}) ---")

            if roof_type == "Μονοκλινής":
                table = anemosData.canopy_mono
                aref = anemosCALC.calculate_Aref_mono(d, b, math.radians(alpha))
            else:
                table = anemosData.canopy_duo
                aref = anemosCALC.calculate_Aref_duo(d, b, math.radians(alpha))

            self.log(f"Εμβαδό Aref = {aref:.2f} m²")

            coeffs, success = anemosCALC.angle_data(table, alpha)

            if not success:
                self.log("ΠΡΟΣΟΧΗ: Η γωνία α είναι εκτός των ορίων του πίνακα!")
                return

            data_total = coeffs.get("total")
            data_phi = coeffs.get(phi, coeffs.get(float(phi)))

            if not data_total or not data_phi:
                self.log("Σφάλμα: Δεν βρέθηκαν συντελεστές για τα δεδομένα.")
                return

            cf_max = data_total["Cf"]
            f_max = qp * cf_max * aref
            cf_min = data_phi["Cf"]
            f_min = qp * cf_min * aref

            self.log("\n>>> ΣΥΝΟΛΙΚΕΣ ΔΥΝΑΜΕΙΣ (Global Forces)")
            self.log(f"F_max (Πίεση/Κάτω): {f_max:.2f} kN  (Cf={cf_max:.2f})")
            self.log(f"F_min (Ανύψωση/Πάνω): {f_min:.2f} kN  (Cf={cf_min:.2f})")

            self.log("\n>>> ΤΟΠΙΚΑ ΦΟΡΤΙΑ (Net Pressure Zones)")

            zones_max_str = []
            for k, v in data_total.items():
                if k != "Cf":
                    w = qp * v
                    zones_max_str.append(f"{k}: {w:.2f}")
            self.log(f"Ζώνες Max (kN/m²):\n  {', '.join(zones_max_str)}")

            zones_min_str = []
            for k, v in data_phi.items():
                if k != "Cf":
                    w = qp * v
                    zones_min_str.append(f"{k}: {w:.2f}")
            self.log(f"Ζώνες Min (kN/m²):\n  {', '.join(zones_min_str)}")

        except Exception as e:
            self.log(f"\nΣΦΑΛΜΑ ΔΕΔΟΜΕΝΩΝ: {str(e)}")
            self.log("Ελέγξτε ότι έχετε βάλει μόνο αριθμούς.")
            print(e)


if __name__ == "__main__":
    app = WindLoadApp()
    app.mainloop()