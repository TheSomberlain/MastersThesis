import os
import shutil
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from ..Common import common

SOURCE_FOLDER = "C:\Projects\MastersThesis\HMICutter\ROI_EXT"
DESTINATION_FOLDERS = common.DESTINATION_FOLDERS

class ImageSorterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Sorter")

        unsorted_files = [f for f in os.listdir(SOURCE_FOLDER)
                          if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        self.image_files = sorted(
            unsorted_files,
            key=lambda f: self.get_image_area(os.path.join(SOURCE_FOLDER, f)),
            reverse=True
        )

        self.total_images = len(self.image_files)
        self.current_index = 0

        self.image_label = tk.Label(self.root)
        self.image_label.pack(padx=10, pady=10)

        self.counter_label = tk.Label(self.root, text="")
        self.counter_label.pack()

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack()

        for label, dest in DESTINATION_FOLDERS.items():
            btn = tk.Button(self.button_frame, text=label,
                            command=lambda d=dest: self.copy_and_next(d))
            btn.pack(side=tk.LEFT, padx=5)

        self.jump_frame = tk.Frame(self.root)
        self.jump_frame.pack(pady=10)

        self.index_entry = tk.Entry(self.jump_frame, width=5)
        self.index_entry.pack(side=tk.LEFT)
        self.go_button = tk.Button(self.jump_frame, text="Go to", command=self.jump_to_index)
        self.go_button.pack(side=tk.LEFT, padx=5)

        self.show_image()

    def show_image(self):
        if self.current_index >= len(self.image_files):
            messagebox.showinfo("Done", "All images processed.")
            self.root.quit()
            return

        image_path = os.path.join(SOURCE_FOLDER, self.image_files[self.current_index])
        img = Image.open(image_path).resize((400, 400))
        img.thumbnail((600, 600))
        self.tk_img = ImageTk.PhotoImage(img)
        self.image_label.config(image=self.tk_img)
        percent = int(((self.current_index + 1) / self.total_images) * 100)
        self.counter_label.config(
            text=f"Image {self.current_index + 1} / {self.total_images} ({percent}%)"
        )


    def copy_and_next(self, dest_folder):
        src_path = os.path.join(SOURCE_FOLDER, self.image_files[self.current_index])
        os.makedirs(dest_folder, exist_ok=True)
        shutil.copy(src_path, dest_folder)
        self.current_index += 1
        self.show_image()

    def get_image_area(self, path):
        try:
            with Image.open(path) as img:
                width, height = img.size
                return width * height
        except Exception:
            return float('inf')
        
    def jump_to_index(self):
            try:
                index = int(self.index_entry.get()) - 1
                if 0 <= index < self.total_images:
                    self.current_index = index
                    self.show_image()
                else:
                    messagebox.showwarning("Invalid", "Index out of range.")
            except ValueError:
                messagebox.showwarning("Invalid", "Please enter a valid number.")

if __name__ == '__main__':
    root = tk.Tk()
    app = ImageSorterApp(root)
    root.mainloop()