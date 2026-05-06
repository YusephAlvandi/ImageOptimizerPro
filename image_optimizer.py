"""
Image Optimizer Pro - Batch Image Compression Tool
Author: Yuseph Alvandi
GitHub: https://github.com/YusephAlvandi
Description: Compress images while preserving visual quality.
Version: 1.1.0 - Smart Compression (keeps original if compressed is larger)
"""

import customtkinter as ctk
from tkinter import filedialog, messagebox
from PIL import Image
import os
from datetime import datetime
from shutil import copy2

# ============ GLOBAL SETTINGS ============
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
# =========================================

class ImageOptimizerApp:
    def __init__(self):
        self.window = ctk.CTk()
        self.window.title("Image Optimizer Pro")
        self.window.geometry("1000x750")
        self.window.configure(fg_color="#0a0a0a")
        
        self.input_folder = ""
        self.output_folder = ""
        
        # Settings
        self.quality = ctk.IntVar(value=70)
        self.convert_png_to_jpg = ctk.BooleanVar(value=True)
        self.output_format = ctk.StringVar(value="JPEG")
        
        self.setup_ui()
    
    def setup_ui(self):
        # ===== HEADER =====
        header = ctk.CTkFrame(self.window, fg_color="transparent")
        header.pack(fill="x", pady=(30, 20), padx=40)
        
        ctk.CTkLabel(
            header, 
            text="🗜️ Image Optimizer Pro",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color="#1E90FF"
        ).pack()
        
        ctk.CTkLabel(
            header,
            text="Smart Compression: keeps original if compressed version is larger",
            font=ctk.CTkFont(size=14),
            text_color="#AAAAAA"
        ).pack(pady=5)
        
        # ===== MAIN CONTENT =====
        main = ctk.CTkFrame(self.window, fg_color="#1a1a1a", corner_radius=16, border_width=1, border_color="#333333")
        main.pack(fill="both", expand=True, padx=40, pady=10)
        
        # ---- Folder Selection ----
        folder_section = self.create_section(main, "📁 Folder Selection")
        folder_section.pack(fill="x", padx=25, pady=(20, 10))
        
        # Input folder
        input_row = ctk.CTkFrame(folder_section, fg_color="transparent")
        input_row.pack(fill="x", pady=8)
        ctk.CTkLabel(input_row, text="Input:", font=ctk.CTkFont(size=13, weight="bold"), width=60).pack(side="left")
        ctk.CTkButton(input_row, text="Browse", width=100, height=32, corner_radius=8, 
                     command=self.select_input, font=ctk.CTkFont(size=12)).pack(side="left", padx=10)
        self.label_input = ctk.CTkLabel(input_row, text="Not selected", text_color="#888888", font=ctk.CTkFont(size=12))
        self.label_input.pack(side="left")
        
        # Output folder
        output_row = ctk.CTkFrame(folder_section, fg_color="transparent")
        output_row.pack(fill="x", pady=8)
        ctk.CTkLabel(output_row, text="Output:", font=ctk.CTkFont(size=13, weight="bold"), width=60).pack(side="left")
        ctk.CTkButton(output_row, text="Browse", width=100, height=32, corner_radius=8,
                     command=self.select_output, font=ctk.CTkFont(size=12)).pack(side="left", padx=10)
        self.label_output = ctk.CTkLabel(output_row, text="Not selected", text_color="#888888", font=ctk.CTkFont(size=12))
        self.label_output.pack(side="left")
        
        # ---- Optimization Settings ----
        opt_section = self.create_section(main, "⚙️ Optimization Settings")
        opt_section.pack(fill="x", padx=25, pady=10)
        
        # Quality slider
        qual_row = ctk.CTkFrame(opt_section, fg_color="transparent")
        qual_row.pack(fill="x", pady=8)
        ctk.CTkLabel(qual_row, text="Quality:", font=ctk.CTkFont(size=13, weight="bold"), width=80).pack(side="left")
        self.quality_slider = ctk.CTkSlider(qual_row, from_=10, to=95, variable=self.quality, width=300, command=self.update_quality_label)
        self.quality_slider.pack(side="left", padx=10)
        self.qual_label = ctk.CTkLabel(qual_row, text="70%", font=ctk.CTkFont(size=13, weight="bold"), width=50)
        self.qual_label.pack(side="left")
        
        ctk.CTkLabel(opt_section, text="Lower quality = Smaller file size (but may keep original if larger)", 
                    font=ctk.CTkFont(size=11, slant="italic"), text_color="#888").pack(anchor="w", padx=30, pady=(5, 8))
        
        # PNG to JPG conversion
        self.png_check = ctk.CTkCheckBox(
            opt_section, text="Convert PNG images to JPEG (drastically reduces file size)",
            variable=self.convert_png_to_jpg, font=ctk.CTkFont(size=13)
        )
        self.png_check.pack(anchor="w", padx=30, pady=8)
        
        # ---- Process Button ----
        btn_frame = ctk.CTkFrame(main, fg_color="transparent")
        btn_frame.pack(fill="x", padx=25, pady=(20, 25))
        
        self.btn_process = ctk.CTkButton(
            btn_frame, text="🗜️ Start Compression", command=self.process_images,
            height=48, font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="#E67E22", hover_color="#D35400", corner_radius=12
        )
        self.btn_process.pack(fill="x")
        
        # ===== STATUS BAR =====
        status_frame = ctk.CTkFrame(self.window, fg_color="#1a1a1a", corner_radius=12, height=45)
        status_frame.pack(fill="x", padx=40, pady=(0, 20))
        status_frame.pack_propagate(False)
        
        self.status_label = ctk.CTkLabel(
            status_frame,
            text="● Ready to optimize images",
            font=ctk.CTkFont(size=13, weight="bold"),
            text_color="#4CAF50"
        )
        self.status_label.pack(pady=10)
    
    def create_section(self, parent, title):
        """Create a titled section frame"""
        section = ctk.CTkFrame(parent, fg_color="#252525", corner_radius=10)
        ctk.CTkLabel(
            section, text=title,
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="#1E90FF"
        ).pack(anchor="w", padx=15, pady=(12, 5))
        return section
    
    def select_input(self):
        """Select input folder"""
        self.input_folder = filedialog.askdirectory(title="Select Input Folder with Images")
        if self.input_folder:
            self.label_input.configure(text=f"✓ {os.path.basename(self.input_folder)}", text_color="#4CAF50")
    
    def select_output(self):
        """Select output folder"""
        self.output_folder = filedialog.askdirectory(title="Select Output Folder for Compressed Images")
        if self.output_folder:
            self.label_output.configure(text=f"✓ {os.path.basename(self.output_folder)}", text_color="#4CAF50")
    
    def update_quality_label(self, value):
        """Update quality percentage label"""
        self.qual_label.configure(text=f"{int(float(value))}%")
    
    def get_file_size_mb(self, filepath):
        """Get file size in MB"""
        try:
            size_bytes = os.path.getsize(filepath)
            return size_bytes / (1024 * 1024)
        except:
            return 0.0
    
    def smart_compress(self, img, input_path, output_path, original_size_mb, quality_val):
        """Compress image and keep the smaller version"""
        name_without_ext = os.path.splitext(os.path.basename(input_path))[0]
        output_ext = os.path.splitext(output_path)[1]
        
        # Attempt compression
        if output_ext.lower() in ('.jpg', '.jpeg'):
            if img.mode != 'RGB':
                img = img.convert('RGB')
            img.save(output_path, 'JPEG', quality=quality_val, optimize=True, subsampling=2)
        elif output_ext.lower() == '.png':
            img.save(output_path, 'PNG', optimize=True)
        elif output_ext.lower() == '.webp':
            img.save(output_path, 'WEBP', quality=quality_val)
        else:
            img.save(output_path, optimize=True)
        
        # Get compressed size
        compressed_size_mb = self.get_file_size_mb(output_path)
        
        # If compressed is larger, keep original instead
        if compressed_size_mb >= original_size_mb:
            os.remove(output_path)
            final_filename = f"original_{os.path.basename(input_path)}"
            final_path = os.path.join(self.output_folder, final_filename)
            copy2(input_path, final_path)
            return final_path, original_size_mb
        
        return output_path, compressed_size_mb
    
    def process_images(self):
        """Process and compress all images with smart optimization"""
        if not self.input_folder:
            messagebox.showerror("Error", "Please select input folder!")
            return
        if not self.output_folder:
            messagebox.showerror("Error", "Please select output folder!")
            return
        
        quality_val = self.quality.get()
        supported_formats = ('.png', '.jpg', '.jpeg', '.bmp', '.tiff', '.webp')
        
        total_original_size = 0
        total_compressed_size = 0
        processed_count = 0
        skipped_count = 0
        kept_original_count = 0
        
        self.btn_process.configure(state="disabled", text="⏳ Compressing...")
        self.window.update()
        
        for filename in os.listdir(self.input_folder):
            if filename.lower().endswith(supported_formats):
                input_path = os.path.join(self.input_folder, filename)
                
                try:
                    # Get original size
                    original_size_mb = self.get_file_size_mb(input_path)
                    total_original_size += original_size_mb
                    
                    # Open image
                    img = Image.open(input_path)
                    
                    # Determine output format
                    name_without_ext = os.path.splitext(filename)[0]
                    
                    if self.convert_png_to_jpg.get() and filename.lower().endswith('.png'):
                        output_ext = '.jpg'
                        if img.mode in ('RGBA', 'P'):
                            img = img.convert('RGB')
                    else:
                        output_ext = os.path.splitext(filename)[1]
                    
                    output_filename = f"optimized_{name_without_ext}{output_ext}"
                    output_path = os.path.join(self.output_folder, output_filename)
                    
                    # Smart compress (keeps original if larger)
                    final_path, final_size_mb = self.smart_compress(
                        img, input_path, output_path, original_size_mb, quality_val
                    )
                    
                    total_compressed_size += final_size_mb
                    
                    # Check if we kept the original
                    if "original_" in os.path.basename(final_path):
                        kept_original_count += 1
                        self.status_label.configure(
                            text=f"ℹ️ {filename}: kept original ({original_size_mb:.2f}MB - already optimized)",
                            text_color="#888888"
                        )
                    else:
                        reduction = ((original_size_mb - final_size_mb) / original_size_mb) * 100 if original_size_mb > 0 else 0
                        self.status_label.configure(
                            text=f"🔄 {filename}: {original_size_mb:.2f}MB → {final_size_mb:.2f}MB ({reduction:.0f}% smaller)",
                            text_color="#FFAA33"
                        )
                    
                    processed_count += 1
                    self.window.update()
                    
                except Exception as e:
                    skipped_count += 1
                    self.status_label.configure(
                        text=f"⚠️ Skipped: {filename} - {str(e)}",
                        text_color="#FF5555"
                    )
                    self.window.update()
        
        # Show completion
        self.btn_process.configure(state="normal", text="🗜️ Start Compression")
        
        if processed_count > 0:
            total_reduction = ((total_original_size - total_compressed_size) / total_original_size) * 100 if total_original_size > 0 else 0
            
            self.status_label.configure(
                text=f"✅ Done! {processed_count} processed, {kept_original_count} kept as original",
                text_color="#4CAF50"
            )
            
            messagebox.showinfo(
                "Compression Complete! 🎉",
                f"Results:\n\n"
                f"📁 Images processed: {processed_count}\n"
                f"📦 Original total: {total_original_size:.2f} MB\n"
                f"🗜️ Final total: {total_compressed_size:.2f} MB\n"
                f"📉 Space saved: {total_reduction:.0f}%\n"
                f"📋 Kept original: {kept_original_count} images (already optimized)"
            )
        else:
            self.status_label.configure(
                text="⚠️ No images found in input folder",
                text_color="#FFAA33"
            )
    
    def run(self):
        """Run the application"""
        self.window.mainloop()

if __name__ == "__main__":
    app = ImageOptimizerApp()
    app.run()