import cv2
import numpy as np
import pywt
import tkinter as tk
from tkinter import filedialog, Label, Button, Scale, HORIZONTAL, Canvas
from PIL import Image, ImageTk

class ImageProcessorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Procesare Imagini - OpenCV")

        self.image_label = Label(root)
        self.image_label.pack()

        self.load_button = Button(root, text="Incarca Imagine", command=self.load_image)
        self.load_button.pack()

        self.reset_button = Button(root, text="Reseteaza Imaginea", command=self.reset_image)
        self.reset_button.pack()

        self.save_button = Button(root, text="Salveaza Imaginea", command=self.save_image)
        self.save_button.pack()

        self.kernel_size = Scale(root, from_=1, to=31, orient=HORIZONTAL, label="M\u0103rime Kernel", length=300)
        self.kernel_size.set(5)
        self.kernel_size.pack()

        self.gamma_value = Scale(root, from_=0.1, to=5, resolution=0.1, orient=HORIZONTAL, label="Valoare Gamma", length=300)
        self.gamma_value.set(1.0)
        self.gamma_value.pack()

        self.alpha_value = Scale(root, from_=0.1, to=3, resolution=0.1, orient=HORIZONTAL, label="Contrast", length=300)
        self.alpha_value.set(1.0)
        self.alpha_value.pack()

        self.beta_value = Scale(root, from_=-100, to=100, orient=HORIZONTAL, label="Luminozitate", length=300)
        self.beta_value.set(0)
        self.beta_value.pack()

        self.filter_button = Button(root, text="Filtru Gaussian", command=self.apply_gaussian_blur)
        self.filter_button.pack()

        self.median_button = Button(root, text="Filtru Median", command=self.apply_median_filter)
        self.median_button.pack()

        self.edge_button = Button(root, text="Detectie Margini (Canny)", command=self.edge_detection)
        self.edge_button.pack()

        self.gamma_button = Button(root, text="Corectie Gamma", command=self.apply_gamma_correction)
        self.gamma_button.pack()

        self.contrast_button = Button(root, text="Ajustare Contrast si Luminozitate", command=self.adjust_contrast_brightness)
        self.contrast_button.pack()

        self.wavelet_button = Button(root, text="Transformare Wavelet", command=self.apply_wavelet_transform)
        self.wavelet_button.pack()

        self.image = None
        self.original_image = None
        self.processed_image = None

    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = cv2.imread(file_path)
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            self.original_image = self.image.copy()
            self.display_image(self.image)

    def reset_image(self):
        if self.original_image is not None:
            self.image = self.original_image.copy()
            self.display_image(self.image)

    def save_image(self):
        if self.processed_image is not None:
            file_path = filedialog.asksaveasfilename(defaultextension=".png")
            if file_path:
                img = cv2.cvtColor(self.processed_image, cv2.COLOR_RGB2BGR)
                cv2.imwrite(file_path, img)

    def display_image(self, img):
        self.processed_image = img
        img = Image.fromarray(img)
        img = ImageTk.PhotoImage(img)
        self.image_label.config(image=img)
        self.image_label.image = img

    def apply_gaussian_blur(self):
        if self.image is not None:
            k = self.kernel_size.get()
            k = k if k % 2 == 1 else k + 1
            blurred = cv2.GaussianBlur(self.image, (k, k), 0)
            self.display_image(blurred)

    def apply_median_filter(self):
        if self.image is not None:
            k = self.kernel_size.get()
            k = k if k % 2 == 1 else k + 1
            median = cv2.medianBlur(self.image, k)
            self.display_image(median)

    def edge_detection(self):
        if self.image is not None:
            gray = cv2.cvtColor(self.image, cv2.COLOR_RGB2GRAY)
            edges = cv2.Canny(gray, 100, 200)
            edges_rgb = cv2.cvtColor(edges, cv2.COLOR_GRAY2RGB)
            self.display_image(edges_rgb)

    def apply_gamma_correction(self):
        if self.image is not None:
            gamma = self.gamma_value.get()
            corrected = np.power(self.image / 255.0, gamma) * 255.0
            corrected = np.uint8(corrected)
            self.display_image(corrected)

    def adjust_contrast_brightness(self):
        if self.image is not None:
            alpha = self.alpha_value.get()
            beta = self.beta_value.get()
            adjusted = cv2.convertScaleAbs(self.image, alpha=alpha, beta=beta)
            self.display_image(adjusted)

    def apply_wavelet_transform(self):
        if self.image is not None:
            coeffs = pywt.dwt2(self.image, 'haar')
            cA, (cH, cV, cD) = coeffs
            cA = np.clip(cA, 0, 255).astype(np.uint8)
            self.display_image(cA)

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessorApp(root)
    root.mainloop()
