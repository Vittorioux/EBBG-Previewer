# --------------------------------------------------------------------------------------------------------------------------



# EarthBound Battle Background Previewer

# https://github.com/Vittorioux/EBBG-Previewer

# UI file.



# -------------------------------------------------------- Imports ---------------------------------------------------------



import logic as l
import constants as c
from constants import DATA_FOLDER_NAME, DATA_FILE_NAME, DEFAULT_DATA

import os
import sys
import tempfile
from functools import partial

import math as m

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import messagebox



# ----------------------------------------------------- Main program -------------------------------------------------------



if __name__ == "__main__":
	
	# -----------------------------------------------------------
	# --------------------- Initialization ----------------------
	# -----------------------------------------------------------
	
	# Detect if we're running the .EXE or from source.
	
	if getattr(sys, 'frozen', False):
		base_path = os.path.dirname(sys.executable)
	else:
		base_path = os.path.dirname(__file__)
	
	# Create data folder and file if they dons't exist.
	
	if not os.path.exists(os.path.join(base_path, DATA_FOLDER_NAME)):
		os.makedirs(os.path.join(base_path, DATA_FOLDER_NAME))
	
	if not os.path.exists(os.path.join(base_path, DATA_FILE_NAME)):
		with open(os.path.join(base_path, DATA_FILE_NAME), "w") as data_f:
			data_f.write(DEFAULT_DATA)
	
	# Load dict 'data'.
	
	data = l.read_data_file(os.path.join(base_path, DATA_FILE_NAME))
	
	program_geometry = f"{data["width"]}x{data["height"]}+{data["x_pos"]}+{data["y_pos"]}"   # These four names are hardcoded.
	
	# Create the Tkinter application.
	
	root = tk.Tk()
	
	# Fetch icon.
	
	try:
		assets_path = sys._MEIPASS
	except Exception:
		assets_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "assets"))
	
	root.iconbitmap(os.path.join(assets_path, "icon.ico"))
	
	# Title and geometry.
	
	root.title("EarthBound BG Previewer")
	root.geometry(program_geometry)
	
	# -----------------------------------------------------------
	# ----------------------- Main frames -----------------------
	# -----------------------------------------------------------
	
	# Top frame: files and 'About' button.
	
	top_frame = tk.Frame(root, height=100, bg="lightblue")
	top_frame.pack(side="top", fill="x")
	
	separator = tk.Frame(root, height=2, bg="black")
	separator.pack(fill="x")
	
	# Middle frame: setting fields.
	
	middle_frame = tk.Frame(root, height=150)
	middle_frame.pack(side="top", fill="x")
	
	separator = tk.Frame(root, height=2, bg="black")
	separator.pack(fill="x")
	
	# Bottom frame: console and 'Execute' button.
	
	bottom_frame = tk.Frame(root)
	bottom_frame.pack(side="top", fill="both", expand=True)
	
	# Dict to be filled with the Tkinter fields.
	
	fields = {}
	
	# -----------------------------------------------------------
	# -------------------- Top frame fields ---------------------
	# -----------------------------------------------------------
	
	t_label_texts = ["Emulator EXE:", "(Clean) ROM:", "BG Layer 1:", "BG Layer 2:"]
	
	# Create the 4 fields.
	
	for i in range(4):
		label = tk.Label(top_frame, text=t_label_texts[i], bg="lightblue")
		label.grid(row=i, column=0, padx=5, pady=5, sticky="e")
		
		entry = tk.Entry(top_frame)
		entry.grid(row=i, column=1, padx=5, pady=5, sticky="ew")
		
		fields[c.t_field_names[i]] = entry
		
		button = tk.Button(top_frame, text="Browse", command=lambda e=entry: l.browse_file(e))
		button.grid(row=i, column=2, padx=5, pady=5)
	
	top_frame.grid_columnconfigure(1, weight=1)
	
	# Add the 'About' button.
	
	button = tk.Button(top_frame, text="About", command=lambda: l.open_about_window(root))
	button.grid(row=0, column=3, padx=(50, 5), pady=5)
	
	# -----------------------------------------------------------
	# ------------------ Middle frame fields --------------------
	# -----------------------------------------------------------
	# ------ Not the best way to program this, I guess... -------
	# -----------------------------------------------------------
	
	# Label names.
	
	m_label_texts_palette = ["BPP:", "Cycle type:", "Palette cycle 1 begin:", "Palette cycle 1 end:", "Palette cycle 2 begin:", "Palette cycle 2 end:", "Cycle speed:"]

	m_label_texts_scroll = ["Disable scrolling", "Duration:", "Horizontal acceleration:", "Horizontal movement:", "Vertical acceleration:", "Vertical movement:"]

	m_label_texts_distortion = ["Disable distortion", "Type:", "Ripple amplitude:", "Ripple amplitude acceleration:", "Ripple frequency:", "Ripple frequency acceleration:", "Acceleration (Unk B):", "Speed:", "Compression rate (Unk C):", "Compression rate acceleration (Unk D):", "Duration (Unk A):"]
	
	# Main notebook.
	
	main_notebook = ttk.Notebook(middle_frame)
	main_notebook.pack(expand=True, fill="both")
	
	# Add IMG preview tab.
	
	tab = tk.Frame(main_notebook)
	main_notebook.add(tab, text="Images")
	
	img_container = tk.Frame(tab)
	img_container.pack(pady=40)
	
	img_frame_1 = tk.Frame(img_container, width=128, height=128, bg="gray")
	img_frame_1.pack(side="left", padx=50)
	
	img_frame_2 = tk.Frame(img_container, width=128, height=128, bg="gray")
	img_frame_2.pack(side="left", padx=50)
	
	img_frame_1.pack_propagate(False)
	img_frame_2.pack_propagate(False)
	
	string_vars = []
	
	for i in range(2):
		string_vars.append(tk.StringVar())
		string_vars[-1].trace_add("write", partial(l.update_preview, fields, img_frame_1, img_frame_2))   # (pass reference to the func by using 'partial' from 'functools').
		
		fields[f"setting_bg{i+1}"].config(textvariable=string_vars[-1])
	
	combobox_vars = []
	check_vars = []
	
	# For BG1 and BG2.
	
	for bg in range(2):
		tab = tk.Frame(main_notebook)
		main_notebook.add(tab, text=f"Layer {bg+1}")
		
		notebook = ttk.Notebook(tab)
		notebook.pack(expand=True, fill="both")
		
		# --------------------------------------------------
		
		# Add 'Palettes' tab.
		
		tab = tk.Frame(notebook)
		notebook.add(tab, text="Palettes")
		
		for field in range(7):
			tk.Label(tab, text=m_label_texts_palette[field]).grid(row=m.floor(field/2), column=(field%2)*2, padx=5, pady=5, sticky="e")
			
			# BPP.
			
			if field == 0:
				if bg == 0:
					bpp_option_names = ["2", "4"]
				else:
					bpp_option_names = ["2"]
				
				combobox_vars.append(tk.StringVar())
				combobox = ttk.Combobox(tab, textvariable=combobox_vars[-1], values=bpp_option_names, state="readonly")
				combobox.grid(row=0, column=1, padx=5, pady=5, sticky="e")
				
				if bg == 0:
					combobox.current(1)
				else:
					combobox.current(0)
				
				fields[c.m_field_names_palette[field]+f"_bg{bg+1}"] = combobox
			
			# Cycle type.
			
			elif field == 1:
				combobox_vars.append(tk.StringVar())
				combobox = ttk.Combobox(tab, textvariable=combobox_vars[-1], values=c.CYCLE_TYPE_NAMES, state="readonly")
				combobox.grid(row=0, column=3, padx=5, pady=5, sticky="e")
				combobox.current(0)
				fields[c.m_field_names_palette[field] + f"_bg{bg+1}"] = combobox
			
			# Rest of settings.
			
			else:
				entry = tk.Entry(tab)
				entry.grid(row=m.floor(field/2), column=(field%2)*2+1, padx=5, pady=5, sticky="e")
				fields[c.m_field_names_palette[field] + f"_bg{bg+1}"] = entry
				entry.insert(0, "0")
		
		# --------------------------------------------------
		
		# Add 'Scroll' tabs.
		
		for scr in range(4):
			tab = tk.Frame(notebook)
			notebook.add(tab, text=f"Scroll {scr+1}")
			
			for field in range(6):
				
				# Checkbox.
				
				if field == 0:
					check_vars.append(tk.BooleanVar())
					check = tk.Checkbutton(tab, text=m_label_texts_scroll[0] + f" {scr+1}", variable=check_vars[-1])
					check.grid(row=0, column=0, padx=5, pady=5, sticky="e")
					check_vars[-1].set(True)
					fields[c.m_field_names_scroll[field] + f"_bg{bg+1}" + f"_scr{scr+1}"] = check
				
				# Rest of settings.
				
				else:
					tk.Label(tab, text=m_label_texts_scroll[field]).grid(row=m.floor(field/2), column=(field%2)*2, padx=5, pady=5, sticky="e")
					entry = tk.Entry(tab)
					entry.grid(row=m.floor(field/2), column=(field%2)*2+1, padx=5, pady=5, sticky="e")
					fields[c.m_field_names_scroll[field] + f"_bg{bg+1}" + f"_scr{scr+1}"] = entry
					entry.insert(0, "0")
		
		# --------------------------------------------------
		
		# Add 'Distortion' tabs.
		
		for dst in range(4):
			tab = tk.Frame(notebook)
			notebook.add(tab, text=f"Distortion {dst+1}")
			
			for field in range(11):
				
				# Checkbox.
				
				if field == 0:
					check_vars.append(tk.BooleanVar())
					check = tk.Checkbutton(tab, text=m_label_texts_distortion[0] + f" {dst+1}", variable=check_vars[-1])
					check.grid(row=0, column=0, padx=5, pady=5, sticky="e")
					check_vars[-1].set(True)
					fields[c.m_field_names_distortion[field] + f"_bg{bg+1}" + f"_dst{dst+1}"] = check
				
				# Distortion type.
				
				elif field == 1:
					tk.Label(tab, text=m_label_texts_distortion[field]).grid(row=0, column=2, padx=5, pady=5, sticky="e")
					combobox_vars.append(tk.StringVar())
					combobox = ttk.Combobox(tab, textvariable=combobox_vars[-1], values=c.DST_TYPE_NAMES, state="readonly", width=25)
					combobox.grid(row=0, column=3, padx=5, pady=5, sticky="e")
					combobox.current(0)
					fields[c.m_field_names_distortion[field] + f"_bg{bg+1}" + f"_dst{dst+1}"] = combobox
				
				# Rest of settings.
				
				else:
					tk.Label(tab, text=m_label_texts_distortion[field]).grid(row=m.floor(field/2), column=(field%2)*2, padx=5, pady=5, sticky="e")
					entry = tk.Entry(tab)
					entry.grid(row=m.floor(field/2), column=(field%2)*2+1, padx=5, pady=5, sticky="e")
					fields[c.m_field_names_distortion[field] + f"_bg{bg+1}" + f"_dst{dst+1}"] = entry
					entry.insert(0, "0")
	
	# -----------------------------------------------------------
	# ------------------- Bottom frame stuff --------------------
	# -----------------------------------------------------------
	
	# Console.
	
	console = tk.Text(bottom_frame, wrap="word", height=5)
	console.grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
	console.config(state="disabled")
	fields["console"] = console
	
	# Buttons.
	
	button = tk.Button(bottom_frame, text="Execute", command=lambda: l.execute(fields, check_vars))
	button.grid(row=1, column=0, pady=5, padx=5, sticky="ew")
	
	button = tk.Button(bottom_frame, text="Run", command=lambda: l.run_rom(fields))
	button.grid(row=1, column=1, pady=5, padx=5, sticky="ew")
	
	bottom_frame.grid_rowconfigure(0, weight=1)
	bottom_frame.grid_columnconfigure(0, weight=1)
	bottom_frame.grid_columnconfigure(1, weight=1)
	
	# -----------------------------------------------------------
	# --------------- Application initialization ----------------
	# -----------------------------------------------------------
	
	# Action to perform when closing the application.
	
	root.protocol("WM_DELETE_WINDOW", lambda: (l.write_data_file(os.path.join(base_path, DATA_FILE_NAME), fields, root), root.destroy()))
	
	# Load saved fields from the data file.
	
	for key, value in data.items():
		if key in c.t_field_names:
			fields[key].delete(0, tk.END)
			fields[key].insert(0, str(value))
	
	# Update preview image frames (only really makes a difference if both BG fields start empty).
	
	l.update_preview(fields, img_frame_1, img_frame_2)
	
	# Run the application.
	
	root.mainloop()