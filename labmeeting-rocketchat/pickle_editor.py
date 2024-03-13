'''
A script to check the pickle files with a GUI
Written by ChatGPT entirely
'''
import tkinter as tk
from tkinter import filedialog, messagebox
import pickle

class PickleEditorApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Pickle File Editor")
        self.master.geometry("1000x800")  # Set initial size of the window

        self.text_area = tk.Text(master, height=40, width=100)
        self.text_area.pack(pady=10)

        self.load_button = tk.Button(master, text="Load Pickle File", command=self.load_pickle)
        self.load_button.pack()

        self.save_button = tk.Button(master, text="Save Changes", command=self.save_pickle)
        self.save_button.pack()

        self.data = None

    def load_pickle(self):
        file_path = filedialog.askopenfilename(filetypes=[("Pickle Files", "*.pkl")])
        if file_path:
            with open(file_path, 'rb') as file:
                self.data = pickle.load(file)
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert(tk.END, self.data)

    def save_pickle(self):
        if self.data is None:
            messagebox.showerror("Error", "No data to save. Please load a pickle file first.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".pkl", filetypes=[("Pickle Files", "*.pkl")])
        if file_path:
            with open(file_path, 'wb') as file:
                pickle.dump(self.text_area.get('1.0', tk.END), file)
            messagebox.showinfo("Success", "Changes saved successfully.")

def main():
    root = tk.Tk()
    app = PickleEditorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()