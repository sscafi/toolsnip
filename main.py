import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import pyautogui
import pytesseract
import io

# Ensure Tesseract OCR is in your PATH or provide the path explicitly
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Screenshot and Text Extractor")

        # Set up the UI
        self.label = tk.Label(root, text="Select a region to capture")
        self.label.pack(pady=10)

        self.capture_button = tk.Button(root, text="Capture Screen", command=self.capture_screen)
        self.capture_button.pack(pady=10)

        self.quit_button = tk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack(pady=10)

    def capture_screen(self):
        try:
            # Instructions for user
            self.label.config(text="Select the region to capture (drag your mouse).")

            # Get the region coordinates from user
            region = self.select_region()

            if not region:
                messagebox.showwarning("Warning", "No region selected.")
                return

            # Capture the screenshot
            screenshot = pyautogui.screenshot(region=region)

            # Save the screenshot
            image_filename = filedialog.asksaveasfilename(defaultextension=".png",
                                                        filetypes=[("PNG files", "*.png")])
            if not image_filename:
                return  # User canceled

            screenshot.save(image_filename)

            # Extract text from screenshot
            text = pytesseract.image_to_string(screenshot)

            # Save the extracted text
            text_filename = filedialog.asksaveasfilename(defaultextension=".txt",
                                                        filetypes=[("Text files", "*.txt")])
            if not text_filename:
                return  # User canceled

            with open(text_filename, 'w') as file:
                file.write(text)

            messagebox.showinfo("Success", "Screenshot and text saved successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def select_region(self):
        # Hide the main Tkinter window
        self.root.withdraw()

        # Create a new Tkinter window for region selection
        select_window = tk.Toplevel()
        select_window.attributes("-fullscreen", True)
        select_window.attributes("-alpha", 0.3)  # Make the window semi-transparent
        select_window.configure(bg='gray')

        region = [None, None, None, None]

        def on_drag(event):
            if region[0] is None:
                region[0] = event.x_root
                region[1] = event.y_root
            else:
                region[2] = event.x_root
                region[3] = event.y_root
                select_window.update_idletasks()

        def on_release(event):
            if region[0] is not None and region[2] is not None:
                # Calculate the region
                left = min(region[0], region[2])
                top = min(region[1], region[3])
                width = abs(region[2] - region[0])
                height = abs(region[3] - region[1])
                self.root.deiconify()  # Show the main window again
                select_window.destroy()  # Close the region selection window
                return (left, top, width, height)
            return None

        select_window.bind("<ButtonPress-1>", on_drag)
        select_window.bind("<B1-Motion>", on_drag)
        select_window.bind("<ButtonRelease-1>", on_release)
        select_window.mainloop()

        # Return the region as a tuple (left, top, width, height)
        return (left, top, width, height)

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotApp(root)
    root.mainloop()
