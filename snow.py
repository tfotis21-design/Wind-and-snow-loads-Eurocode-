import customtkinter as ctk

# Ρυθμίσεις εμφάνισης
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class SnowLoadApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Ρυθμίσεις παραθύρου
        self.title("Υπολογισμός Φορτίων Χιονιού (ΕΝ 1991-1-3) - Ελλάδα")
        self.geometry("1100x700")
        self.resizable(True, True)

        # --- Grid Layout ---
        self.grid_columnconfigure(0, weight=2)  # Αριστερά (Inputs)
        self.grid_columnconfigure(1, weight=3)  # Δεξιά (Results)
        self.grid_rowconfigure(1, weight=1)

        # --- Τίτλος ---
        self.lbl_title = ctk.CTkLabel(self, text="Υπολογισμός Φορτίου Χιονιού (ΕΝ 1991-1-3)",
                                      font=("Roboto Medium", 24))
        self.lbl_title.grid(row=0, column=0, columnspan=2, pady=(20, 10), padx=10)

        # ============================================================
        # INPUT FRAME (Αριστερά)
        # ============================================================
        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.grid(row=1, column=0, padx=20, pady=10, sticky="nsew")
        self.left_frame.grid_columnconfigure(1, weight=1)

        # --- 1. Περιοχή & Γεωμετρία ---
        self.lbl_sec1 = ctk.CTkLabel(self.left_frame, text="1. Δεδομένα Περιοχής", font=("Roboto", 16, "bold"))
        self.lbl_sec1.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))

        # Ζώνη
        self.lbl_zone = ctk.CTkLabel(self.left_frame, text="Ζώνη Χιονιού:")
        self.lbl_zone.grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.combo_zone = ctk.CTkComboBox(self.left_frame, values=["Ζώνη 1 (0.4)", "Ζώνη 2 (0.8)", "Ζώνη 3 (1.7)"])
        self.combo_zone.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
        self.combo_zone.set("Ζώνη 1 (0.4)")

        # Υψόμετρο
        self.lbl_alt = ctk.CTkLabel(self.left_frame, text="Υψόμετρο (m):")
        self.lbl_alt.grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_alt = ctk.CTkEntry(self.left_frame, placeholder_text="π.χ. 150")
        self.entry_alt.grid(row=2, column=1, sticky="ew", padx=5, pady=5)

        # Συντελεστές
        self.lbl_ce = ctk.CTkLabel(self.left_frame, text="Συντ. Ce:")
        self.lbl_ce.grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.combo_ce = ctk.CTkComboBox(self.left_frame,
                                        values=["1.0 (Κανονικό)", "0.8 (Εκτεθειμένο)", "1.2 (Προστατευμένο)"])
        self.combo_ce.grid(row=3, column=1, sticky="ew", padx=5, pady=5)

        self.lbl_ct = ctk.CTkLabel(self.left_frame, text="Συντ. Ct:")
        self.lbl_ct.grid(row=4, column=0, sticky="w", padx=5, pady=5)
        self.entry_ct = ctk.CTkEntry(self.left_frame)
        self.entry_ct.insert(0, "1.0")
        self.entry_ct.grid(row=4, column=1, sticky="ew", padx=5, pady=5)

        # --- 2. Γεωμετρία Στέγης ---
        self.lbl_sec2 = ctk.CTkLabel(self.left_frame, text="2. Γεωμετρία Στέγης", font=("Roboto", 16, "bold"))
        self.lbl_sec2.grid(row=5, column=0, columnspan=2, sticky="w", pady=(20, 5))

        # Τύπος Στέγης
        self.lbl_type = ctk.CTkLabel(self.left_frame, text="Τύπος:")
        self.lbl_type.grid(row=6, column=0, sticky="w", padx=5, pady=5)
        self.roof_types = [
            "Επίπεδη (Flat)",
            "Μονοκλινής (Monopitch)",
            "Δικλινής (^ Shape)",
            "Δικλινής Ανεστραμμένη (V Shape - Κοιλάδα)"
        ]
        self.combo_type = ctk.CTkComboBox(self.left_frame, values=self.roof_types,
                                          command=self.update_inputs_visibility)
        self.combo_type.grid(row=6, column=1, sticky="ew", padx=5, pady=5)

        # Γωνία Α (Αριστερά ή Μοναδική)
        self.lbl_alpha1 = ctk.CTkLabel(self.left_frame, text="Γωνία α1 (°):")
        self.lbl_alpha1.grid(row=7, column=0, sticky="w", padx=5, pady=5)
        self.entry_alpha1 = ctk.CTkEntry(self.left_frame, placeholder_text="0")
        self.entry_alpha1.grid(row=7, column=1, sticky="ew", padx=5, pady=5)

        # Γωνία Β (Δεξιά - μόνο για δικλινείς)
        self.lbl_alpha2 = ctk.CTkLabel(self.left_frame, text="Γωνία α2 (°):")
        self.lbl_alpha2.grid(row=8, column=0, sticky="w", padx=5, pady=5)
        self.entry_alpha2 = ctk.CTkEntry(self.left_frame, placeholder_text="0")
        self.entry_alpha2.grid(row=8, column=1, sticky="ew", padx=5, pady=5)

        # Κουμπί
        self.btn_calc = ctk.CTkButton(self.left_frame, text="ΥΠΟΛΟΓΙΣΜΟΣ", command=self.calculate,
                                      height=50, font=("Roboto", 16, "bold"), fg_color="#106A43", hover_color="#148F5C")
        self.btn_calc.grid(row=9, column=0, columnspan=2, pady=30, sticky="ew")

        # ============================================================
        # OUTPUT FRAME (Δεξιά)
        # ============================================================
        self.right_frame = ctk.CTkFrame(self, border_width=1, border_color="#555")
        self.right_frame.grid(row=1, column=1, padx=20, pady=10, sticky="nsew")

        self.lbl_res_title = ctk.CTkLabel(self.right_frame, text="Αποτελέσματα & Φορτίσεις",
                                          font=("Roboto", 18, "bold"))
        self.lbl_res_title.pack(pady=10)

        self.results_box = ctk.CTkTextbox(self.right_frame, font=("Consolas", 14), activate_scrollbars=True)
        self.results_box.pack(fill="both", expand=True, padx=10, pady=10)
        self.results_box.configure(state="disabled")

        # Αρχική ρύθμιση πεδίων
        self.update_inputs_visibility("Επίπεδη (Flat)")

    def update_inputs_visibility(self, choice):
        """Εμφανίζει/Κρύβει τη δεύτερη γωνία ανάλογα με τον τύπο στέγης"""
        if "Επίπεδη" in choice:
            self.entry_alpha1.delete(0, "end")
            self.entry_alpha1.insert(0, "0")
            self.entry_alpha1.configure(state="disabled")
            self.entry_alpha2.configure(state="disabled", fg_color="#333")
        elif "Μονοκλινής" in choice:
            self.entry_alpha1.configure(state="normal")
            self.entry_alpha2.delete(0, "end")
            self.entry_alpha2.configure(state="disabled", fg_color="#333")
        else:
            # Δικλινείς (V ή ^)
            self.entry_alpha1.configure(state="normal")
            self.entry_alpha2.configure(state="normal", fg_color=["#F9F9FA", "#343638"])

    def get_mu1(self, alpha):
        """Υπολογισμός συντελεστή μορφής μ1 βάσει ΕΝ 1991-1-3 Πίνακας 5.2"""
        if 0 <= alpha <= 30:
            return 0.8
        elif 30 < alpha < 60:
            return 0.8 * (60 - alpha) / 30.0
        else:
            return 0.0

    def get_mu2(self, alpha):
        """Υπολογισμός συντελεστή μορφής μ2 (για κοιλάδες)"""
        # Σημείωση: Ο τύπος είναι ενδεικτικός βάσει Ευρωκώδικα για συσσώρευση
        if 0 <= alpha <= 30:
            return 0.8 + ((0.8 * alpha) / 30)
        elif 30 < alpha < 60:
            return 1.6
        else:
            return 0.0  # Πρακτικά δεν συσσωρεύεται χιόνι σε πολύ απότομες κλίσεις

    def calculate(self):
        try:
            # --- 1. Λήψη Δεδομένων (ΜΕ ΔΙΟΡΘΩΣΗ ΚΟΜΜΑΤΟΣ) ---
            zone_txt = self.combo_zone.get()
            sk0 = 0.4 if "Ζώνη 1" in zone_txt else (0.8 if "Ζώνη 2" in zone_txt else 1.7)

            # Αντικατάσταση ',' με '.' στο Υψόμετρο
            A_txt = self.entry_alt.get().replace(",", ".")
            if not A_txt: raise ValueError("Λείπει το υψόμετρο")
            A = float(A_txt)

            ce_val = float(self.combo_ce.get().split()[0])

            # Αντικατάσταση ',' με '.' στον Ct
            ct_txt = self.entry_ct.get().replace(",", ".")
            ct_val = float(ct_txt) if ct_txt else 1.0

            roof_type = self.combo_type.get()

            # Αντικατάσταση ',' με '.' στις Γωνίες
            raw_a1 = self.entry_alpha1.get().replace(",", ".")
            raw_a2 = self.entry_alpha2.get().replace(",", ".")

            a1 = float(raw_a1) if raw_a1 else 0.0
            a2 = float(raw_a2) if raw_a2 else 0.0

            # --- 2. Υπολογισμός Sk (Φορτίο Εδάφους) ---
            # Sk = Sk0 * [1 + (A/917)^2]
            Sk = sk0 * (1 + (A / 917) ** 2)

            # --- 3. Υπολογισμοί ανά Τύπο Στέγης ---
            res_text = f"*** ΔΕΔΟΜΕΝΑ ΥΠΟΛΟΓΙΣΜΟΥ ***\n"
            res_text += f"Ζώνη: {zone_txt} | Υψόμετρο: {A}m\n"
            res_text += f"Sk (έδαφος) = {Sk:.3f} kN/m²\n"
            res_text += f"Ce = {ce_val} | Ct = {ct_val}\n"
            res_text += "-" * 50 + "\n\n"

            mu1_a1 = self.get_mu1(a1)
            mu1_a2 = self.get_mu1(a2)
            mu2 = self.get_mu2(a1)  # Χρήση της μέσης κλίσης συνήθως, εδώ απλοποιημένα με a1

            if "Επίπεδη" in roof_type or "Μονοκλινής" in roof_type:
                # Μία Περίπτωση Φόρτισης
                s = mu1_a1 * ce_val * ct_val * Sk
                res_text += f"ΤΥΠΟΣ: {roof_type}\n"
                res_text += f"Γωνία: {a1}° --> μ1 = {mu1_a1:.3f}\n\n"
                res_text += ">> ΠΕΡΙΠΤΩΣΗ ΦΟΡΤΙΣΗΣ (Μοναδική):\n"
                res_text += f"   S = {s:.3f} kN/m²  (Ομοιόμορφο)\n"

            elif "Δικλινής (^ Shape)" in roof_type:
                # Τρεις Περιπτώσεις Φόρτισης (Εικόνα 1)
                res_text += f"ΤΥΠΟΣ: Δικλινής (^)\n"
                res_text += f"Κλίση Αριστερά: {a1}° (μ1={mu1_a1:.3f})\n"
                res_text += f"Κλίση Δεξιά:    {a2}° (μ1={mu1_a2:.3f})\n\n"

                # Case I: Full
                s_left_1 = mu1_a1 * ce_val * ct_val * Sk
                s_right_1 = mu1_a2 * ce_val * ct_val * Sk

                # Case II: 50% Left, 100% Right
                s_left_2 = 0.5 * s_left_1
                s_right_2 = s_right_1

                # Case III: 100% Left, 50% Right
                s_left_3 = s_left_1
                s_right_3 = 0.5 * s_right_1

                res_text += ">> CASE (i) - Πλήρης Φόρτιση:\n"
                res_text += f"   Αριστερά: {s_left_1:.3f} kN/m²\n"
                res_text += f"   Δεξιά:    {s_right_1:.3f} kN/m²\n\n"

                res_text += ">> CASE (ii) - Μετακίνηση (Drift) Δεξιά:\n"
                res_text += f"   Αριστερά: {s_left_2:.3f} kN/m² (50%)\n"
                res_text += f"   Δεξιά:    {s_right_2:.3f} kN/m² (100%)\n\n"

                res_text += ">> CASE (iii) - Μετακίνηση (Drift) Αριστερά:\n"
                res_text += f"   Αριστερά: {s_left_3:.3f} kN/m² (100%)\n"
                res_text += f"   Δεξιά:    {s_right_3:.3f} kN/m² (50%)\n"

            elif "V Shape" in roof_type:
                # Κοιλάδα (Valley) - Εικόνα 2
                res_text += f"ΤΥΠΟΣ: Δικλινής Ανεστραμμένη (V - Κοιλάδα)\n"
                res_text += "Προσοχή: Υπολογισμός συσσώρευσης στην υδρορροή.\n\n"

                s_slope_left = mu1_a1 * ce_val * ct_val * Sk
                s_slope_right = mu1_a2 * ce_val * ct_val * Sk
                s_valley = mu2 * ce_val * ct_val * Sk

                res_text += ">> ΦΟΡΤΙΑ ΣΧΕΔΙΑΣΜΟΥ:\n"
                res_text += f"   Στις κλίσεις (Ομοιόμορφο):\n"
                res_text += f"   - Αριστερά (S1): {s_slope_left:.3f} kN/m²\n"
                res_text += f"   - Δεξιά (S2):    {s_slope_right:.3f} kN/m²\n\n"
                res_text += f"   Στην Κοιλάδα (S_valley) - Συσσώρευση:\n"
                res_text += f"   - Συντελεστής μ2: {mu2:.2f}\n"
                res_text += f"   - Φορτίο Κέντρου: {s_valley:.3f} kN/m²\n"
                res_text += "   (Το φορτίο μειώνεται γραμμικά προς τις κορυφές)"

            # Εμφάνιση αποτελεσμάτων
            self.results_box.configure(state="normal")
            self.results_box.delete("0.0", "end")
            self.results_box.insert("0.0", res_text)
            self.results_box.configure(state="disabled")

        except ValueError as e:
            self.results_box.configure(state="normal")
            self.results_box.delete("0.0", "end")
            self.results_box.insert("0.0", "ΣΦΑΛΜΑ: Ελέγξτε ότι όλα τα πεδία έχουν αριθμούς.\n" + str(e))
            self.results_box.configure(state="disabled")


if __name__ == "__main__":
    app = SnowLoadApp()
    app.mainloop()