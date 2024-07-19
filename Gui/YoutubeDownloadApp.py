import customtkinter as ctk
import tkinter as tk
from tkinter import Canvas, Menu, messagebox, PhotoImage, filedialog
from PIL import Image
import webbrowser

from Utils import Config
from Backend import VideoDownloader
from Error import DownloadError


class YoutubeDownloadApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        self.config_var = Config()
        self.video_downloader = VideoDownloader()
        
        self.download_button = None
        
        self.title("YouTube Downloader")
        self.iconbitmap(self.config_var.icon_img_path)
        self.resizable(False, False)
        
        self.create_menu()
        self.create_page()
        
    def create_menu(self):
        menubar = Menu(self)
        self.config(menu=menubar)
        
        helpMenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Para mas información", menu=helpMenu)
        helpMenu.add_command(label="Información del autor", command=self.popup)
        
    def popup(self):
        messagebox.showinfo("Sobre la app", "Descarga videos de YouTube y los convierte a mp3.")
        
    def create_page(self):
        canvas = Canvas(self,
                        width=500,
                        height=800,
                        bg=self.config_var.color_bg)
        canvas.pack()
        
        self.logo_img = PhotoImage(file=self.config_var.logo_img_path)
        self.logo_img =self.logo_img.subsample(1, 1)
        canvas.create_image(250, 200, image=self.logo_img)
        
        self.create_widgets()
        
    def create_widgets(self):
        self.create_label("YouTube mp3\nDownloader", 35,  'bold', 400, 'center', 0.5, 0.27)
        self.create_label("Video link", 14, 'bold',0, 'center', 0.25, 0.51)       
        self.inf_video_label = self.create_label("", 14, 'normal',0, 'center', 0.5, 0.70)
        self.estado_label = self.create_label("", 12, 'normal',0, 'left', 0.5, 0.80)   #0.5, 0.70
        self.location_label = self.create_label("", 14, 'normal',0, 'center', 0.5, 0.85) #0.5, 0.80
        self.create_label("GitHub", 14, 'bold', 0, 'center', 0.2, 0.95)  
        self.create_label("Create by Mario Petro", 10, 'normal',  0, 'center', 0.5, 0.95) 
        
        self.url_entry = self.create_entry(260, 30, 14, "Pegue el enlace de su video aquí", 0.40, 0.55)
        
        self.create_button("Start", 14, 'bold', 60, 30,self.config_var.color_bg, self.config_var.color_btn, self.config_var.color_btnDark,self.config_var.arrow_img_path, self.btn_start, 0.85, 0.55)            
        self.create_button("", 0, 'normal', 0, 0, self.config_var.color_bg, self.config_var.color_bg, self.config_var.color_bg, self.config_var.github_img_path, self.open_link, 0.1, 0.95)
        
        
        
    def create_label(self, text, font_size, font_style, width, justify, relx, rely):
        label = ctk.CTkLabel(self,
                             text=text,
                             font=('Arial Rounded MT', font_size, font_style),
                             justify=justify,
                             width=width,
                             text_color=self.config_var.color_text,
                             bg_color=self.config_var.color_bg)
        label.place(relx=relx, rely=rely, anchor=tk.CENTER)
        return label
        
    def create_entry(self, width, height, font_size, placeholder, relx, rely):
        entry = ctk.CTkEntry(self,
                             width=width,
                             height=height,
                             font=('Arial Rounded MT', font_size),
                             placeholder_text=placeholder,
                             text_color=self.config_var.color_text,
                             bg_color=self.config_var.color_bg)
        entry.place(relx=relx, rely=rely, anchor=tk.CENTER)
        return entry
        
    def create_button(self, text, font_size, font_style, width, height, color_bg, color_fg, hover_color, img, command,  relx, rely):
        img_button = ctk.CTkImage(Image.open(img))
        button = ctk.CTkButton(self,
                               text=text,
                               font=('Arial Rounded MT', font_size, font_style),
                               width=width,
                               anchor="center",
                               compound="right",
                               height=height,
                               corner_radius=5,
                               image=img_button,
                               text_color=self.config_var.color_text,
                               bg_color=color_bg,
                               fg_color=color_fg,
                               hover_color=hover_color,
                               command=command
                               )
        button.place(relx=relx, rely=rely, anchor=tk.CENTER)
        return button
    
    def create_combobox(self, width, height, options):
        combobox = ctk.CTkComboBox(self,
                                   width=width,
                                   height=height,
                                   values=options,
                                   command=lambda event=None: self.option_format.get()
                                   )
        combobox.place(relx=0.70, rely=0.63, anchor=tk.CENTER)
        return combobox
    
    def open_link(self):
        webbrowser.open(self.config_var.github_link)
        
    
    def btn_start(self):
        self.reset_wn()
        link = self.url_entry.get()
        if not link:
            return
        
        self.video_downloader.set_url(link)
        self.update_gui_success("Loading...")
        self.update()
        try:
            self.button_quality(self.video_downloader.get_available_resolutions())
            self.button_download()
            self.update()
            
            status = self.video_downloader.format_download_info()
            self.inf_video_label.configure(text=status)
            self.update_gui_failure()
        except DownloadError as e:
            messagebox.showerror("Download Error", str(e))
            self.update_gui_failure()
            
    def reset_wn(self):
        if  self.download_button is not None and self.option_format is not None: 
            self.download_button.destroy()
            self.option_format.destroy()
        self.location_label.configure(text="")
        self.inf_video_label.configure(text="") 
            
    def button_quality(self, quality):
        self.option_format = self.create_combobox(90, 40, quality)
     
    def button_download(self):
         self.download_button = self.create_button("Download", 20, 'bold', 150, 40,self.config_var.color_bg, self.config_var.color_btn, 
                            self.config_var.color_btnDark,self.config_var.download_img_path, self.btn_download, 0.4, 0.63) 
    
    
    def btn_download(self):
        download_path = self.ask_download_path()
        if not download_path:
            return self.location_label.configure(text="")

        self.update_gui_success("Descargando...")
        self.location_label.configure(text=download_path)
        self.update()
        
        self.video_downloader.set_quality(self.option_format.get())
        self.video_downloader.set_download_path(download_path)
        
        try:
            self.video_downloader.download_video()
            self.update_gui_success("Descarga completa.")
        except DownloadError as e:
            messagebox.showerror("Download Error", str(e))
            self.update_gui_failure()
            
                
    def ask_download_path(self):
        return filedialog.askdirectory()
        
    def update_gui_success(self, message):
        self.estado_label.configure(text=message)
        
    def update_gui_failure(self):
        self.estado_label.configure(text="")