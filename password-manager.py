from tkinter import Tk, Label, Button, Entry, Listbox, messagebox, Toplevel, END
from tkinter import ttk
import pyperclip

class root_window:
    def __init__(self, root):
        self.root = root
        self.root.title("Password manager")
        self.root.geometry("1200x600+40+40")  # Adjusted width

        head_title = Label(self.root, text="Password Manager", width=40,
                           bg="purple", font=("Arial", 20), padx=10, pady=10, justify="center", anchor="center")
        head_title.grid(columnspan=7, padx=130, pady=20)  # Adjusted columnspan

        self.crud_frame = ttk.Frame(self.root)
        self.crud_frame.grid(row=1, column=0, columnspan=5)  # Adjusted columnspan
        self.create_entry_labels()
        self.create_entry_boxes()

        # Buttons for Save, Update, Copy Paste, and Delete below the entry boxes
        self.save_button = Button(self.crud_frame, text="Save", bg="green", command=self.save_data)
        self.save_button.grid(row=2, column=0, padx=5, pady=2)

        self.update_button = Button(self.crud_frame, text="Update", bg="blue", command=self.update_data)
        self.update_button.grid(row=2, column=1, padx=5, pady=2)

        self.delete_button = Button(self.crud_frame, text="Delete", bg="red", command=self.delete_data)
        self.delete_button.grid(row=2, column=2, padx=5, pady=2)

        self.copy_paste_button = Button(self.crud_frame, text="Copy Paste", bg="cyan", command=self.copy_paste_data)
        self.copy_paste_button.grid(row=2, column=3, padx=5, pady=2)

        # Entry box for searching by website name
        self.search_entry = Entry(self.root, width=20, background="lightgrey", font=("Arial", 12))
        self.search_entry.grid(row=1, column=5, padx=5, pady=2)
        search_button = Button(self.root, text="Search", bg="orange", command=self.search_data)
        search_button.grid(row=1, column=6, padx=5, pady=2)

        # Listbox to display saved items with adjusted width
        self.item_listbox = Listbox(self.root, width=80, height=10, font=("Arial", 12))
        self.item_listbox.grid(row=3, column=0, columnspan=7, padx=10, pady=5, sticky="w")  # Adjusted width and columnspan

        # Dictionary to store website names and corresponding passwords
        self.website_passwords = {}

        # Bind double click event on Listbox to display details in Entry boxes
        self.item_listbox.bind('<Double-1>', self.display_selected_item)

    def create_entry_labels(self):
        labels_info = ('Id', 'Website', 'Username', 'Password')
        self.col_no = 0
        for label_info in labels_info:
            Label(self.crud_frame, text=label_info, bg='grey', fg='white', font=('Arial', 12), padx=5, pady=2).grid(
                row=0, column=self.col_no, padx=5, pady=2)
            self.col_no += 1

    def create_entry_boxes(self):
        self.entry_boxes = []
        self.col_no = 0
        self.row_no = 1  # Incremented row number for entry boxes
        for i in range(4):
            entry_box = Entry(self.crud_frame, width=20, background="lightgrey", font=("Arial", 12))
            entry_box.grid(row=self.row_no, column=self.col_no, padx=5, pady=2)
            self.col_no += 1
            self.entry_boxes.append(entry_box)

    def save_data(self):
        # Check if the website name is already saved
        website_value = self.entry_boxes[1].get()
        password_value = self.entry_boxes[3].get()

        if website_value in self.website_passwords:
            messagebox.showinfo("Already Saved", f"This website ({website_value}) is already saved.")
        else:
            # Display entered website and password in the Listbox
            item_text = f"Website: {website_value}, Username: {self.entry_boxes[2].get()}, Password: {password_value}"
            self.item_listbox.insert("end", item_text)

            # Add the website and password to the dictionary
            self.website_passwords[website_value] = {'Username': self.entry_boxes[2].get(), 'Password': password_value}

    def update_data(self):
        # Get the selected item from the Listbox
        selected_index = self.item_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Select Item", "Please select an item to update.")
            return

        # Get the text of the selected item
        selected_item = self.item_listbox.get(selected_index)

        # Extract website name and password from the selected item
        website_value = selected_item.split(',')[0].split(': ')[1]
        username_value = selected_item.split(',')[1].split(': ')[1]
        password_value = selected_item.split(',')[2].split(': ')[1]

        # Open a new window for updating
        update_window = Toplevel(self.root)
        update_window.title("Update Information")

        # Entry boxes for the updated information
        website_label = Label(update_window, text="Website:")
        website_label.grid(row=0, column=0, padx=5, pady=2)
        updated_website_entry = Entry(update_window, width=20, background="lightgrey", font=("Arial", 12))
        updated_website_entry.insert(0, website_value)
        updated_website_entry.grid(row=0, column=1, padx=5, pady=2)

        username_label = Label(update_window, text="Username:")
        username_label.grid(row=1, column=0, padx=5, pady=2)
        updated_username_entry = Entry(update_window, width=20, background="lightgrey", font=("Arial", 12))
        updated_username_entry.insert(0, username_value)
        updated_username_entry.grid(row=1, column=1, padx=5, pady=2)

        password_label = Label(update_window, text="Password:")
        password_label.grid(row=2, column=0, padx=5, pady=2)
        updated_password_entry = Entry(update_window, width=20, background="lightgrey", font=("Arial", 12))
        updated_password_entry.insert(0, password_value)
        updated_password_entry.grid(row=2, column=1, padx=5, pady=2)

        # Update button in the update window
        update_button = Button(update_window, text="Update", bg="blue", command=lambda: self.perform_update(selected_index, updated_website_entry.get(), updated_username_entry.get(), updated_password_entry.get(), update_window))
        update_button.grid(row=3, column=0, columnspan=2, padx=5, pady=2)

    def perform_update(self, selected_index, updated_website, updated_username, updated_password, update_window):
        # Remove the selected item from the Listbox
        self.item_listbox.delete(selected_index)

        # Add the updated information to the Listbox
        updated_item_text = f"Website: {updated_website}, Username: {updated_username}, Password: {updated_password}"
        self.item_listbox.insert(selected_index, updated_item_text)

        # Update the dictionary with the new information
        if updated_website in self.website_passwords:
            del self.website_passwords[updated_website]
        self.website_passwords[updated_website] = {'Username': updated_username, 'Password': updated_password}

        # Close the update window
        update_window.destroy()

    def delete_data(self):
        # Get the selected item from the Listbox
        selected_index = self.item_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Select Item", "Please select an item to delete.")
            return

        # Get the text of the selected item
        selected_item = self.item_listbox.get(selected_index)

        # Extract website name from the selected item
        website_value = selected_item.split(',')[0].split(': ')[1]

        # Remove the entry from the dictionary
        if website_value in self.website_passwords:
            del self.website_passwords[website_value]
            # Remove the selected item from the Listbox
            self.item_listbox.delete(selected_index)
        else:
            messagebox.showinfo("Not Found", "Selected website not found in the dictionary.")

    def copy_paste_data(self):
        # Get the selected item from the Listbox
        selected_index = self.item_listbox.curselection()
        if not selected_index:
            messagebox.showinfo("Select Item", "Please select an item to copy.")
            return

        # Get the text of the selected item
        selected_item = self.item_listbox.get(selected_index)

        # Extract password from the selected item
        password_value = selected_item.split(',')[2].split(': ')[1]

        # Copy the password to the clipboard
        pyperclip.copy(password_value)
        messagebox.showinfo("Password Copied", "Password copied to clipboard.")

    def search_data(self):
        # Clear the Listbox
        self.item_listbox.delete(0, "end")

        # Get the search term
        search_term = self.search_entry.get().lower()

        # Display items matching the search term
        for website, password_info in self.website_passwords.items():
            if search_term in website.lower():
                item_text = f"Website: {website}, Username: {password_info['Username']}, Password: {password_info['Password']}"
                self.item_listbox.insert("end", item_text)

    def display_selected_item(self, event):
        # Get the selected item from the Listbox
        selected_index = self.item_listbox.curselection()
        if not selected_index:
            return

        # Get the text of the selected item
        selected_item = self.item_listbox.get(selected_index)

        # Extract website, username, and password from the selected item
        website_value = selected_item.split(',')[0].split(': ')[1]
        username_value = selected_item.split(',')[1].split(': ')[1]
        password_value = selected_item.split(',')[2].split(': ')[1]

        # Display the values in the corresponding Entry boxes
        self.entry_boxes[1].delete(0, END)
        self.entry_boxes[1].insert(0, website_value)

        self.entry_boxes[2].delete(0, END)
        self.entry_boxes[2].insert(0, username_value)

        self.entry_boxes[3].delete(0, END)
        self.entry_boxes[3].insert(0, password_value)


if __name__ == "__main__":
    root = Tk()
    root_class = root_window(root)
    root.mainloop()
