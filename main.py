import tkinter as tk
from tkinter import simpledialog
import json

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Order Tracker")
        self.geometry("300x300")
        self.current_list = None

        self.listbox = tk.Listbox(self)
        self.listbox.pack(pady=10)

        self.item_listbox = tk.Listbox(self)
        self.item_listbox.pack(pady=10)

        self.new_list_button = tk.Button(self, text="Make New Item List", command=self.new_list)
        self.new_list_button.pack()

        self.add_item_button = tk.Button(self, text="Add New Item", command=self.new_item)
        self.add_item_button.pack()

        self.listbox.bind('<Double-1>', self.show_items)

        self.data = self.load_data()
        self.convert_data()
        for list_name in self.data:
            self.listbox.insert(tk.END, list_name)

    def load_data(self):
        try:
            with open('data.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_data(self):
        with open('data.json', 'w') as file:
            json.dump(self.data, file)

    def new_list(self):
        list_name = simpledialog.askstring("Input", "Enter list name")
        if list_name:
            self.data[list_name] = []
            self.listbox.insert(tk.END, list_name)
            self.save_data()

    def new_item(self):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            list_name = self.listbox.get(index)
            self.current_list = list_name
            item_name = simpledialog.askstring("Input", "Enter item name")
            if item_name:
                self.data[list_name].append({'name': item_name, 'checked': False})
                self.save_data()

    def show_items(self, event):
        if self.listbox.curselection():
            index = self.listbox.curselection()[0]
            self.current_list = self.listbox.get(index)  # Store the current list name
            items = self.data.get(self.current_list, [])
            self.item_listbox.delete(0, tk.END)
            for item in items:
                display_name = '*' + item['name'] if item['checked'] else item['name']
                self.item_listbox.insert(tk.END, display_name)
            self.item_listbox.bind('<Double-1>', self.check_off_item)

    def check_off_item(self, event):
        if self.item_listbox.curselection():
            index = self.item_listbox.curselection()[0]
            item = self.item_listbox.get(index)
            if not item.startswith('*'):
                print("Checking")
                self.item_listbox.delete(index)
                self.item_listbox.insert(index, '*' + item)
                self.data[self.current_list][index]['checked'] = True  # Use the current list name
                self.save_data()
            elif item.startswith('*'):
                print("Unchecking")
                self.item_listbox.delete(index)
                self.item_listbox.insert(index, item[1:])
                self.data[self.current_list][index]['checked'] = False  # Use the current list name
                self.save_data()

    def convert_data(self):
        for list_name, items in self.data.items():
            new_items = []
            for item in items:
                if isinstance(item, str):
                    new_items.append({'name': item, 'checked': False})
                else:
                    new_items.append(item)
            self.data[list_name] = new_items
        self.save_data()

if __name__ == "__main__":
    app = Application()
    app.mainloop()