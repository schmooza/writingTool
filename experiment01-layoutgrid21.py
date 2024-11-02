import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import json
from spellchecker import SpellChecker
import csv
import string

highlight_errors = False  # State for highlight toggle
highlight_specific_word_active = False  # State for specific word highlight toggle
font_size = 14  # Initial font size

# Function to export data to JSON file
def export_json():
    data = {}
    for row in range(3):
        for col in range(3):
            if entries[row][col] is not None:
                cell_data = entries[row][col].get("1.0", tk.END).strip()
                data[f"{row}{col}"] = cell_data
    file_path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file)

# Function to export data to CSV file
import csv  # Add this line to your imports at the top

def export_csv():
    data = []

    # Collect data from the text widgets
    for row in range(3):
        data_row = []
        for col in range(3):
            if entries[row][col] is not None:
                cell_data = entries[row][col].get("1.0", tk.END).strip()
                data_row.append(cell_data)
            else:
                data_row.append("")
        data.append(data_row)

    # Ask for the file path to save the CSV
    file_path = filedialog.asksaveasfilename(defaultextension='.csv', filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            # Writing headers for each cell
            headers = [f"Cell {row * 3 + col + 1:02}" for row in range(3) for col in range(3)]
            writer.writerow(headers)

            # Writing the data to the CSV
            for row in data:
                writer.writerow(row)




# Function to import data from JSON file
def import_json():
    file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'r') as json_file:
            data = json.load(json_file)
            for key, value in data.items():
                try:
                    row, col = int(key[0]), int(key[1])
                    if entries[row][col] is not None:
                        entries[row][col].delete("1.0", tk.END)
                        entries[row][col].insert("1.0", value)
                except (IndexError, ValueError):
                    pass  # Handle any improperly formatted keys gracefully


# Function to spell check and highlight misspelled words
import re  # Import regular expressions to help handle punctuation

import string

# Function to spell check and highlight misspelled words
def spell_check_highlight():
    spell = SpellChecker()
    for row in range(3):
        for col in range(3):
            if entries[row][col] is not None:
                text_widget = entries[row][col]
                text_widget.tag_remove('misspelled', '1.0', tk.END)
                text = text_widget.get("1.0", tk.END).strip()

                # Split text into words and keep track of their positions
                words = text.split()
                start_idx = 0

                for word in words:
                    clean_word = word.strip(string.punctuation)
                    if clean_word and clean_word not in spell:
                        # Find the position of the word in the text widget
                        start_pos = f"1.0 + {start_idx}c"
                        end_pos = f"{start_pos} + {len(word)}c"
                        text_widget.tag_add('misspelled', start_pos, end_pos)

                    # Update start index for the next word, including trailing spaces
                    start_idx += len(word) + 1

                # Configure tag properties for misspelled words
                text_widget.tag_config('misspelled', foreground='red')

# Function to toggle spell check highlight
def toggle_highlight():
    global highlight_errors
    highlight_errors = not highlight_errors
    if highlight_errors:
        highlight_btn.config(text="Stop Highlighting Spelling Errors")
        spell_check_highlight()
    else:
        highlight_btn.config(text="Highlight Spelling Errors")
        for row in range(3):
            for col in range(3):
                if entries[row][col] is not None:
                    entries[row][col].tag_remove('misspelled', '1.0', tk.END)

# Function to spell check the text in each cell and provide suggestions
from spellchecker import SpellChecker
import string

# Function to spell check the text in each cell and provide suggestions
def spell_check_suggestions():
    spell = SpellChecker()
    corrections = {}

    for row in range(3):
        for col in range(3):
            if entries[row][col] is not None:
                text_widget = entries[row][col]
                text = text_widget.get("1.0", tk.END).strip()
                
                # Split text into words and clean punctuation
                words = text.split()
                for word in words:
                    clean_word = word.strip(string.punctuation).lower()  # Clean punctuation and make lowercase
                    if clean_word and clean_word not in spell:
                        # Get suggestions only if the word is not recognized
                        if word in corrections:
                            suggestion = corrections[word]
                        else:
                            suggestions = spell.candidates(clean_word)
                            if suggestions:
                                suggestion = simpledialog.askstring(
                                    "Spell Check", 
                                    f"Suggestions for '{word}': {', '.join(suggestions)}\nEnter correction:", 
                                    initialvalue=spell.correction(clean_word)
                                )
                                if suggestion:
                                    apply_to_all = messagebox.askyesno(
                                        "Spell Check", 
                                        f"Apply correction '{suggestion}' to all occurrences of '{word}'?"
                                    )
                                    if apply_to_all:
                                        corrections[word] = suggestion

                        if suggestion:
                            text = text.replace(word, suggestion)
                
                text_widget.delete("1.0", tk.END)
                text_widget.insert("1.0", text)


# Function to increase font size
def increase_font_size():
    global font_size
    font_size += 1
    update_font_size()
    if 'text_field' in globals() and text_field.winfo_exists():
        text_field.config(font=("TkDefaultFont", font_size))

# Function to decrease font size
def decrease_font_size():
    global font_size
    if font_size > 1:
        font_size -= 1
    update_font_size()
    if 'text_field' in globals():
        text_field.config(font=("TkDefaultFont", font_size))

# Function to update the font size of all text widgets
def update_font_size():
        for row in range(3):
            for col in range(3):
                if entries[row][col] is not None:
                    entries[row][col].config(font=("TkDefaultFont", font_size))
        if 'text_field' in globals() and text_field.winfo_exists():
            text_field.config(font=("TkDefaultFont", font_size))
        for col in range(3):
            if entries[row][col] is not None:
                entries[row][col].config(font=("TkDefaultFont", font_size))

# Function to highlight a specific word set by the user
def highlight_specific_word():
    global highlight_specific_word_active
    highlight_specific_word_active = not highlight_specific_word_active
    if highlight_specific_word_active:
        highlight_word_btn.config(text="Stop Highlighting Specific Word")
        word_to_highlight = simpledialog.askstring("Highlight Word", "Enter the word to highlight:")
        if word_to_highlight:
            for row in range(3):
                for col in range(3):
                    if entries[row][col] is not None:
                        text_widget = entries[row][col]
                        text_widget.tag_remove('highlight', '1.0', tk.END)
                        start_idx = "1.0"
                        while True:
                            start_idx = text_widget.search(word_to_highlight, start_idx, stopindex=tk.END, nocase=True)
                            if not start_idx:
                                break
                            end_idx = f"{start_idx}+{len(word_to_highlight)}c"
                            text_widget.tag_add('highlight', start_idx, end_idx)
                            start_idx = end_idx
                        text_widget.tag_config('highlight', foreground='blue')
    else:
        highlight_word_btn.config(text="Highlight Specific Word")
        for row in range(3):
            for col in range(3):
                if entries[row][col] is not None:
                    entries[row][col].tag_remove('highlight', '1.0', tk.END)

# Create main window
root = tk.Tk()

# Function to send the contents of the Template Maker to a chosen box in the main window
def send_to_main_screen(text_widget):
    content = text_widget.get("1.0", tk.END).strip()
    if content:
        row, col = 0, 1
        if entries[row][col] is not None:
            entries[row][col].delete("1.0", tk.END)
            entries[row][col].insert("1.0", content)
    root.title("3x3 Grid with JSON Import/Export")

# Function to open the Template Maker window
def open_template_maker():
    global text_field
    template_window = tk.Toplevel(root)
    template_window.title("Template Maker")
    template_window.geometry("500x800")
    label = tk.Label(template_window, text="This is the Template Maker Window.", font=("TkDefaultFont", 14))
    label.pack(pady=20)
    text_field = tk.Text(template_window, wrap='word', font=("TkDefaultFont", font_size))
    text_field.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)

    # Function to save the contents of the Template Maker window to a JSON file
    def save_template():
        content = text_field.get("1.0", tk.END).strip()
        if content:
            file_path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[("JSON files", "*.json")])
            if file_path:
                with open(file_path, 'w') as json_file:
                    json.dump({"template": content}, json_file)

    # Function to load the contents from a JSON file into the Template Maker window
    def load_template():
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)
                if "template" in data:
                    text_field.delete("1.0", tk.END)
                    text_field.insert("1.0", data["template"])

    # Button to save the contents of the Template Maker window
    save_btn = tk.Button(template_window, text="Save Template", command=save_template, font=("TkDefaultFont", 14))
    save_btn.pack(pady=5, fill=tk.X)

    # Button to load the contents into the Template Maker window
    load_btn = tk.Button(template_window, text="Load Template", command=load_template, font=("TkDefaultFont", 14))
    load_btn.pack(pady=5, fill=tk.X)

    # Button to send contents back to the main window
    send_btn = tk.Button(template_window, text="Send to Cell Next to Menu", command=lambda: send_to_main_screen(text_field), font=("TkDefaultFont", 14))
    send_btn.pack(pady=10, fill=tk.X)

root.rowconfigure([0, 1, 2], weight=1)
root.columnconfigure([0, 1, 2], weight=1)

# Create grid and entries
entries = [[None for _ in range(3)] for _ in range(3)]
for row in range(3):
    for col in range(3):
        if row == 0 and col == 0:
            # Menu items cell
            frame = tk.Frame(root, bg=['#FFEEEE', '#EEFFEE', '#EEEEFF', '#FFFFEE', '#EEFFFF', '#FFEFFF', '#F0FFF0', '#FFF0F0', '#F0F0FF'][row * 3 + col])
            frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            import_btn = tk.Button(frame, text="Load", command=import_json, font=("TkDefaultFont", 14))
            import_btn.pack(side=tk.TOP, fill=tk.X)
            export_btn = tk.Button(frame, text="Save", command=export_json, font=("TkDefaultFont", 14))
            export_csv_btn = tk.Button(frame, text="Design", command=export_csv, font=("TkDefaultFont", 14))
            export_csv_btn.pack(side=tk.TOP, fill=tk.X)
            export_btn.pack(side=tk.TOP, fill=tk.X)
            highlight_btn = tk.Button(frame, text="Highlight Spelling Errors", command=toggle_highlight, font=("TkDefaultFont", 14))
            highlight_btn.pack(side=tk.TOP, fill=tk.X)
            highlight_word_btn = tk.Button(frame, text="Highlight Specific Word", command=highlight_specific_word, font=("TkDefaultFont", 14))
            highlight_word_btn.pack(side=tk.TOP, fill=tk.X)
            spell_check_suggest_btn = tk.Button(frame, text="Spell Check with Suggestions", command=spell_check_suggestions, font=("TkDefaultFont", 14))
            spell_check_suggest_btn.pack(side=tk.TOP, fill=tk.X)
            increase_font_btn = tk.Button(frame, text="Increase Font Size", command=increase_font_size, font=("TkDefaultFont", 14))
            increase_font_btn.pack(side=tk.TOP, fill=tk.X)
            decrease_font_btn = tk.Button(frame, text="Decrease Font Size", command=decrease_font_size, font=("TkDefaultFont", 14))
            decrease_font_btn.pack(side=tk.TOP, fill=tk.X)
            template_maker_btn = tk.Button(frame, text="Open Template Maker", command=open_template_maker, font=("TkDefaultFont", 14))
            template_maker_btn.pack(side=tk.TOP, fill=tk.X)
        else:
            # Add cell name as a label
            cell_name = f"{row * 3 + col + 1:02}"
            label = tk.Label(root, text=cell_name, font=("TkDefaultFont", 14))
            label.grid(row=row, column=col, padx=5, pady=(5, 0), sticky="nsew")
            # Text input fields for other cells
            frame = tk.Frame(root)
            frame.grid(row=row, column=col, padx=5, pady=(0, 5), sticky="nsew")
            entry = tk.Text(frame, wrap='word', height=1, font=("TkDefaultFont", 14))
            entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar = tk.Scrollbar(frame, command=entry.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            entry.config(yscrollcommand=scrollbar.set)
            entries[row][col] = entry

# Start the Tkinter loop
root.mainloop()
