import tkinter as tk
import random
import time
from ParkingLot import ParkingLot

# ====================== Colors ======================
ROOT_BG = '#2c3e50'
KIOSK_BG = '#ffffff'
MAP_BG = '#ecf0f1'
FREE_COLOR = '#27ae60'
OCCUPIED_COLOR = '#e74c3c'
TEXT_COLOR = '#2d3436'
BTN_BG = '#3498db'
BTN_FG = 'white'
SCANNER_BG = '#dfe6e9'
TERM_BG = '#34495e'
TERM_FG = '#ecf0f1'
SEPARATOR_COLOR = '#b0b8c1'
# ====================================================

spot_ids = ['A-1', 'A-2', 'A-3', 'B-1', 'B-2', 'B-3']
lot = ParkingLot(spot_ids)

root = tk.Tk()
root.title("One-Way Parking Kiosk")
root.geometry("800x620")
root.resizable(True, True)
root.configure(bg=ROOT_BG)

# ----- Top container (kiosk + map) -----
top_frame = tk.Frame(root, bg=ROOT_BG)
top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

# ----- Left panel (kiosk) -----
left_frame = tk.Frame(top_frame, bg=KIOSK_BG, width=260, height=400,
                      highlightbackground=SEPARATOR_COLOR, highlightthickness=2)
left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(10, 0), pady=10)
left_frame.pack_propagate(False)

# ---------- Kiosk top status strip ----------
status_frame = tk.Frame(left_frame, bg='#2c3e50', height=30)
status_frame.pack(fill=tk.X)
status_frame.pack_propagate(False)

tk.Label(status_frame, text="●", fg='#27ae60', bg='#2c3e50', font=('Arial', 12)).pack(side=tk.LEFT, padx=(10, 5))
tk.Label(status_frame, text="System Online", fg='white', bg='#2c3e50', font=('Arial', 10, 'bold')).pack(side=tk.LEFT)

# Vertical separator (thin line between kiosk and map)
separator = tk.Frame(top_frame, bg=SEPARATOR_COLOR, width=2)
separator.pack(side=tk.LEFT, fill=tk.Y, padx=(3, 3), pady=10)

# Title
tk.Label(left_frame, text="PARKING KIOSK", font=("Arial", 18, "bold"),
         bg=KIOSK_BG, fg=TEXT_COLOR).pack(pady=(20, 10))

# Free spots count
free_label = tk.Label(left_frame, text=f"Free spots: {lot.free_count()}",
                      font=("Arial", 12), bg=KIOSK_BG, fg=TEXT_COLOR)
free_label.pack(pady=10)

# Assigned spot display
assigned_label = tk.Label(left_frame, text="Your spot: ---",
                          font=("Arial", 12, "bold"), fg="#e67e22", bg=KIOSK_BG)
assigned_label.pack(pady=10)

# ---------- Kiosk buttons ----------
button_style = {
    'font': ("Arial", 11, "bold"),
    'relief': 'flat',
    'borderwidth': 0,
    'padx': 20,
    'pady': 8,
    'cursor': 'hand2'
}

def assign_spot():
    spot = lot.assign_random_spot()
    if spot:
        assigned_label.config(text=f"🚗 Your spot: {spot}")
        frame = spot_frames[spot]
        frame.config(bg=OCCUPIED_COLOR)
        frame.winfo_children()[0].config(bg=OCCUPIED_COLOR)
        log_message(f"[Kiosk] Car assigned → {spot}")
    else:
        assigned_label.config(text="Lot FULL!")
        log_message("[Kiosk] Lot FULL – no free spots.")
    free_label.config(text=f"Free spots: {lot.free_count()}")

get_btn = tk.Button(left_frame, text="Get Parking Spot", bg=BTN_BG, fg=BTN_FG,
                    command=assign_spot, **button_style)
get_btn.pack(pady=10)

# "Car Left (Random)" button
def free_random_spot():
    data = lot._load_data()
    occupied = [s for s, st in data.items() if st == 'occupied']
    if occupied:
        free_spot(random.choice(occupied))
    else:
        log_message("[SCANNER] No occupied spots.")

tk.Button(left_frame, text="Car Left (Random)", bg='#95a5a6', fg='white',
          command=free_random_spot, **button_style).pack(pady=5)

# Instruction text at bottom of kiosk
tk.Label(left_frame, text="Press button to get a spot", font=("Arial", 9),
         bg=KIOSK_BG, fg="#7f8c8d").pack(side=tk.BOTTOM, pady=(10, 5))

# ---------- Digital clock ----------
clock_label = tk.Label(left_frame, text="", font=("Arial", 10), bg=KIOSK_BG, fg='#7f8c8d')
clock_label.pack(side=tk.BOTTOM, pady=(0, 10))

def update_clock():
    time_str = time.strftime("%H:%M:%S")
    clock_label.config(text=f"🕒 {time_str}")
    root.after(1000, update_clock)
update_clock()

# ----- Right panel (map) -----
right_frame = tk.Frame(top_frame, bg=MAP_BG,
                       highlightbackground=SEPARATOR_COLOR, highlightthickness=2)
right_frame.pack(side=tk.RIGHT, expand=True, fill=tk.BOTH, padx=(0, 10), pady=10)

# Legend at the top of map (pack inside right_frame)
legend_frame = tk.Frame(right_frame, bg=MAP_BG)
legend_frame.pack(side=tk.TOP, fill=tk.X, pady=(10, 5))

tk.Label(legend_frame, text="   ", bg=FREE_COLOR, width=4).pack(side=tk.LEFT, padx=(20, 5))
tk.Label(legend_frame, text="Free", bg=MAP_BG, font=("Arial", 9), fg=TEXT_COLOR).pack(side=tk.LEFT)
tk.Label(legend_frame, text="   ", bg=OCCUPIED_COLOR, width=4).pack(side=tk.LEFT, padx=(15, 5))
tk.Label(legend_frame, text="Occupied", bg=MAP_BG, font=("Arial", 9), fg=TEXT_COLOR).pack(side=tk.LEFT)

# ---------- Lane markings (place directly on right_frame) ----------
lane_color = '#bdc3c7'
road = tk.Frame(right_frame, bg=lane_color, height=3)
road.place(relx=0.0, rely=0.55, relwidth=1.0, anchor='w')

tk.Label(right_frame, text="DRIVEWAY", bg=MAP_BG, fg='#7f8c8d',
         font=('Arial', 7, 'italic')).place(relx=0.5, rely=0.55, anchor='center')
tk.Label(right_frame, text="← ENTER", bg=MAP_BG, fg=TEXT_COLOR,
         font=('Arial', 8, 'bold')).place(relx=0.05, rely=0.55, anchor='w')
tk.Label(right_frame, text="EXIT →", bg=MAP_BG, fg=TEXT_COLOR,
         font=('Arial', 8, 'bold')).place(relx=0.95, rely=0.55, anchor='e')

# ---------- Container for the spot grid (grid inside) ----------
spot_grid_frame = tk.Frame(right_frame, bg=MAP_BG)
spot_grid_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=10)

spot_frames = {}
rows = ['A', 'B']
cols = [1, 2, 3]

for r_idx, row_letter in enumerate(rows):
    for c_idx, col_num in enumerate(cols):
        spot_id = f"{row_letter}-{col_num}"
        # Parent is spot_grid_frame (NOT right_frame)
        frame = tk.Frame(spot_grid_frame, relief=tk.RAISED, borderwidth=2,
                         bg=FREE_COLOR, width=110, height=80)
        frame.grid(row=r_idx, column=c_idx, padx=8, pady=8, sticky="nsew")
        frame.grid_propagate(False)

        lbl = tk.Label(frame, text=spot_id, font=("Arial", 11, "bold"),
                       bg=FREE_COLOR, fg="white")
        lbl.pack(expand=True, fill=tk.BOTH)

        tk.Button(frame, text="🚗 Left", font=("Arial", 8),
                  bg=SCANNER_BG, fg='#2c3e50', relief='flat', borderwidth=0,
                  command=lambda sid=spot_id: free_spot(sid)).pack(side=tk.BOTTOM, pady=3)

        spot_frames[spot_id] = frame

# Make the spot grid expand
for i in range(2):
    spot_grid_frame.grid_rowconfigure(i, weight=1)
for j in range(3):
    spot_grid_frame.grid_columnconfigure(j, weight=1)

# ----- Terminal (bottom) -----
terminal_frame = tk.Frame(root, bg=ROOT_BG, height=120)
terminal_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0,10))
terminal_frame.pack_propagate(False)

terminal_text = tk.Text(terminal_frame, wrap=tk.WORD, bg=TERM_BG, fg=TERM_FG,
                        font=('Consolas', 10), state=tk.DISABLED, relief=tk.FLAT,
                        borderwidth=0, highlightthickness=0)
terminal_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scrollbar = tk.Scrollbar(terminal_frame, orient=tk.VERTICAL, command=terminal_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
terminal_text.config(yscrollcommand=scrollbar.set)

def log_message(msg):
    terminal_text.config(state=tk.NORMAL)
    terminal_text.insert(tk.END, f"{msg}\n")
    terminal_text.see(tk.END)
    terminal_text.config(state=tk.DISABLED)

# Free spot function (updates UI and logs)
def free_spot(spot_id):
    if lot.free_spot(spot_id):
        frame = spot_frames[spot_id]
        frame.config(bg=FREE_COLOR)
        frame.winfo_children()[0].config(bg=FREE_COLOR)
        free_label.config(text=f"Free spots: {lot.free_count()}")
        log_message(f"[SCANNER] {spot_id}: car left → now free")
        assigned_label.config(text="Your spot: ---")   # reset kiosk message

root.mainloop()