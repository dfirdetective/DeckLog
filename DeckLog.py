import sys
import os
import json
import csv
import tkinter as tk
from collections import defaultdict
import pyperclip

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

    root.columnconfigure(0, weight=0)  # Labels stay fixed
    root.columnconfigure(1, weight=1)  # Text boxes fill the rest

    widgets = []

    for i, (column, prompt_text) in enumerate(prompt_list):
        # Allow rows to stretch evenly (optional)
        root.rowconfigure(i, weight=1)

        tk.Label(root, text=prompt_text).grid(row=i, column=0, sticky="e", padx=5, pady=5)

        text_box = tk.Text(root, height=5)
        text_box.grid(row=i, column=1, padx=5, pady=5, sticky="nsew")  # Fill cell
        text_box.bind("<Tab>", lambda e, index=i: focus_next(e, widgets, i))

        if i == 0:
            text_box.focus_set()

        widgets.append(text_box)

    # Submit button
    submit_btn = tk.Button(root, text="Submit", command=submit)
    submit_btn.grid(columnspan=2, pady=10)

    root.bind("<Return>", submit)
    root.mainloop()
    return data

def show_daily_summary():
    if not os.path.isfile("deck_log.csv"):
        summary = "No log file found."
    else:
        today = datetime.now().strftime("%Y-%m-%d")
        grouped = defaultdict(list)

        with open("deck_log.csv", newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row.get("Date") == today:
                    log_type = row.get("Type", "Unknown")
                    time = row.get("Time", "")
                    entry_parts = []

                    for field in row:
                        if field not in ("Date", "Time", "Day", "Type"):
                            value = (row.get(field) or "").strip()
                            if value:
                                entry_parts.append(f"{field}: {value}")

                    entry_text = f"- 🕐 {time} — " + ", ".join(entry_parts)
                    grouped[log_type].append(entry_text)

        if not grouped:
            summary = "No logs found for today."
        else:
            summary = ""
            for log_type, entries in grouped.items():
                summary += f"\n{log_type}\n"
                for entry in entries:
                    summary += entry + "\n"
            summary = summary.strip()

    pyperclip.copy(summary)

    root = tk.Tk()
    root.title("DeckLog: Daily Summary")
    root.geometry("700x500")

    # === Create a frame for scrollable text ===
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    text_widget = tk.Text(frame, wrap="word", yscrollcommand=scrollbar.set)
    text_widget.insert("1.0", summary)
    text_widget.configure(state="disabled")
    text_widget.pack(side="left", fill="both", expand=True)

    scrollbar.config(command=text_widget.yview)

    # Info bar + optional Close button
    tk.Label(root, text="Summary copied to clipboard.", fg="gray").pack(pady=(0, 10))
    tk.Button(root, text="Close", command=root.destroy).pack(pady=(0, 10))

    root.mainloop()


#  Get Log Type from CLI or Dropdown
arg = sys.argv[1] if len(sys.argv) > 1 else "List"
label = arg.strip()

if label.lower() == "list":
    label = pick_log_type()

if label.lower() == "summary":
    show_daily_summary()
    sys.exit(0)

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
