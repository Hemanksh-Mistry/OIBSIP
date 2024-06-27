# Importing the required libraries
import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Initialize the main window
class BMICalculatorApp:
        def __init__(self, root):
                self.root = root
                self.root.title("BMI Calculator")

                # Labels and Entry widgets for weight and height
                self.weight_label = tk.Label(root, text="Weight (kg):")
                self.weight_label.pack()
                self.weight_entry = tk.Entry(root)
                self.weight_entry.pack()

                self.height_label = tk.Label(root, text="Height (cm):")
                self.height_label.pack()
                self.height_entry = tk.Entry(root)
                self.height_entry.pack()

                # Button to calculate BMI
                self.calculate_button = tk.Button(root, text="Calculate BMI", command=self.calculate_bmi)
                self.calculate_button.pack()

                # Label to display BMI result
                self.result_label = tk.Label(root, text="")
                self.result_label.pack()

                # Button to view historical data
                self.view_data_button = tk.Button(root, text="View Historical Data", command=self.view_data)
                self.view_data_button.pack()

        def calculate_bmi(self):
                try:
                        weight = float(self.weight_entry.get())
                        height = float(self.height_entry.get()) / 100  # Convert cm to meters

                        if weight <= 0 or height <= 0:
                                raise ValueError

                        bmi = weight / (height ** 2)
                        self.result_label.config(text=f"Your BMI is {bmi:.2f}")

                        self.save_data(weight, height, bmi)
                except ValueError:
                                messagebox.showerror("Input Error", "Please enter valid numerical values for weight and height.")

        def save_data(self, weight, height, bmi):
                try:
                        data = pd.read_csv('bmi_data.csv')
                except FileNotFoundError:
                        data = pd.DataFrame(columns=["Date", "Weight", "Height", "BMI"])

                new_data = {
                        "Date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "Weight": weight,
                        "Height": height * 100,  # Store height in cm
                        "BMI": bmi
                }
                data = data._append(new_data, ignore_index=True)
                data.to_csv('bmi_data.csv', index=False)
                messagebox.showinfo("Data Saved", "Your BMI data has been saved successfully.")

        def view_data(self):
                try:
                        data = pd.read_csv('bmi_data.csv')
                        if data.empty:
                                messagebox.showinfo("No Data", "No historical data available.")
                                return
                except FileNotFoundError:
                        messagebox.showinfo("No Data", "No historical data available.")
                        return

                top = tk.Toplevel(self.root)
                top.title("Historical Data")

                text = tk.Text(top)
                text.pack()
                
                text.insert(tk.END, data.to_string(index=False))

                # Plotting the BMI trend
                data['Date'] = pd.to_datetime(data['Date'])
                data.set_index('Date', inplace=True)
                data['BMI'].plot()
                plt.xlabel('Date')
                plt.ylabel('BMI')
                plt.title('BMI Trend Over Time')
                plt.show()

if __name__ == "__main__":
        root = tk.Tk()
        app = BMICalculatorApp(root)
        root.mainloop()