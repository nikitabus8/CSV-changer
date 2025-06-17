import tkinter as tk
from tkinter import filedialog
import csv

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        process_csv(file_path)

def process_csv(file_path):
    with open(file_path, "r") as csv_file:
        file_reader = csv.reader(csv_file, delimiter=",")
        rows = list(file_reader)

    modified_rows = rename_columns(
        rows,
        {
            "private"
        }
    )

    modified_rows = update_status_column(modified_rows, "Status", {"private"})

    final_rows = select_and_reorder_columns(
        modified_rows,
        ["private"]
    )

    if final_rows:
        save_file(final_rows)

def save_file(rows):
    """Prompt the user to save the modified CSV file."""
    save_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv")],
        title="Save CSV As"
    )
    if save_path:
        with open(save_path, "w", newline="") as new_file:
            file_writer = csv.writer(new_file, delimiter=",")
            file_writer.writerows(rows)
        print(f"Modified CSV saved as '{save_path}'.")

def rename_columns(rows, rename_map):
    """Renames columns in the CSV rows based on the rename_map."""
    if not rows:
        print("The CSV file is empty.")
        return None

    headers = rows[0]
    for old_name, new_name in rename_map.items():
        if old_name in headers:
            column_index = headers.index(old_name)
            headers[column_index] = new_name
            print(f"Renamed column '{old_name}' to '{new_name}'.")
        else:
            print(f"Column '{old_name}' not found in headers.")

    return rows

def update_status_column(rows, column_name, value_map):
    """Updates the values in a specific column based on a mapping."""
    if not rows:
        print("The CSV file is empty.")
        return None

    headers = rows[0]
    if column_name not in headers:
        print(f"Column '{column_name}' not found.")
        return rows

    column_index = headers.index(column_name)
    for row in rows[1:]:
        if row[column_index] in value_map:
            old_value = row[column_index]
            row[column_index] = value_map[old_value]
            print(f"Updated '{old_value}' to '{row[column_index]}' in row: {row}")

    return rows

def select_and_reorder_columns(rows, selected_columns):
    """Selects specific columns and reorders them. Adds empty columns for missing ones."""
    if not rows:
        print("The CSV file is empty.")
        return None

    headers = rows[0]
    data_rows = rows[1:]

    for col_name in selected_columns:
        if col_name not in headers:
            print(f"Adding missing column '{col_name}' with empty values.")
            headers.append(col_name)
            for row in data_rows:
                row.append("")

    column_indices = [headers.index(col_name) for col_name in selected_columns]
    reordered_rows = [[headers[i] for i in column_indices]]
    for row in data_rows:
        reordered_rows.append([row[i] for i in column_indices])

    return reordered_rows

root = tk.Tk()
root.title("CSV Editor")
root.geometry("200x80")

open_button = tk.Button(root, text="Open CSV", command=open_file)
open_button.pack(pady=10)

root.mainloop()