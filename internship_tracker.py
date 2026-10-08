import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector


DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "roshu1221"       
DB_NAME = "internship_tracker"


def create_database():

    try:
        con = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD
        )

        cursor = con.cursor()

        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS {DB_NAME}"
        )

        cursor.close()
        con.close()

    except mysql.connector.Error as e:

        messagebox.showerror(
            "MySQL Error",
            f"Cannot connect to MySQL.\n\n{e}"
        )


def connect_database():

    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

def create_table():

    try:

        con = connect_database()
        cursor = con.cursor()

        query = """
        CREATE TABLE IF NOT EXISTS applications (

            id INT AUTO_INCREMENT PRIMARY KEY,

            company_name VARCHAR(100) NOT NULL,

            internship_role VARCHAR(100) NOT NULL,

            location VARCHAR(100),

            internship_type VARCHAR(30),

            application_date DATE,

            deadline DATE,

            status VARCHAR(30),

            interview_date DATE,

            stipend VARCHAR(50),

            duration VARCHAR(50),

            website VARCHAR(255),

            notes TEXT
        )
        """

        cursor.execute(query)

        con.commit()

        cursor.close()
        con.close()

    except mysql.connector.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


root = tk.Tk()

root.title(
    "Digital Internship Application Tracker"
)

root.geometry("1250x700")

root.configure(
    bg="#f2f5f9"
)


company_var = tk.StringVar()
role_var = tk.StringVar()
location_var = tk.StringVar()
type_var = tk.StringVar()
application_date_var = tk.StringVar()
deadline_var = tk.StringVar()
status_var = tk.StringVar()
interview_date_var = tk.StringVar()
stipend_var = tk.StringVar()
duration_var = tk.StringVar()
website_var = tk.StringVar()
search_var = tk.StringVar()


def clear_fields():

    company_var.set("")
    role_var.set("")
    location_var.set("")
    type_var.set("")
    application_date_var.set("")
    deadline_var.set("")
    status_var.set("")
    interview_date_var.set("")
    stipend_var.set("")
    duration_var.set("")
    website_var.set("")

    notes_text.delete(
        "1.0",
        tk.END
    )


def add_application():

    if company_var.get().strip() == "":
        messagebox.showwarning(
            "Warning",
            "Enter Company Name."
        )
        return

    if role_var.get().strip() == "":
        messagebox.showwarning(
            "Warning",
            "Enter Internship Role."
        )
        return

    try:

        con = connect_database()
        cursor = con.cursor()

        query = """
        INSERT INTO applications
        (
            company_name,
            internship_role,
            location,
            internship_type,
            application_date,
            deadline,
            status,
            interview_date,
            stipend,
            duration,
            website,
            notes
        )
        VALUES
        (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
        """

        values = (

            company_var.get(),

            role_var.get(),

            location_var.get(),

            type_var.get(),

            application_date_var.get()
            if application_date_var.get()
            else None,

            deadline_var.get()
            if deadline_var.get()
            else None,

            status_var.get(),

            interview_date_var.get()
            if interview_date_var.get()
            else None,

            stipend_var.get(),

            duration_var.get(),

            website_var.get(),

            notes_text.get(
                "1.0",
                tk.END
            ).strip()
        )

        cursor.execute(
            query,
            values
        )

        con.commit()

        cursor.close()
        con.close()

        messagebox.showinfo(
            "Success",
            "Internship application added successfully."
        )

        clear_fields()

        load_data()

    except mysql.connector.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


def load_data():

    for item in application_table.get_children():

        application_table.delete(item)

    try:

        con = connect_database()

        cursor = con.cursor()

        cursor.execute(
            "SELECT * FROM applications ORDER BY id DESC"
        )

        rows = cursor.fetchall()

        for row in rows:

            application_table.insert(
                "",
                tk.END,
                values=row
            )

        cursor.close()
        con.close()

        update_dashboard()

    except mysql.connector.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


def search_application():

    search_value = search_var.get().strip()

    for item in application_table.get_children():

        application_table.delete(item)

    try:

        con = connect_database()

        cursor = con.cursor()

        query = """
        SELECT * FROM applications

        WHERE company_name LIKE %s

        OR internship_role LIKE %s

        OR location LIKE %s

        OR status LIKE %s
        """

        value = "%" + search_value + "%"

        cursor.execute(
            query,
            (
                value,
                value,
                value,
                value
            )
        )

        rows = cursor.fetchall()

        for row in rows:

            application_table.insert(
                "",
                tk.END,
                values=row
            )

        cursor.close()
        con.close()

    except mysql.connector.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )

def select_application(event):

    selected = application_table.focus()

    if not selected:
        return

    data = application_table.item(
        selected
    )

    values = data["values"]

    if not values:
        return

    company_var.set(values[1])
    role_var.set(values[2])
    location_var.set(values[3])
    type_var.set(values[4])
    application_date_var.set(values[5] or "")
    deadline_var.set(values[6] or "")
    status_var.set(values[7] or "")
    interview_date_var.set(values[8] or "")
    stipend_var.set(values[9] or "")
    duration_var.set(values[10] or "")
    website_var.set(values[11] or "")

    notes_text.delete(
        "1.0",
        tk.END
    )

    if values[12]:

        notes_text.insert(
            tk.END,
            values[12]
        )


def update_application():

    selected = application_table.focus()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Select an application first."
        )

        return

    data = application_table.item(
        selected
    )

    application_id = data["values"][0]

    try:

        con = connect_database()

        cursor = con.cursor()

        query = """
        UPDATE applications

        SET
        company_name=%s,
        internship_role=%s,
        location=%s,
        internship_type=%s,
        application_date=%s,
        deadline=%s,
        status=%s,
        interview_date=%s,
        stipend=%s,
        duration=%s,
        website=%s,
        notes=%s

        WHERE id=%s
        """

        values = (

            company_var.get(),

            role_var.get(),

            location_var.get(),

            type_var.get(),

            application_date_var.get()
            if application_date_var.get()
            else None,

            deadline_var.get()
            if deadline_var.get()
            else None,

            status_var.get(),

            interview_date_var.get()
            if interview_date_var.get()
            else None,

            stipend_var.get(),

            duration_var.get(),

            website_var.get(),

            notes_text.get(
                "1.0",
                tk.END
            ).strip(),

            application_id
        )

        cursor.execute(
            query,
            values
        )

        con.commit()

        cursor.close()
        con.close()

        messagebox.showinfo(
            "Success",
            "Application updated successfully."
        )

        clear_fields()

        load_data()

    except mysql.connector.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


def delete_application():

    selected = application_table.focus()

    if not selected:

        messagebox.showwarning(
            "Warning",
            "Select an application first."
        )

        return

    data = application_table.item(
        selected
    )

    application_id = data["values"][0]

    answer = messagebox.askyesno(
        "Delete",
        "Are you sure you want to delete this application?"
    )

    if not answer:
        return

    try:

        con = connect_database()

        cursor = con.cursor()

        cursor.execute(
            "DELETE FROM applications WHERE id=%s",
            (application_id,)
        )

        con.commit()

        cursor.close()
        con.close()

        messagebox.showinfo(
            "Success",
            "Application deleted successfully."
        )

        clear_fields()

        load_data()

    except mysql.connector.Error as e:

        messagebox.showerror(
            "Database Error",
            str(e)
        )


def update_dashboard():

    try:

        con = connect_database()

        cursor = con.cursor()

        cursor.execute(
            "SELECT COUNT(*) FROM applications"
        )

        total = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM applications
            WHERE status='Applied'
            """
        )

        applied = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM applications
            WHERE status='Shortlisted'
            """
        )

        shortlisted = cursor.fetchone()[0]

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM applications
            WHERE status='Selected'
            """
        )

        selected = cursor.fetchone()[0]

        cursor.close()
        con.close()

        total_label.config(
            text=f"Total Applications\n{total}"
        )

        applied_label.config(
            text=f"Applied\n{applied}"
        )

        shortlisted_label.config(
            text=f"Shortlisted\n{shortlisted}"
        )

        selected_label.config(
            text=f"Selected\n{selected}"
        )

    except mysql.connector.Error:
        pass



def logout():

    answer = messagebox.askyesno(
        "Exit",
        "Do you want to close the application?"
    )

    if answer:
        root.destroy()


header = tk.Frame(
    root,
    bg="#1f4e78",
    height=70
)

header.pack(
    fill="x"
)


title_label = tk.Label(
    header,
    text="Digital Internship Application Tracker",
    font=("Arial", 22, "bold"),
    bg="#1f4e78",
    fg="white"
)

title_label.pack(
    side="left",
    padx=20,
    pady=18
)


logout_button = tk.Button(
    header,
    text="Exit",
    command=logout,
    width=10
)

logout_button.pack(
    side="right",
    padx=20
)

dashboard = tk.Frame(
    root,
    bg="#f2f5f9"
)

dashboard.pack(
    fill="x",
    padx=20,
    pady=15
)


total_label = tk.Label(
    dashboard,
    text="Total Applications\n0",
    font=("Arial", 13, "bold"),
    width=20,
    height=3,
    bg="white",
    relief="groove"
)

total_label.pack(
    side="left",
    padx=5
)


applied_label = tk.Label(
    dashboard,
    text="Applied\n0",
    font=("Arial", 13, "bold"),
    width=20,
    height=3,
    bg="white",
    relief="groove"
)

applied_label.pack(
    side="left",
    padx=5
)


shortlisted_label = tk.Label(
    dashboard,
    text="Shortlisted\n0",
    font=("Arial", 13, "bold"),
    width=20,
    height=3,
    bg="white",
    relief="groove"
)

shortlisted_label.pack(
    side="left",
    padx=5
)


selected_label = tk.Label(
    dashboard,
    text="Selected\n0",
    font=("Arial", 13, "bold"),
    width=20,
    height=3,
    bg="white",
    relief="groove"
)

selected_label.pack(
    side="left",
    padx=5
)

form_frame = tk.LabelFrame(
    root,
    text=" Internship Application Details ",
    font=("Arial", 11, "bold"),
    bg="#f2f5f9"
)

form_frame.pack(
    fill="x",
    padx=20
)


# Row 1

tk.Label(
    form_frame,
    text="Company Name:",
    bg="#f2f5f9"
).grid(
    row=0,
    column=0,
    padx=5,
    pady=5
)

tk.Entry(
    form_frame,
    textvariable=company_var,
    width=22
).grid(
    row=0,
    column=1,
    padx=5
)


tk.Label(
    form_frame,
    text="Internship Role:",
    bg="#f2f5f9"
).grid(
    row=0,
    column=2,
    padx=5
)

tk.Entry(
    form_frame,
    textvariable=role_var,
    width=22
).grid(
    row=0,
    column=3,
    padx=5
)


tk.Label(
    form_frame,
    text="Location:",
    bg="#f2f5f9"
).grid(
    row=0,
    column=4,
    padx=5
)

tk.Entry(
    form_frame,
    textvariable=location_var,
    width=20
).grid(
    row=0,
    column=5,
    padx=5
)


# Row 2

tk.Label(
    form_frame,
    text="Internship Type:",
    bg="#f2f5f9"
).grid(
    row=1,
    column=0,
    padx=5,
    pady=5
)

type_combo = ttk.Combobox(
    form_frame,
    textvariable=type_var,
    values=[
        "Online",
        "Offline",
        "Hybrid"
    ],
    width=19,
    state="readonly"
)

type_combo.grid(
    row=1,
    column=1,
    padx=5
)


tk.Label(
    form_frame,
    text="Application Date:",
    bg="#f2f5f9"
).grid(
    row=1,
    column=2,
    padx=5
)

tk.Entry(
    form_frame,
    textvariable=application_date_var,
    width=22
).grid(
    row=1,
    column=3,
    padx=5
)


tk.Label(
    form_frame,
    text="Deadline:",
    bg="#f2f5f9"
).grid(
    row=1,
    column=4,
    padx=5
)

tk.Entry(
    form_frame,
    textvariable=deadline_var,
    width=20
).grid(
    row=1,
    column=5,
    padx=5
)


# Row 3

tk.Label(
    form_frame,
    text="Status:",
    bg="#f2f5f9"
).grid(
    row=2,
    column=0,
    padx=5,
    pady=5
)

status_combo = ttk.Combobox(
    form_frame,
    textvariable=status_var,
    values=[
        "Applied",
        "Shortlisted",
        "Interview",
        "Selected",
        "Rejected",
        "Withdrawn"
    ],
    width=19,
    state="readonly"
)

status_combo.grid(
    row=2,
    column=1,
    padx=5
)


tk.Label(
    form_frame,
    text="Interview Date:",
    bg="#f2f5f9"
).grid(
    row=2,
    column=2,
    padx=5
)

tk.Entry(
    form_frame,
    textvariable=interview_date_var,
    width=22
).grid(
    row=2,
    column=3,
    padx=5
)


tk.Label(
    form_frame,
    text="Stipend:",
    bg="#f2f5f9"
).grid(
    row=2,
    column=4,
    padx=5
)

tk.Entry(
    form_frame,
    textvariable=stipend_var,
    width=20
).grid(
    row=2,
    column=5,
    padx=5
)


# Row 4

tk.Label(
    form_frame,
    text="Duration:",
    bg="#f2f5f9"
).grid(
    row=3,
    column=0,
    padx=5,
    pady=5
)

tk.Entry(
    form_frame,
    textvariable=duration_var,
    width=22
).grid(
    row=3,
    column=1,
    padx=5
)


tk.Label(
    form_frame,
    text="Website:",
    bg="#f2f5f9"
).grid(
    row=3,
    column=2,
    padx=5
)

tk.Entry(
    form_frame,
    textvariable=website_var,
    width=22
).grid(
    row=3,
    column=3,
    padx=5
)


tk.Label(
    form_frame,
    text="Notes:",
    bg="#f2f5f9"
).grid(
    row=3,
    column=4,
    padx=5
)

notes_text = tk.Text(
    form_frame,
    width=20,
    height=3
)

notes_text.grid(
    row=3,
    column=5,
    padx=5,
    pady=5
)


button_frame = tk.Frame(
    root,
    bg="#f2f5f9"
)

button_frame.pack(
    fill="x",
    padx=20,
    pady=8
)


tk.Button(
    button_frame,
    text="Add Application",
    width=17,
    command=add_application
).pack(
    side="left",
    padx=5
)


tk.Button(
    button_frame,
    text="Update",
    width=12,
    command=update_application
).pack(
    side="left",
    padx=5
)


tk.Button(
    button_frame,
    text="Delete",
    width=12,
    command=delete_application
).pack(
    side="left",
    padx=5
)


tk.Button(
    button_frame,
    text="Clear",
    width=12,
    command=clear_fields
).pack(
    side="left",
    padx=5
)


search_frame = tk.Frame(
    root,
    bg="#f2f5f9"
)

search_frame.pack(
    fill="x",
    padx=20,
    pady=5
)


tk.Label(
    search_frame,
    text="Search:",
    font=("Arial", 10, "bold"),
    bg="#f2f5f9"
).pack(
    side="left"
)


tk.Entry(
    search_frame,
    textvariable=search_var,
    width=35
).pack(
    side="left",
    padx=5
)


tk.Button(
    search_frame,
    text="Search",
    width=12,
    command=search_application
).pack(
    side="left",
    padx=5
)


tk.Button(
    search_frame,
    text="Show All",
    width=12,
    command=load_data
).pack(
    side="left",
    padx=5
)


table_frame = tk.Frame(
    root,
    bg="#f2f5f9"
)

table_frame.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=10
)


columns = (
    "ID",
    "Company",
    "Role",
    "Location",
    "Type",
    "Application Date",
    "Deadline",
    "Status",
    "Interview Date",
    "Stipend",
    "Duration",
    "Website",
    "Notes"
)


application_table = ttk.Treeview(
    table_frame,
    columns=columns,
    show="headings"
)


for column in columns:

    application_table.heading(
        column,
        text=column
    )

    application_table.column(
        column,
        width=120
    )


application_table.column(
    "ID",
    width=50
)


application_table.column(
    "Company",
    width=130
)


application_table.column(
    "Role",
    width=130
)


application_table.column(
    "Notes",
    width=180
)


scroll_y = ttk.Scrollbar(
    table_frame,
    orient="vertical",
    command=application_table.yview
)

scroll_x = ttk.Scrollbar(
    table_frame,
    orient="horizontal",
    command=application_table.xview
)


application_table.configure(
    yscrollcommand=scroll_y.set,
    xscrollcommand=scroll_x.set
)


application_table.pack(
    side="top",
    fill="both",
    expand=True
)


scroll_y.pack(
    side="right",
    fill="y"
)


scroll_x.pack(
    side="bottom",
    fill="x"
)


application_table.bind(
    "<ButtonRelease-1>",
    select_application
)

create_database()
create_table()
load_data()
root.mainloop()