import tkinter as tk
from tkinter import ttk, messagebox, font as tkfont
import json, os
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk

PRIMARY_BG = "#F7F9FC"
CARD_BG = "#FFFFFF"
PRIMARY_ACCENT = "#007BFF"
SECONDARY_ACCENT = "#28A745"
TEXT_PRIMARY = "#212529"
TEXT_SECONDARY = "#6C757D"
BORDER_COLOR = "#DEE2E6"
GRAPH_LINE = "#007BFF"
BUTTON_HOVER = "#0056B3"
FONT_FAMILY = 'Helvetica'
FONT_SIZE_SMALL = 10
FONT_SIZE_MEDIUM = 12
FONT_SIZE_LARGE = 14
FONT_SIZE_XLARGE = 16
FONT_SIZE_XXLARGE = 20
FONT_SIZE_TITLE = 24
BORDER_RADIUS = 6
PADDING_SMALL = 5
PADDING_MEDIUM = 10
PADDING_LARGE = 15
PADDING_XLARGE = 20

DATA_FILE = "data/users.json"

os.makedirs("data", exist_ok=True)
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, "w") as f:
        json.dump({}, f)

def load_data():
    try:
        with open(DATA_FILE) as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError):
        return {}

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def calculate_bmi():
    username = username_var.get().strip()
    if not username:
        messagebox.showerror("Error", "Please enter a username.")
        return

    try:
        weight = float(weight_var.get())
        height = float(height_var.get()) / 100  

        if weight <= 0 or height <= 0:
            raise ValueError("Weight and height must be positive numbers")

        bmi = round(weight / (height ** 2), 1)
        
        if bmi < 18.5:
            category = "Underweight"
            category_color = "#3498db"  
        elif bmi < 24.9:
            category = "Normal"
            category_color = "#28A745"  
        elif bmi < 29.9:
            category = "Overweight"
            category_color = "#f39c12"  
        else:
            category = "Obese"
            category_color = "#e74c3c"  

        result_var.set(f"{bmi}")
        category_var.set(category)
        result_label.config(foreground=PRIMARY_ACCENT)
        category_label.config(foreground=TEXT_PRIMARY)

        
        data = load_data()
        record = {
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "weight": weight,
            "height": height * 100,  
            "bmi": bmi,
            "category": category
        }
        data.setdefault(username, []).append(record)
        save_data(data)
        update_history()
        plot_bmi_trend()

    except ValueError as e:
        messagebox.showerror("Error", "Please enter valid numbers.")

def update_history():
    username = username_var.get().strip()
    if not username:
        return
        
    data = load_data()
    history = data.get(username, [])
    history_text.config(state="normal")
    history_text.delete("1.0", tk.END)
    
    if not history:
        history_text.insert(tk.END, "Your BMI history will appear here")
    else:
        for rec in reversed(history[-5:]):  
            date_str = datetime.strptime(rec['date'], "%Y-%m-%d %H:%M:%S").strftime("%b %d, %H:%M")
            line = f"{date_str} | {rec['bmi']} ({rec['category']})\n"
            history_text.insert(tk.END, line)
    
    history_text.config(state="disabled")

def plot_bmi_trend():
    username = username_var.get().strip()
    if not username:
        return

    data = load_data()
    history = data.get(username, [])
    
    if not history:
        return

    for widget in chart_frame.winfo_children():
        widget.destroy()

    if len(history) < 2: 
        no_data_label = ttk.Label(chart_frame, 
                                text="At least 2 data points needed for trend",
                                foreground=TEXT_SECONDARY,
                                font=(FONT_FAMILY, FONT_SIZE_MEDIUM))
        no_data_label.pack(expand=True, pady=20)
        return

    dates = [rec["date"] for rec in history]
    bmis = [rec["bmi"] for rec in history]
    
    date_objs = [datetime.strptime(d, "%Y-%m-%d %H:%M:%S") for d in dates]
    
    fig = Figure(figsize=(6, 3), dpi=100, facecolor=CARD_BG)
    ax = fig.add_subplot(111)
    
    ax.set_facecolor(CARD_BG)
    
    line, = ax.plot(date_objs, bmis, color=GRAPH_LINE, linewidth=2, marker='o', markersize=6)
    
    fig.autofmt_xdate()
    
    ax.set_title('BMI Trend Over Time', pad=15, fontsize=FONT_SIZE_LARGE, 
                fontweight='bold', color=TEXT_PRIMARY)
    ax.set_ylabel('BMI', fontsize=FONT_SIZE_MEDIUM, color=TEXT_PRIMARY)
    ax.grid(True, linestyle='--', alpha=0.3, color=BORDER_COLOR)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(BORDER_COLOR)
    ax.spines['bottom'].set_color(BORDER_COLOR)
    ax.tick_params(axis='both', which='both', colors=TEXT_SECONDARY, 
                  labelsize=FONT_SIZE_SMALL)
    
    canvas = FigureCanvasTkAgg(fig, master=chart_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, 
                              pady=PADDING_MEDIUM)
    
    fig.tight_layout()

root = tk.Tk()
root.title("BMI Calculator")
root.geometry("900x600")
root.configure(bg=PRIMARY_BG)
root.minsize(800, 500)

style = ttk.Style()
style.theme_use('clam')

style.configure('TFrame', background=PRIMARY_BG)
style.configure('TLabel', background=PRIMARY_BG, 
               foreground=TEXT_PRIMARY, 
               font=(FONT_FAMILY, FONT_SIZE_MEDIUM))
style.configure('TButton', font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'bold'), 
                padding=(15, 8))
style.configure('TEntry', padding=8, fieldbackground=CARD_BG)
style.configure('TLabelFrame', background=PRIMARY_BG, 
               relief='flat', borderwidth=0)
style.configure('TLabelFrame.Label', background=PRIMARY_BG,
               foreground=TEXT_PRIMARY, 
               font=(FONT_FAMILY, FONT_SIZE_LARGE, 'bold'))

style.configure('Primary.TButton', 
               background=PRIMARY_ACCENT, 
               foreground='white',
               borderwidth=0,
               bordercolor=PRIMARY_ACCENT,
               focusthickness=3,
               focuscolor='none',
               padding=(15, 10))

style.map('Primary.TButton',
         background=[('active', BUTTON_HOVER)],
         foreground=[('active', 'white')])

style.configure('Secondary.TButton',
               background='white',
               foreground=TEXT_PRIMARY,
               borderwidth=1,
               bordercolor=BORDER_COLOR,
               padding=(15, 10))

style.map('Secondary.TButton',
         background=[('active', PRIMARY_BG)],
         foreground=[('active', TEXT_PRIMARY)])

main_container = ttk.Frame(root, style='TFrame')
main_container.pack(fill=tk.BOTH, expand=True, padx=PADDING_XLARGE, 
                   pady=PADDING_XLARGE)

left_panel = ttk.Frame(main_container, style='TFrame')
left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, 
               padx=(0, PADDING_LARGE))

right_panel = ttk.Frame(main_container, style='TFrame')
right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

title_frame = ttk.Frame(left_panel, style='TFrame')
title_frame.pack(fill=tk.X, pady=(0, PADDING_XLARGE * 1.5))

icon_label = ttk.Label(title_frame, text="📊", 
                      font=('Segoe UI', 28))
icon_label.pack(side=tk.LEFT, padx=(0, PADDING_MEDIUM))

title_label = ttk.Label(title_frame, text="BMI Calculator", 
                       font=(FONT_FAMILY, FONT_SIZE_TITLE, 'bold'),
                       foreground=PRIMARY_ACCENT)
title_label.pack(side=tk.LEFT)

input_frame = ttk.LabelFrame(left_panel, text="Enter Your Details", 
                           padding=(PADDING_LARGE, PADDING_LARGE, 
                                   PADDING_LARGE, PADDING_MEDIUM))
input_frame.pack(fill=tk.X, pady=(0, PADDING_LARGE))

username_var = tk.StringVar()
username_label = ttk.Label(input_frame, text="Username")
username_label.grid(row=0, column=0, sticky='w', 
                   pady=(0, PADDING_SMALL))
username_entry = ttk.Entry(input_frame, textvariable=username_var, 
                          font=(FONT_FAMILY, FONT_SIZE_MEDIUM))
username_entry.grid(row=0, column=1, sticky='ew', 
                   pady=(0, PADDING_MEDIUM), 
                   padx=(PADDING_MEDIUM, 0))

weight_var = tk.StringVar()
weight_label = ttk.Label(input_frame, text="Weight (kg)")
weight_label.grid(row=1, column=0, sticky='w', 
                 pady=PADDING_SMALL)
weight_entry = ttk.Entry(input_frame, textvariable=weight_var,
                        font=(FONT_FAMILY, FONT_SIZE_MEDIUM))
weight_entry.grid(row=1, column=1, sticky='ew', 
                 pady=PADDING_SMALL, 
                 padx=(PADDING_MEDIUM, 0))

height_var = tk.StringVar()
height_label = ttk.Label(input_frame, text="Height (cm)")
height_label.grid(row=2, column=0, sticky='w', 
                 pady=PADDING_SMALL)
height_entry = ttk.Entry(input_frame, textvariable=height_var,
                        font=(FONT_FAMILY, FONT_SIZE_MEDIUM))
height_entry.grid(row=2, column=1, sticky='ew', 
                 pady=PADDING_SMALL, 
                 padx=(PADDING_MEDIUM, 0))

input_frame.columnconfigure(1, weight=1)
input_frame.grid_rowconfigure(0, weight=1)
input_frame.grid_rowconfigure(1, weight=1)
input_frame.grid_rowconfigure(2, weight=1)

buttons_frame = ttk.Frame(left_panel, style='TFrame')
buttons_frame.pack(fill=tk.X, pady=(0, PADDING_LARGE))

calculate_btn = ttk.Button(buttons_frame, text="Calculate BMI", 
                         command=calculate_bmi,
                         style='Primary.TButton')
calculate_btn.pack(side=tk.LEFT, fill=tk.X, expand=True, 
                  padx=(0, PADDING_MEDIUM))

trend_btn = ttk.Button(buttons_frame, text="Show BMI Trend", 
                      command=plot_bmi_trend,
                      style='Secondary.TButton')
trend_btn.pack(side=tk.LEFT, fill=tk.X, expand=True)

result_frame = ttk.Frame(left_panel, style='TFrame')
result_frame.pack(fill=tk.X, pady=(0, PADDING_LARGE))

result_var = tk.StringVar()
result_var.set("-")
category_var = tk.StringVar()
category_var.set("")

result_title = ttk.Label(result_frame, text="Your BMI", 
                       font=(FONT_FAMILY, FONT_SIZE_LARGE))
result_title.pack()

result_label = ttk.Label(result_frame, textvariable=result_var, 
                       font=(FONT_FAMILY, 48, 'bold'),
                       foreground=PRIMARY_ACCENT)
result_label.pack()

category_label = ttk.Label(result_frame, textvariable=category_var, 
                         font=(FONT_FAMILY, FONT_SIZE_XLARGE),
                         foreground=TEXT_PRIMARY)
category_label.pack()

history_frame = ttk.LabelFrame(left_panel, text="Recent History", 
                             padding=PADDING_MEDIUM)
history_frame.pack(fill=tk.BOTH, expand=True)

history_text_frame = ttk.Frame(history_frame)
history_text_frame.pack(fill=tk.BOTH, expand=True)

scrollbar = ttk.Scrollbar(history_text_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

history_text = tk.Text(history_text_frame, wrap=tk.WORD, 
                      font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
                      bg=CARD_BG, fg=TEXT_PRIMARY,
                      relief='flat', bd=0,
                      yscrollcommand=scrollbar.set,
                      padx=PADDING_MEDIUM, pady=PADDING_MEDIUM)
history_text.pack(fill=tk.BOTH, expand=True)
history_text.insert(tk.END, "Your BMI history will appear here")
history_text.config(state="disabled")

scrollbar.config(command=history_text.yview)

chart_frame = ttk.Frame(right_panel, style='TFrame')
chart_frame.pack(fill=tk.BOTH, expand=True, padx=PADDING_MEDIUM, 
                pady=PADDING_MEDIUM)

initial_chart_label = ttk.Label(chart_frame, 
                              text="Your BMI trend will appear here",
                              font=(FONT_FAMILY, FONT_SIZE_MEDIUM, 'italic'),
                              foreground=TEXT_SECONDARY)
initial_chart_label.place(relx=0.5, rely=0.5, anchor='center')

main_container.columnconfigure(0, weight=1)
main_container.columnconfigure(1, weight=1)
main_container.rowconfigure(0, weight=1)

def on_enter_key(event):
    calculate_bmi()

root.bind('<Return>', on_enter_key)

username_entry.focus()

style.configure('TEntry',
               fieldbackground=CARD_BG,
               foreground=TEXT_PRIMARY,
               borderwidth=1,
               relief='solid',
               padding=8)

style.map('TEntry',
         fieldbackground=[('readonly', CARD_BG)],
         foreground=[('readonly', TEXT_SECONDARY)])

history_text.tag_configure('history', 
                         font=(FONT_FAMILY, FONT_SIZE_MEDIUM),
                         lmargin1=10,
                         lmargin2=10,
                         rmargin=10,
                         spacing1=5,
                         spacing3=5)
root.mainloop()
