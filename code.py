import tkinter as tk
from tkinter import filedialog, messagebox

class Notepad:
    def __init__(self, master):
        self.master = master
        self.master.title("Notepad Kelompok 1")
        self.file_path = None

        self.text_area = tk.Text(self.master)
        self.text_area.pack(fill=tk.BOTH, expand=True)

        self.create_menu()
        
        # Mengganti warna background atau canvasnya
        self.set_background("#ECE5C7")
        
    def set_background(self, color):
        self.text_area.configure(bg=color)

    def create_menu(self):
        menu_bar = tk.Menu(self.master)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="New", accelerator="Ctrl+N", command=self.new_file)
        file_menu.add_separator()
        file_menu.add_command(label="Open", accelerator="Ctrl+O", command=self.open_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save", accelerator="Ctrl+S", command=self.save_file)
        file_menu.add_separator()
        file_menu.add_command(label="Save As", accelerator="Ctrl+Shift+S", command=self.save_file_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.exit_app)
        menu_bar.add_cascade(label="File", menu=file_menu)

        edit_menu = tk.Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label="Cut", accelerator="Ctrl+X", command=self.cut_text)
        edit_menu.add_command(label="Copy", accelerator="Ctrl+C", command=self.copy_text)
        edit_menu.add_command(label="Paste", accelerator="Ctrl+V", command=self.paste_text)
        edit_menu.add_command(label="Delete", accelerator="Del", command=self.delete_text)
        edit_menu.add_separator()
        edit_menu.add_command(label="Find", accelerator="Ctrl+F", command=self.find_text)
        edit_menu.add_command(label="Replace", accelerator="Ctrl+H", command=self.replace_text)
        menu_bar.add_cascade(label="Edit", menu=edit_menu)

        format_menu = tk.Menu(menu_bar, tearoff=0)
        format_menu.add_command(label="Font", command=self.change_font)
        format_menu.add_separator()
        format_menu.add_command(label="Arial", command=lambda: self.set_font("Arial"))
        format_menu.add_command(label="Times New Roman", command=lambda: self.set_font("Times New Roman"))
        format_menu.add_command(label="Courier New", command=lambda: self.set_font("Courier New"))
        format_menu.add_command(label="Verdana", command=lambda: self.set_font("Verdana"))
        menu_bar.add_cascade(label="Format", menu=format_menu)

        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=self.about)
        menu_bar.add_cascade(label="Help", menu=help_menu)

        self.master.config(menu=menu_bar)

        # Bind keyboard shortcuts
        self.master.bind("<Control-n>", lambda event: self.new_file())
        self.master.bind("<Control-o>", lambda event: self.open_file())
        self.master.bind("<Control-s>", lambda event: self.save_file())
        self.master.bind("<Control-S>", lambda event: self.save_file_as())
        self.master.bind("<Control-x>", lambda event: self.cut_text())
        self.master.bind("<Control-c>", lambda event: self.copy_text())
        self.master.bind("<Control-v>", lambda event: self.paste_text())
        self.master.bind("<Delete>", lambda event: self.delete_text())
        self.master.bind("<Control-f>", lambda event: self.find_text())
        self.master.bind("<Control-h>", lambda event: self.replace_text())

    def new_file(self):
        self.text_area.delete("1.0", tk.END)
        self.file_path = None

    def open_file(self):
        filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if filepath:
            with open(filepath, "r") as file:
                text = file.read()
                self.text_area.delete("1.0", tk.END)
                self.text_area.insert(tk.END, text)
            self.file_path = filepath

    def save_file(self):
        if self.file_path:
            self._save_file()
        else:
            self.save_file_as()

    def save_file_as(self):
        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if filepath:
            self.file_path = filepath
            self._save_file()

    def _save_file(self):
        text = self.text_area.get("1.0", tk.END)
        with open(self.file_path, "w") as file:
            file.write(text)

    def exit_app(self):
        if messagebox.askokcancel("Exit", "Are you sure you want to exit?"):
            self.master.destroy()

    def cut_text(self):
        self.text_area.event_generate("<<Cut>>")

    def copy_text(self):
        self.text_area.event_generate("<<Copy>>")

    def paste_text(self):
        self.text_area.event_generate("<<Paste>>")

    def delete_text(self):
        self.text_area.event_generate("<<Clear>>")

    def find_text(self):
        search_dialog = tk.Toplevel(self.master)
        search_dialog.title("Find")
        
        search_label = tk.Label(search_dialog, text="Find:")
        search_label.pack(side=tk.LEFT)

        search_entry = tk.Entry(search_dialog)
        search_entry.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        search_entry.focus()

        find_button = tk.Button(search_dialog, text="Find", command=lambda: self.find(search_entry.get()))
        find_button.pack(side=tk.LEFT)

    def find(self, search_text):
        start_index = self.text_area.search(search_text, "1.0", tk.END)
        if start_index:
            end_index = f"{start_index}+{len(search_text)}c"
            self.text_area.tag_remove("search", "1.0", tk.END)
            self.text_area.tag_add("search", start_index, end_index)
            self.text_area.tag_config("search", background="yellow")

    def replace_text(self):
        replace_dialog = tk.Toplevel(self.master)
        replace_dialog.title("Replace")

        find_label = tk.Label(replace_dialog, text="Find:")
        find_label.grid(row=0, column=0)

        find_entry = tk.Entry(replace_dialog)
        find_entry.grid(row=0, column=1)

        replace_label = tk.Label(replace_dialog, text="Replace:")
        replace_label.grid(row=1, column=0)

        replace_entry = tk.Entry(replace_dialog)
        replace_entry.grid(row=1, column=1)

        replace_button = tk.Button(replace_dialog, text="Replace",
                                   command=lambda: self.replace(find_entry.get(), replace_entry.get()))
        replace_button.grid(row=2, column=0, columnspan=2)

    def replace(self, search_text, replace_text):
        start_index = self.text_area.search(search_text, "1.0", tk.END)
        if start_index:
            end_index = f"{start_index}+{len(search_text)}c"
            self.text_area.delete(start_index, end_index)
            self.text_area.insert(start_index, replace_text)

    def change_font(self):
        font = filedialog.askstring("Change Font", "Enter font name (e.g., Arial, Times New Roman):")
        if font:
            self.text_area.config(font=font)

    def set_font(self, font_name):
        self.text_area.config(font=(font_name, 12))

    def about(self):
        messagebox.showinfo("About", "Ini adalah program teks sederhana dengan GUI menggunakan Tkinter.")

root = tk.Tk()
notepad = Notepad(root)
root.mainloop()
