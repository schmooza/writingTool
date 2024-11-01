import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
import json
from spellchecker import SpellChecker

highlight_errors = False  # State for highlight toggle
highlight_specific_word_active = False  # State for specific word highlight toggle
font_size = 10  # Initial font size

# Function to export data to JSON file
def export_json():
    data = {}
    for row in range(3):
        for col in range(3):
            if entries[row][col] is not None:
                cell_name = f"{row}{col}"
                cell_data = entries[row][col].get("1.0", tk.END).strip()
                data[cell_name] = cell_data
    file_path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[("JSON files", "*.json")])
    if file_path:
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file)

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
                    # Handle any improperly formatted keys gracefully
                    pass

# Function to spell check and highlight misspelled words
def spell_check_highlight():
    spell = SpellChecker()
    for row in range(3):
        for col in range(3):
            if entries[row][col] is not None:
                text_widget = entries[row][col]
                text_widget.tag_remove('misspelled', '1.0', tk.END)
                text = text_widget.get("1.0", tk.END).strip()
                words = text.split()
                misspelled = spell.unknown(words)
                for word in misspelled:
                    start_idx = "1.0"
                    while True:
                        start_idx = text_widget.search(word, start_idx, stopindex=tk.END, nocase=True)
                        if not start_idx:
                            break
                        end_idx = f"{start_idx}+{len(word)}c"
                        text_widget.tag_add('misspelled', start_idx, end_idx)
                        start_idx = end_idx
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
def spell_check_suggestions():
    spell = SpellChecker()
    corrections = {}

    for row in range(3):
        for col in range(3):
            if entries[row][col] is not None:
                text_widget = entries[row][col]
                text = text_widget.get("1.0", tk.END).strip()
                words = text.split()
                misspelled = spell.unknown(words)
                for word in misspelled:
                    if word in corrections:
                        suggestion = corrections[word]
                    else:
                        suggestions = spell.candidates(word)
                        suggestion = simpledialog.askstring("Spell Check", f"Suggestions for '{word}': {', '.join(suggestions)}\nEnter correction:", initialvalue=spell.correction(word))
                        if suggestion:
                            apply_to_all = messagebox.askyesno("Spell Check", f"Apply correction '{suggestion}' to all occurrences of '{word}'?")
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

# Function to decrease font size
def decrease_font_size():
    global font_size
    if font_size > 1:
        font_size -= 1
    update_font_size()

# Function to update the font size of all text widgets
def update_font_size():
    for row in range(3):
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
root.title("3x3 Grid with JSON Import/Export")
root.rowconfigure([0, 1, 2], weight=1)
root.columnconfigure([0, 1, 2], weight=1)

# Create grid and entries
entries = [[None for _ in range(3)] for _ in range(3)]
for row in range(3):
    for col in range(3):
        if row == 0 and col == 0:
            # Menu items cell
            frame = tk.Frame(root)
            frame.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
            import_btn = tk.Button(frame, text="Import JSON", command=import_json)
            import_btn.pack(side=tk.TOP, fill=tk.X)
            export_btn = tk.Button(frame, text="Export JSON", command=export_json)
            export_btn.pack(side=tk.TOP, fill=tk.X)
            highlight_btn = tk.Button(frame, text="Highlight Spelling Errors", command=toggle_highlight)
            highlight_btn.pack(side=tk.TOP, fill=tk.X)
            highlight_word_btn = tk.Button(frame, text="Highlight Specific Word", command=highlight_specific_word)
            highlight_word_btn.pack(side=tk.TOP, fill=tk.X)
            spell_check_suggest_btn = tk.Button(frame, text="Spell Check with Suggestions", command=spell_check_suggestions)
            spell_check_suggest_btn.pack(side=tk.TOP, fill=tk.X)
            increase_font_btn = tk.Button(frame, text="Increase Font Size", command=increase_font_size)
            increase_font_btn.pack(side=tk.TOP, fill=tk.X)
            decrease_font_btn = tk.Button(frame, text="Decrease Font Size", command=decrease_font_size)
            decrease_font_btn.pack(side=tk.TOP, fill=tk.X)
        else:
            # Add cell name as a label
            cell_name = f"{row}{col}"
            label = tk.Label(root, text=cell_name)
            label.grid(row=row, column=col, padx=5, pady=(5, 0), sticky="nsew")
            # Text input fields for other cells
            frame = tk.Frame(root)
            frame.grid(row=row, column=col, padx=5, pady=(0, 5), sticky="nsew")
            entry = tk.Text(frame, wrap='word', height=1, font=("TkDefaultFont", font_size))
            entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar = tk.Scrollbar(frame, command=entry.yview)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            entry.config(yscrollcommand=scrollbar.set)
            entries[row][col] = entry

# Start the Tkinter loop
root.mainloop()
