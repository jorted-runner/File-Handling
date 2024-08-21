import os
import shutil
import tkinter
from tkinter import ttk
from msgtopdf import Msgtopdf

import fetch_files
import utilities
import file_convert
import OCR

program_file = os.path.dirname(os.path.abspath(__file__))
not_OCRed_directory = os.path.join(program_file, "Original Not OCRed")
ocr_data_directory = os.path.join(program_file, "OCR-DATA")

root = tkinter.Tk()
root.title("Folder OCR")

options = ["OCR", "Convert Files to PDF", "Convert MSG to PDF", "Convert HEIC to JPEG", "Convert audio or video to MP4"]
file_fetcher = fetch_files.FetchFiles()
utils = utilities.Utils()
converter = file_convert.converter()
ocr_engine = OCR.ocr()

def decision_time():
    function_selected = option_select.get()
    user_path = path_entry.get()
    if function_selected == options[0]:
        trigger_OCR(user_path)
    elif function_selected == options[1]:
        file_conversion(user_path)
    elif function_selected == options[2]:
        msg_conversion_process(user_path)
    elif function_selected == options[3]:
        heic_to_jpeg(user_path)
    elif function_selected == options[4]:
        file_to_mp4(user_path)

def file_conversion(user_path):
    all_files = file_fetcher.fetch_all_files_recursive(user_path)
    errors = []
    for file in all_files:
        directory, file_w_ext, file_name, file_extension = utils.file_data(file)
        try:
            if file_extension == ".txt":
                converter.txt_to_pdf(directory, file_name, file_extension)
            elif file_extension in ['.png', '.jpg', '.jpeg', '.bmp']:
                converter.image_to_pdf(directory, file_name, file_extension)
            elif file_extension == ".docx":
                converter.docx_to_pdf(directory, file_name, file_extension)
            elif file_extension == ".doc":
                converter.doc_to_pdf(directory, file_name, file_extension)
        except Exception as e:
            error = f"{file} | {e}"
            errors.append(error)
    if errors:
        show_messages(errors, "Errors")
    else:
        show_messages(errors, "Done")
    reset_entries()

def msg_conversion_process(user_path):
    all_files = file_fetcher.fetch_all_files_recursive(user_path)
    errors = []
    for file in all_files:
        root_directory, file_w_ext, file_name, file_extension = utils.file_data(file)
        if file_extension == ".msg":
            try:
                email = Msgtopdf(file)
                email.email2pdf()
            except Exception as e:
                error = f"{file} | {e}"
                errors.append(error)
    if errors:
        show_messages(errors, "Errors")
    else:
        show_messages(errors, "Done")
    reset_entries()

def heic_to_jpeg(user_path):
    all_files = file_fetcher.fetch_all_files_recursive(user_path)
    errors = []
    for file in all_files:
        root_directory, file_w_ext, file_name, file_extension = utils.file_data(file)
        if file_extension == ".heic":
            try:
                heic_file = file
                jpg_file = os.path.join(root_directory, f"{file_name}.jpeg")
                converter.convert_heic_to_jpg(heic_file, jpg_file)
            except Exception as e:
                error = f"{file} | {e}"
                errors.append(error)
    if errors:
        show_messages(errors, "Errors")
    else:
        show_messages(errors, "Done")
    reset_entries()

def file_to_mp4(user_path):
    all_files = file_fetcher.fetch_all_files_recursive(user_path)
    errors = []
    for file in all_files:
        root_directory, file_w_ext, file_name, file_extension = utils.file_data(file)
        if file_extension.lower() == ".mov":
            converter.mov_to_mp4(root_directory, file_name, file_extension)
        elif file_extension.lower() == ".aac":
            converter.convert_audio(file, os.path.join(root_directory, file_name + ".mp4"), 'mp4')
        elif file_extension.lower() == ".m4a":
            converter.m4a_to_mp4(root_directory, file_name, file_extension)
        elif file_extension.lower() == '.gif':
                converter.gif_to_mp4(root_directory, file_name, file_extension)
        elif file_extension.lower() == '.mpg':
                converter.mpg_to_mp4(root_directory, file_name, file_extension)
    if errors:
        show_messages(errors, "Errors")
    else:
        show_messages(errors, "Done")
    reset_entries()
    

def trigger_OCR(user_path):
    messagebox = tkinter.Toplevel(root)
    messagebox.title("Working")
    messagebox.geometry("500x100")
    
    message_label = tkinter.Label(messagebox, text="Working on those files, this window will close when the process is finished.")
    message_label.pack(pady=20)
    messagebox.protocol("WM_DELETE_WINDOW", lambda: None)
    utils.create_folders([ocr_data_directory, not_OCRed_directory])
    all_files = file_fetcher.fetch_all_files(user_path)
    ocred_pdfs = []
    error_pdfs = []
    for i, file in enumerate(all_files, start=1):
        root_directory, file_w_ext, file_name, file_extension = utils.file_data(file)
        if file_extension.lower() == ".pdf":
            try:
                shutil.copy2(file, not_OCRed_directory)
            except Exception as e:
                print(e)
            copied_file = os.path.join(not_OCRed_directory, file_w_ext)
            needs_OCRed = ocr_engine.check_OCR(copied_file)
            try:
                if needs_OCRed:
                    OCR_process(file, root_directory, file_w_ext, file_name)
                    ocred_pdfs.append(file)
                else:
                    pass
            except Exception as e:
                error = f"{e} - {file}"
                error_pdfs.append(error)
        root.update()
    if len(error_pdfs) > 0:
        show_messages(error_pdfs, message_type="errors")
    if len(ocred_pdfs) > 0:
        show_messages(ocred_pdfs, message_type="OCRed")
    if len(ocred_pdfs) == 0 and len(error_pdfs) == 0:
        show_messages(messages=[], message_type="none")
    root.after(2000, messagebox.destroy)
    reset_entries()

def reset_entries():
    root.after(2000, path_entry.delete(0, tkinter.END))
    option_select.set("Pick a function to execute")
    start_button.config(state=tkinter.DISABLED)

def show_messages(messages, message_type):
    error_message_box = tkinter.Toplevel(root)
    error_message_box.title(message_type.capitalize())

    canvas = tkinter.Canvas(error_message_box, height=500)
    canvas.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=True)

    scrollbar = tkinter.Scrollbar(error_message_box, command=canvas.yview)
    scrollbar.pack(side=tkinter.RIGHT, fill=tkinter.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    frame = tkinter.Frame(canvas)
    canvas.create_window((0, 0), window=frame, anchor="nw")
    total_height = 0

    if messages:
        max_width = 500
        title_label = tkinter.Label(frame, text=f"{message_type.capitalize()}:")
        title_label.grid(sticky="w", padx=20, pady=20)
        total_height += title_label.winfo_reqheight() + 20

        for i, file in enumerate(messages):
            message_label = tkinter.Label(frame, text=f"{file}")
            message_label.grid(sticky="w", padx=20, pady=10)

            label_width = message_label.winfo_reqwidth()
            if label_width > max_width:
                max_width = label_width

            label_height = message_label.winfo_reqheight()
            total_height += label_height + 10

    else:
        max_width = 200
        if message_type == "Done":
            title_label = tkinter.Label(frame, text="PDF Conversion Successful")
        else:
            title_label = tkinter.Label(frame, text="No files needed to be OCRed, nothing done.")
        title_label.grid(sticky="w", padx=20, pady=20)
        label_width = title_label.winfo_reqwidth()
        if label_width > max_width:
                max_width = label_width
        total_height = title_label.winfo_reqheight() + 20

    frame.grid_rowconfigure(0, weight=1)

    close_button = tkinter.Button(frame, text="Ok", command=lambda: close_error(error_message_box))
    close_button.grid(row=len(messages) + 1, column=0, pady=20)

    window_height = total_height + close_button.winfo_reqheight()
    window_height = min(window_height, 500)
    error_message_box.geometry(f"{max_width + 40}x{window_height + 50}")

    window_width = error_message_box.winfo_width()
    window_height = error_message_box.winfo_height()
    screen_width = error_message_box.winfo_screenwidth()
    screen_height = error_message_box.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    error_message_box.geometry(f"+{x}+{y}")

def close_error(box):
    box.destroy()

def OCR_process(file_path, directory, file_name_ext, file_name):
    ocr_data_folder = os.path.join(ocr_data_directory, file_name)
    utils.create_folders([ocr_data_folder])
    converter.image_conversion(file_path, ocr_data_folder, file_name)
    jpgs = [f for f in os.listdir(ocr_data_folder) if os.path.isfile(os.path.join(ocr_data_folder, f))]
    for page, pic in enumerate(jpgs):
        page += 1
        ocr_engine.OCR(page, pic, ocr_data_folder)
    extracted_files = file_fetcher.fetch_all_files(ocr_data_folder)
    ocr_engine.merge_pdf(extracted_files, file_name, directory)

def display_help():
    os.startfile('HowToUse.pdf')

def option_selected(event):
    selected_option = option_select.get()
    if selected_option == "Pick a function to execute" or not path_entry.get().strip():
        start_button.config(state=tkinter.DISABLED)
    else:
        start_button.config(state=tkinter.NORMAL)

def clear_entry(event):
    path_entry.delete(0, tkinter.END)
    path_entry["fg"] = "black"
    option_selected(None)

frame = tkinter.Frame(master=root)
frame.pack(pady=10, padx=20, fill="both", expand=True)

label = tkinter.Label(master=frame, text="OCR all PDFs in a folder")
label.grid(column=0, columnspan=2, row=0)

example_label = tkinter.Label(master=frame, text="Enter the Folder path below:", justify="left")
example_label.grid(column=0, columnspan=2, row=1)

path_entry = tkinter.Entry(master=frame, width=50, fg="gray")
path_entry.insert(string=r"C:\Users\dee\General", index=0)
path_entry.grid(column=0, columnspan=2, row=2, sticky="w", pady=(10, 5))

option_select = ttk.Combobox(frame, values=options)
option_select.set("Pick a function to execute")
option_select.grid(column=0, row=3, columnspan=2, sticky="ew")

start_button = tkinter.Button(master=frame, text="Start", command=decision_time, state=tkinter.DISABLED)
start_button.grid(column=0, row=4, pady=10, padx=10, sticky="ew")

help_button = tkinter.Button(master=frame, text="Help", command=display_help)
help_button.grid(column=1, row=4, pady=10, padx=10, sticky="ew")

option_select.bind("<<ComboboxSelected>>", option_selected)
path_entry.bind("<FocusIn>", clear_entry)

frame.grid_rowconfigure(0, weight=1)
frame.grid_rowconfigure(1, weight=1)
frame.grid_rowconfigure(2, weight=1)
frame.grid_rowconfigure(3, weight=1)
frame.grid_rowconfigure(4, weight=1)
frame.grid_columnconfigure(0, weight=1)
frame.grid_columnconfigure(1, weight=1)

root.geometry("350x150")
root.mainloop()
