import tkinter as tk
from tkinter import messagebox
import random
import string

# Password Generator App
class PasswordGeneratorApp:
        # Initialize the main window
        def __init__(self, root):
                self.root = root
                self.root.title("Advanced Password Generator")

                # Password length
                self.length_label = tk.Label(root, text="Password Length:")
                self.length_label.grid(row=0, column=0, padx=10, pady=5)
                self.length_entry = tk.Entry(root)
                self.length_entry.grid(row=0, column=1, padx=10, pady=5)

                # Include uppercase letters
                self.uppercase_var = tk.IntVar()
                self.uppercase_check = tk.Checkbutton(root, text="Include Uppercase Letters", variable=self.uppercase_var)
                self.uppercase_check.grid(row=1, column=0, columnspan=2, padx=10, pady=5)

                # Include lowercase letters
                self.lowercase_var = tk.IntVar(value=1)
                self.lowercase_check = tk.Checkbutton(root, text="Include Lowercase Letters", variable=self.lowercase_var)
                self.lowercase_check.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

                # Include digits
                self.digits_var = tk.IntVar(value=1)
                self.digits_check = tk.Checkbutton(root, text="Include Digits", variable=self.digits_var)
                self.digits_check.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

                # Include special characters
                self.special_var = tk.IntVar()
                self.special_check = tk.Checkbutton(root, text="Include Special Characters", variable=self.special_var)
                self.special_check.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

                # Generate button
                self.generate_button = tk.Button(root, text="Generate Password", command=self.generate_password)
                self.generate_button.grid(row=5, column=0, columnspan=2, pady=10)

                # Display generated password
                self.password_label = tk.Label(root, text="Generated Password:")
                self.password_label.grid(row=6, column=0, padx=10, pady=5)
                self.password_display = tk.Entry(root, state='readonly')
                self.password_display.grid(row=6, column=1, padx=10, pady=5)

                # Copy to clipboard button
                self.copy_button = tk.Button(root, text="Copy to Clipboard", command=self.copy_to_clipboard)
                self.copy_button.grid(row=7, column=0, columnspan=2, pady=10)

        # Generate a random password based on the selected options
        def generate_password(self):
                length = self.length_entry.get()
                if not length.isdigit() or int(length) <= 0:
                        messagebox.showerror("Invalid Input", "Please enter a valid length.")
                        return

                length = int(length)
                char_set = ""
                if self.uppercase_var.get():
                        char_set += string.ascii_uppercase
                if self.lowercase_var.get():
                        char_set += string.ascii_lowercase
                if self.digits_var.get():
                        char_set += string.digits
                if self.special_var.get():
                        char_set += string.punctuation

                if not char_set:
                        messagebox.showerror("Invalid Selection", "Please select at least one character set.")
                        return

                password = ''.join(random.choice(char_set) for _ in range(length))
                self.password_display.config(state='normal')
                self.password_display.delete(0, tk.END)
                self.password_display.insert(0, password)
                self.password_display.config(state='readonly')

        # Copy the generated password to the clipboard
        def copy_to_clipboard(self):
                password = self.password_display.get()
                if password:
                        self.root.clipboard_clear()
                        self.root.clipboard_append(password)
                        messagebox.showinfo("Copied to Clipboard", "Password copied to clipboard.")
                else:
                        messagebox.showwarning("No Password", "No password to copy.")

# Main function to run the app
if __name__ == "__main__":
        root = tk.Tk()
        app = PasswordGeneratorApp(root)
        root.mainloop()