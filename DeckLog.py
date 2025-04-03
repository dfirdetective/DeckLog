import sys
import os
import json
import csv
import tkinter as tk
from datetime import datetime


#  Helper: Support for PyInstaller Exe Version
def get_resource_path(filename):
    if hasattr(sys, '_MEIPASS'):  # PyInstaller temp folder
        return os.path.join(sys._MEIPASS, filename)
    return os.path.join(os.path.abspath("."), filename)


#  Load Prompts from JSON
with open(get_resource_path("prompts.json"), "r") as f:
    prompt_map = json.load(f)


#  GUI: Dropdown Picker for the List option
def pick_log_type():
    selected = {}

    picker = tk.Tk()
    picker.title("Choose a log type")
    picker.geometry("400x120")

    tk.Label(picker, text="Select a log type:").pack(pady=(10, 5))

    options = list(prompt_map.keys())
    var = tk.StringVar(value=options[0])

    tk.OptionMenu(picker, var, *options).pack()

    def submit():
        selected["label"] = var.get()
        picker.quit()
        picker.destroy()

    tk.Button(picker, text="Continue", command=submit).pack(pady=10)
    picker.mainloop()

    return selected.get("label", "Log")


#  Tab Navigation Between Fields
def focus_next(event, widgets, current_index):
    next_index = current_index + 1
    if next_index < len(widgets):
        widgets[next_index].focus_set()
    else:
        event.widget.tk_focusNext().focus_set()
    return "break"


#  GUI: Collect Prompt Inputs
def collect_inputs(prompt_list):
    data = {}

    def submit(event=None):
        for (col, _), widget in zip(prompt_list, widgets):
            if isinstance(widget, tk.Text):
                data[col] = widget.get("1.0", tk.END).strip()
            else:
                data[col] = widget.get()
        root.destroy()

    root = tk.Tk()
    root.title(f"DeckLog: {label}")
    root.geometry("600x400")
    root.columnconfigure(0, weight=0)
    root.columnconfigure(1, weight=1) 

    widgets = []

    for i, (column, prompt_text) in enumerate(prompt_list):
        root.rowconfigure(i, weight=1)

        tk.Label(root, text=prompt_text).grid(row=i, column=0, sticky="e", padx=5, pady=5)

        text_box = tk.Text(root, height=5)
        text_box.grid(row=i, column=1, padx=5, pady=5, sticky="nsew")
        text_box.bind("<Tab>", lambda e, index=i: focus_next(e, widgets, i))
        if i == 0:
            text_box.focus_set()
        widgets.append(text_box)

    submit_btn = tk.Button(root, text="Submit", command=submit)
    submit_btn.grid(columnspan=2, pady=10)

    root.bind("<Return>", submit)
    root.mainloop()
    return data


#  Get Log Type from CLI or Dropdown
arg = sys.argv[1] if len(sys.argv) > 1 else "List"
label = arg.strip()

if label.lower() == "list":
    label = pick_log_type()

# Default to "Log" question if the label does not exist in prompts.json
prompt_list = prompt_map.get(label, [["Entry", f"What would you like to log for {label}?"]])

#  Get Data from GUI Input
data = collect_inputs(prompt_list)

#  Log to CSV File
log_file = "deck_log.csv"
file_exists = os.path.isfile(log_file)

now = datetime.now()
row = {
    "Date": now.strftime("%Y-%m-%d"),
    "Time": now.strftime("%I:%M %p"),
    "Day": now.strftime("%A"),
    "Type": label
}
row.update(data)

headers = ["Date", "Time", "Day", "Type"] + list(data.keys())

with open(log_file, "a", newline='', encoding="utf-8") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=headers)

    if not file_exists:
        writer.writeheader()
    writer.writerow(row)
