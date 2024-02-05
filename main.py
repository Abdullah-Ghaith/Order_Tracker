import tkinter as tk
import json
from tkinter import simpledialog

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Order Tracker")
        self.geometry("300x300")
        self.current_list = None

        self.listbox = tk.Listbox(self)
        self.listbox.pack(pady=10)

        self.new_list_button = tk.Button(self, text="Make New Item List", command=self.new_list)
        self.new_list_button.pack()

        self.add_item_button = tk.Button(self, text="Add New Item", command=self.new_item)
        self.add_item_button.pack()

        self.listbox.bind('<Double-1>', self.show_items)

        self.data = self.load_data()
        for list_name in self.data:
            self.listbox.insert(tk.END, list_name)

    def load_data(self):
        try:
            with open('data.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def new_list(self):
        list_name = simpledialog.askstring("Input", "Enter list name")
        if list_name:
            self.listbox.insert(tk.END, list_name)
            self.data[list_name] = []

    def new_item(self):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            list_name = self.listbox.get(index)
            self.current_list = list_name
            item_name = simpledialog.askstring("Input", "Enter item name")
            if item_name:
                self.data[list_name].append(item_name)
                self.save_data()

    def show_items(self, event):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            list_name = self.listbox.get(index)
            items = self.data.get(list_name, [])
            tk.messagebox.showinfo("Items", "\n".join(items))

    def save_data(self):
        with open('data.json', 'w') as f:
            json.dump(self.data, f)

if __name__ == "__main__":
    app = Application()
    app.mainloop()