import tkinter as tk

class StudentAddEditPage:
    def __init__(self, root, student_page_instance, mode="add", index=None):
        self.root = root
        self.student_page = student_page_instance
        self.mode = mode
        self.index = index
        self.subjects = []


        self.vcmd = (self.root.register(self.validate_numeric), '%P')

        self.frame = tk.Frame(self.root, bg="#1e293b")
        self.frame.pack(fill="both", expand=True)

        title = "➕ Add New Student" if mode == "add" else "📝 Edit Student Data"

        header = tk.Frame(self.frame, bg="#334155")
        header.pack(fill="x", pady=(0, 20))
        
        tk.Button(header, text="⬅️ View Dashboard", bg="#475569", fg="white", 
                  command=self.back).pack(side="left", padx=10, pady=10)
        
        tk.Label(header, text=title,
                 bg="#334155", fg="white",
                 font=("Arial", 14, "bold")).pack(side="left", padx=20)

        # ================= UI LAYOUT =================
        form_container = tk.Frame(self.frame, bg="#1e293b")
        form_container.pack(pady=10)

        # Left Side: Info
        info_frame = tk.LabelFrame(form_container, text="Basic Information", bg="#1e293b", fg="#94a3b8", padx=20, pady=20)
        info_frame.grid(row=0, column=0, padx=20, sticky="n")

        tk.Label(info_frame, text="Full Name", bg="#1e293b", fg="white").pack(anchor="w")
        self.name = tk.Entry(info_frame, width=30)
        self.name.pack(pady=(0, 10))
        self.name.bind("<Return>", self.focus_next)

        tk.Label(info_frame, text="Academic Year", bg="#1e293b", fg="white").pack(anchor="w")
        self.year = tk.Entry(info_frame, width=30, validate="key", validatecommand=self.vcmd)
        self.year.pack(pady=(0, 10))
        self.year.bind("<Return>", self.focus_next)

        tk.Label(info_frame, text="Birth Date", bg="#1e293b", fg="white").pack(anchor="w")
        self.birth = tk.Entry(info_frame, width=30)
        self.birth.pack(pady=(0, 10))
        self.birth.bind("<Return>", self.focus_next)

        # Right Side: Subjects
        sub_frame = tk.LabelFrame(form_container, text="Grades & Subjects", bg="#1e293b", fg="#94a3b8", padx=20, pady=20)
        sub_frame.grid(row=0, column=1, padx=20, sticky="n")

        tk.Label(sub_frame, text="Subject Name", bg="#1e293b", fg="white").pack(anchor="w")
        self.sub_name = tk.Entry(sub_frame, width=20)
        self.sub_name.pack(pady=(0, 5))
        self.sub_name.bind("<Return>", self.focus_next)

        tk.Label(sub_frame, text="Score", bg="#1e293b", fg="white").pack(anchor="w")
        self.sub_score = tk.Entry(sub_frame, width=20, validate="key", validatecommand=self.vcmd)
        self.sub_score.pack(pady=(0, 5))
        self.sub_score.bind("<Return>", self.focus_next)

        tk.Button(sub_frame, text="Add Subject", bg="#10b981", fg="white",
                  command=self.add_subject).pack(pady=5)

        self.list = tk.Listbox(sub_frame, height=5, width=25, bg="#0f172a", fg="white")
        self.list.pack()

        sub_btns = tk.Frame(sub_frame, bg="#1e293b")
        sub_btns.pack(pady=5)

        tk.Button(sub_btns, text="✏️ Edit", bg="#f59e0b", fg="white", font=("Arial", 8),
                  command=self.edit_selected_subject).pack(side="left", padx=2)
        tk.Button(sub_btns, text="🗑️ Delete", bg="#ef4444", fg="white", font=("Arial", 8),
                  command=self.delete_selected_subject).pack(side="left", padx=2)

        # Bottom Save Button
        tk.Button(self.frame, text="💾 Save Student Data",
                 bg="#1e293b", fg="white",
                 font=("Arial", 12, "bold"),
                 command=self.save).pack(pady=30, ipadx=20, ipady=10)
        
        # ================= EDIT LOAD =================
        if mode == "edit":
            s = self.student_page.students[index]
            self.name.insert(0, s["name"])
            self.year.insert(0, s["year"])
            self.birth.insert(0, s["birth"])
            self.subjects = s.get("subjects", [])
            self.refresh_subjects()

    def back(self):
        self.frame.destroy()
        self.student_page.frame.pack(fill="both", expand=True)

    def validate_numeric(self, P):
        return P == "" or P.isdigit()

    def focus_next(self, event):
        event.widget.tk_focusNext().focus()
        return "break"

    def add_subject(self):
        name = self.sub_name.get().strip()
        score = self.sub_score.get().strip()

        if not name or not score:
            return

        try:
            score_val = int(score)
            if score_val < 0 or score_val > 100:
                self.student_page.app.toast("Score must be between 0 and 100 ⚠️")
                return
                
            self.subjects.append({
                "name": name,
                "score": score_val
            })
        except ValueError:
            self.student_page.app.toast("Please enter a valid number for score ❌")
            return

        self.refresh_subjects()

        self.sub_name.delete(0, "end")
        self.sub_score.delete(0, "end")

    def edit_selected_subject(self):
        selection = self.list.curselection()
        if not selection:
            return

        index = selection[0]
        subject = self.subjects.pop(index)

        self.sub_name.delete(0, "end")
        self.sub_name.insert(0, subject["name"])
        self.sub_score.delete(0, "end")
        self.sub_score.insert(0, str(subject["score"]))

        self.refresh_subjects()

    def delete_selected_subject(self):
        selection = self.list.curselection()
        if selection:
            self.subjects.pop(selection[0])
            self.refresh_subjects()

    def refresh_subjects(self):
        self.list.delete(0, "end")
        for s in self.subjects:
            self.list.insert("end", f"{s['name']} - {s['score']}")

    def save(self):
        name = self.name.get().strip()
        year = self.year.get().strip()
        birth = self.birth.get().strip()

        if not name or not year or not birth:
            self.student_page.app.toast("Please fill all basic information ❌")
            return
        student = {
           "name": name,
            "year": year,
            "birth": birth,
            "subjects": self.subjects
        }

        if self.mode == "add":
            self.student_page.students.append(student)
        else:
            self.student_page.students[self.index] = student

        self.student_page.save()
        self.student_page.refresh()
        self.back()
        # rgthj