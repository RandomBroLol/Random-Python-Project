import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os
import subprocess
import urllib.request
import requests
import sys

# Directory and file paths
ASSETS_DIR = "Assets"
SETTINGS_FILE = os.path.join(ASSETS_DIR, "settings.json")
APP_FOLDER = os.path.dirname(os.path.abspath(__file__))
APP_VERSION_FILE = os.path.join(APP_FOLDER, "version.json")
GITHUB_REPO = "RandomBroLol/Random-Python-Project"  # Replace with your GitHub repository
VERSION_FILE_URL = f"https://raw.githubusercontent.com/{GITHUB_REPO}/main/version.json"

# Ensure the Assets directory exists
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

# Function to load settings from a file
def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    return {"theme": "light", "screen_size": "400x300"}

# Function to save settings to a file
def save_settings(settings):
    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f)

# Function to apply the theme
def apply_theme(theme, window):
    if theme == "dark":
        window.configure(bg='#34495e')
        style.configure('TLabel', foreground='#ecf0f1', background='#34495e')
        style.configure('TButton', foreground='#000000', background='#2c3e50')
        style.map('TButton', background=[('active', '#1F2C39')], foreground=[('active', '#000000')])
        style.configure('TEntry', foreground='#000000', background='#34495e')
    elif theme == "blood":
        window.configure(bg='#8B0000')
        style.configure('TLabel', foreground='#ffffff', background='#8B0000')
        style.configure('TButton', foreground='#000000', background='#5C0002')
        style.map('TButton', background=[('active', '#8B0000')], foreground=[('active', '#000000')])
        style.configure('TEntry', foreground='#000000', background='#8B0000')
    else:
        window.configure(bg='#ffffff')
        style.configure('TLabel', foreground='#000000', background='#ffffff')
        style.configure('TButton', foreground='#000000', background='#dddddd')
        style.map('TButton', background=[('active', '#cccccc')], foreground=[('active', '#000000')])
        style.configure('TEntry', foreground='#000000', background='#ffffff')

# Function to set the theme
def set_theme(theme):
    global current_settings
    current_settings["theme"] = theme
    save_settings(current_settings)
    apply_theme(current_settings["theme"], root)
    for window in open_windows:
        apply_theme(current_settings["theme"], window)

# Function to set the screen size and apply to all windows
def set_screen_size_and_apply(value):
    global current_settings
    current_settings["screen_size"] = value
    save_settings(current_settings)
    root.geometry(current_settings["screen_size"])
    for window in open_windows:
        window.geometry(current_settings["screen_size"])

# Function to download a file from a URL and open it
def download_and_run(url, name):
    try:
        # Download the file
        file_path = os.path.join(ASSETS_DIR, f"{name}.exe")
        urllib.request.urlretrieve(url, file_path)

        # Open the downloaded file
        subprocess.Popen(file_path)
        
        messagebox.showinfo("Success", f"{name} installer has been downloaded and executed.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download or execute {name} installer.\nError: {e}")

# Function to create the program installer window
def open_program_installer_window():
    global program_installer_window
    program_installer_window = tk.Toplevel(root)
    open_windows.append(program_installer_window)
    program_installer_window.title("Program Installer")
    program_installer_window.geometry(current_settings["screen_size"])
    apply_theme(current_settings["theme"], program_installer_window)

    programs = {
        "WinRAR": "https://www.rarlab.com/rar/winrar-x64-621.exe",
        "7-Zip": "https://www.7-zip.org/a/7z1900-x64.exe",
        "Notepad++": "https://notepad-plus-plus.org/repository/7.x/7.8.9/npp.7.8.9.Installer.exe",
        "Python": "https://www.python.org/ftp/python/3.9.5/python-3.9.5-amd64.exe",
        "Roblox FPS": "http://example.com/roblox_fps_installer.exe"  # Replace with the actual link
    }

    for name, url in programs.items():
        button = ttk.Button(program_installer_window, text=name, command=lambda u=url, n=name: download_and_run(u, n), style='TButton')
        button.pack(pady=10)

def open_browsers_window():
    global browsers_window
    browsers_window = tk.Toplevel(root)
    open_windows.append(browsers_window)
    browsers_window.title("Download Browsers")
    browsers_window.geometry(current_settings["screen_size"])
    apply_theme(current_settings["theme"], browsers_window)

    browsers = {
        "Chrome": "https://dl.google.com/chrome/install/latest/chrome_installer.exe",
        "Edge": "https://go.microsoft.com/fwlink/?linkid=2108834",
        "Firefox": "https://download.mozilla.org/?product=firefox-latest&os=win&lang=en-US",
        "Supermium": "http://example.com/supermium_installer.exe",  # Replace with the actual link
        "Chrome TOO": "http://example.com/chrome_too_installer.exe"  # Replace with the actual link
    }

    for name, url in browsers.items():
        button = ttk.Button(browsers_window, text=name, command=lambda u=url, n=name: download_and_run(u, n), style='TButton')
        button.pack(pady=10)

def open_settings_window():
    global settings_window
    settings_window = tk.Toplevel(root)
    open_windows.append(settings_window)
    settings_window.title("Settings")
    settings_window.geometry(current_settings["screen_size"])
    apply_theme(current_settings["theme"], settings_window)

    screen_sizes = ["400x300", "600x400", "800x600", "1024x768", "1280x720", "1920x1080"]
    for size in screen_sizes:
        button = ttk.Button(settings_window, text=size, command=lambda v=size: set_screen_size_and_apply(v), style='TButton')
        button.pack(pady=5)

    theme_label = ttk.Label(settings_window, text="Select Theme:", style='TLabel')
    theme_label.pack(pady=5)
    
    themes = {"Light": "light", "Dark": "dark", "Blood": "blood"}
    for name, value in themes.items():
        button = ttk.Button(settings_window, text=name, command=lambda v=value: set_theme(v), style='TButton')
        button.pack(pady=5)

    check_updates_button = ttk.Button(settings_window, text="Check for Updates", command=check_for_updates_manually, style='TButton')
    check_updates_button.pack(pady=10)

def open_more_window():
    global more_window
    more_window = tk.Toplevel(root)
    open_windows.append(more_window)
    more_window.title("More Options")
    more_window.geometry(current_settings["screen_size"])
    apply_theme(current_settings["theme"], more_window)

    discord_webhook_button = ttk.Button(more_window, text="Discord Webhook", command=open_discord_webhook_window, style='TButton')
    discord_webhook_button.pack(pady=10)

    useful_websites_button = ttk.Button(more_window, text="Useful Websites", command=open_useful_websites_window, style='TButton')
    useful_websites_button.pack(pady=10)

def open_discord_webhook_window():
    global discord_webhook_window
    discord_webhook_window = tk.Toplevel(root)
    open_windows.append(discord_webhook_window)
    discord_webhook_window.title("Discord Webhook")
    discord_webhook_window.geometry(current_settings["screen_size"])
    apply_theme(current_settings["theme"], discord_webhook_window)

    webhook_label = ttk.Label(discord_webhook_window, text="Link to Webhook:", style='TLabel')
    webhook_label.pack(pady=5)

    webhook_entry = ttk.Entry(discord_webhook_window, width=50)
    webhook_entry.pack(pady=5)

    def send_message_to_webhook():
        webhook_url = webhook_entry.get()
        message = message_entry.get()
        if webhook_url and message:
            try:
                response = requests.post(webhook_url, json={"content": message})
                if response.status_code == 204:
                    messagebox.showinfo("Success", "Message sent to webhook successfully.")
                else:
                    messagebox.showerror("Error", f"Failed to send message to webhook. Status code: {response.status_code}")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

    message_label = ttk.Label(discord_webhook_window, text="Message:", style='TLabel')
    message_label.pack(pady=5)

    message_entry = ttk.Entry(discord_webhook_window, width=50)
    message_entry.pack(pady=5)

    send_button = ttk.Button(discord_webhook_window, text="Send to Webhook", command=send_message_to_webhook, style='TButton')
    send_button.pack(pady=10)

def open_useful_websites_window():
    global useful_websites_window
    useful_websites_window = tk.Toplevel(root)
    open_windows.append(useful_websites_window)
    useful_websites_window.title("Useful Websites")
    useful_websites_window.geometry(current_settings["screen_size"])
    apply_theme(current_settings["theme"], useful_websites_window)

    websites = [
        "https://www.google.com",
        "https://www.stackoverflow.com",
        "https://www.github.com",
        "https://www.reddit.com",
        "https://www.wikipedia.org",
        # Add more websites here
        "https://www.example1.com",
        "https://www.example2.com",
        "https://www.example3.com"
    ]

    for site in websites:
        entry = ttk.Entry(useful_websites_window, width=50)
        entry.insert(0, site)
        entry.configure(state='readonly', foreground='black')
        entry.pack(pady=5)

def check_for_updates():
    try:
        with urllib.request.urlopen(VERSION_FILE_URL) as response:
            latest_version_data = json.load(response)

        with open(APP_VERSION_FILE, "r") as f:
            current_version_data = json.load(f)

        latest_version = latest_version_data.get("version")
        current_version = current_version_data.get("version")

        if latest_version and latest_version != current_version:
            download_new_version(latest_version)
        else:
            messagebox.showinfo("Up to Date", "The application is up to date.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to check for updates.\nError: {e}")

def download_new_version(version):
    try:
        # Download new version files from GitHub
        # Example: Use urllib.request.urlretrieve() to download the new version files

        # Replace old application files with new version files

        # Relaunch the application with the updated version
        messagebox.showinfo("Update", f"New version {version} is downloaded and ready to use.")
        # Optionally, you can add code here to relaunch the application with the updated version
    except Exception as e:
        messagebox.showerror("Error", f"Failed to download and update the application.\nError: {e}")

def save_version_info(version):
    try:
        with open(APP_VERSION_FILE, "w") as f:
            json.dump({"version": version}, f)
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save version information.\nError: {e}")

# Add this function to your settings window to allow users to manually check for updates
def check_for_updates_manually():
    check_for_updates()

# Main application window
root = tk.Tk()
root.title("Cool Interface")
root.geometry(load_settings()["screen_size"])

# Load current settings
current_settings = load_settings()

# List to keep track of open windows
open_windows = []

# Styling
style = ttk.Style()
style.configure('TLabel', font=('Helvetica', 16, 'bold'))
style.configure('TButton', font=('Helvetica', 12), padding=10)
style.configure('TEntry', font=('Helvetica', 12))

apply_theme(current_settings["theme"], root)

# Adding a title label
title_label = ttk.Label(root, text="Welcome to Browser Installer", style='TLabel')
title_label.pack(pady=20)

# Adding a styled button for installing browsers
install_browsers_button = ttk.Button(root, text="Install Browsers", command=open_browsers_window, style='TButton')
install_browsers_button.pack(pady=10)

# Adding a styled button for program installer
program_installer_button = ttk.Button(root, text="Program Installer", command=open_program_installer_window, style='TButton')
program_installer_button.pack(pady=10)

# Adding a styled button for settings
settings_button = ttk.Button(root, text="Settings", command=open_settings_window, style='TButton')
settings_button.pack(pady=10)

# Adding a styled button for more options
more_button = ttk.Button(root, text="More", command=open_more_window, style='TButton')
more_button.pack(pady=10)

root.mainloop()


