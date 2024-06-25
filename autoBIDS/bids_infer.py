import os, json, sys, pydicom, subprocess, re
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from collections import defaultdict
from pathlib import Path

## Choose a file
def choose_file(str_msg):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(parent=root, title=str_msg)
    root.after(3000, root.destroy)  # Close the window after 3 seconds
    root.mainloop()
    if file_path:
        print("Selected file:", file_path)
        return file_path
    else:
        print("No file selected")
        sys.exit()
    

## Choose a directory
def choose_directory(str_msg):
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    directory_path = filedialog.askdirectory(parent=root, title=str_msg)  # Open the directory dialog
    root.after(3000, root.destroy)  # Close the window after 3 seconds
    root.mainloop()
    if directory_path:
        print("Selected directory:", directory_path)
        return directory_path
    else:
        print("No directory selected")
        sys.exit()

## get DICOM info
def extract_series_info(dicom_dir):
    series_info = defaultdict(list)
    for root, _, files in os.walk(dicom_dir):
        for file in files:
            if file.endswith('.IMA') or file.endswith('.dcm'):
                dicom_path = os.path.join(root, file)
                try:
                    dicom = pydicom.dcmread(dicom_path)
                    series_desc = dicom.SeriesDescription
                    series_info[series_desc].append(dicom_path)
                except Exception as e:
                    print(f"Could not read {dicom_path}: {e}")
    return series_info # return the dictionary with all filenames and different filetypes
##
class PlaceholderEntry(tk.Entry):
    def __init__(self, master=None, placeholder="PLACEHOLDER", color='grey'):
        super().__init__(master)

        self.placeholder = placeholder
        self.placeholder_color = color
        self.default_fg_color = self['fg']

        self.bind("<FocusIn>", self.foc_in)
        self.bind("<FocusOut>", self.foc_out)

        self.put_placeholder()

    def put_placeholder(self):
        self.insert(0, self.placeholder)
        self['fg'] = self.placeholder_color

    def foc_in(self, *args):
        if self['fg'] == self.placeholder_color:
            self.delete('0', 'end')
            self['fg'] = self.default_fg_color

    def foc_out(self, *args):
        if not self.get():
            self.put_placeholder()

class SeriesInfoGUI:
    def __init__(self, master, series_info, output_path):
        self.master = master
        self.series_info = series_info
        self.output_path = output_path
        self.entries = {}
        
        self.master.title("DICOM Series Information")
        
        row = 0
        tk.Label(master, text="Series Description").grid(row=row, column=0)
        tk.Label(master, text="Data Type").grid(row=row, column=1)
        tk.Label(master, text="BIDS Label").grid(row=row, column=2)
        tk.Label(master, text="Custom Labels").grid(row=row, column=3)
        
        for series_desc in series_info:
            row += 1
            tk.Label(master, text=series_desc).grid(row=row, column=0)
            self.entries[series_desc] = {
                "dataType": PlaceholderEntry(master, placeholder="e.g., anat, func"),
                "modalityLabel": PlaceholderEntry(master, placeholder="e.g., T1w, bold, "),
                "customLabels": PlaceholderEntry(master, placeholder="e.g., acq-mprage, task-rest")
            }
            self.entries[series_desc]["dataType"].grid(row=row, column=1)
            self.entries[series_desc]["modalityLabel"].grid(row=row, column=2)
            self.entries[series_desc]["customLabels"].grid(row=row, column=3)
        
        row += 1
        tk.Button(master, text="Save Config", command=self.save_config).grid(row=row, column=1, columnspan=2)

    def save_config(self):
        config = {"descriptions": []}
        for series_desc, entries in self.entries.items():
            data_type = entries["dataType"].get()
            modality_label = entries["modalityLabel"].get()
            custom_labels = entries["customLabels"].get()
            if data_type == "" or "e.g." in data_type:
                continue
            elif data_type and modality_label:
                config["descriptions"].append({
                    "datatype": data_type if data_type != "e.g., anat, func" else "",
                    "suffix": modality_label if modality_label != "e.g., T1w, bold" else "",
                    "custom_entities": custom_labels if custom_labels != "e.g., acq-mprage, task-rest" else "",
                    "criteria": {
                        "SeriesDescription": series_desc
                    }
                })
        
        with open(self.output_path, 'w') as f:
            json.dump(config, f, indent=4)
        
        messagebox.showinfo("Info", "Configuration saved successfully!")
# Removes all non-alphanumeric characters from the input string.
def make_alphanumeric(input_string):
    return re.sub(r'[^a-zA-Z0-9]', '', input_string)

# first scaffold the dicom folders
def dicom_scaffold(output_path):
    command = [
        '/zi/home/cagatay.guersoy/.conda/envs/dcm2bids/bin/dcm2bids_scaffold',
        '-o', output_path,
        '--force'
    ]
    # Run the command
    result = subprocess.run(command, capture_output=True, text=True)
    return result
# create a function for dicom conversion and other stuff here
# dcm2bids -d /zi/flstorage/group_klips/data/data/fMRI_workgroup/data/RAWDATA/TEST_SEMINAR_HD/ -p sub00 -c config.json -o bids_test --clobber --force_dcm2bids
def dicom_conv(dicom_path, output_path, config_file):
    # Get all subject folder names
    sub_fld = [folder.name for folder in Path(dicom_path).iterdir() if folder.is_dir()]
    if not sub_fld:
        sub_fld = [dicom_path]
    print(sub_fld)
    # Create the output directory if it doesn't exist
    os.makedirs(output_path, exist_ok=True)
    # list of results
    res_list = []
    # Now run everything in a loop there's multiple participants
    if len(sub_fld) > 1:
        for subject_id in sub_fld:
            # Construct the dcm2bids command
            print(make_alphanumeric(subject_id))
            command = [
                '/zi/home/cagatay.guersoy/.conda/envs/dcm2bids/bin/dcm2bids',
                '-d', dicom_path,
                '-p', make_alphanumeric(subject_id),
                '-c', config_file,
                '-o', output_path,
                '--clobber',
                '--force_dcm2bids'
            ]
            
            # Run the command
            result = subprocess.run(command, capture_output=True, text=True)
            res_list.append(result)
    else:
        command = [
                '/zi/home/cagatay.guersoy/.conda/envs/dcm2bids/bin/dcm2bids',
                '-d', dicom_path,
                '-p', 'sub00',
                '-c', config_file,
                '-o', output_path,
                '--clobber',
                '--force_dcm2bids'
            ]
        # Run the command
        result = subprocess.run(command, capture_output=True, text=True)
        res_list.append(result)
    return res_list
# Create an initial checklist for what to run
def show_checklist():
    def submit():
        results = [var.get() for var in var_list]
        print("Checklist results:", results)
        root.destroy()
    root = tk.Tk()
    root.title("Checklist")
    # Define the items in the checklist
    items = ["Create config.json", "Run scaffolding", "Run dcm2bids"]
    var_list = []
    for item in items:
        var = tk.IntVar()
        chk = tk.Checkbutton(root, text=item, variable=var)
        chk.pack(anchor='w')
        var_list.append(var)
    submit_button = tk.Button(root, text="Submit", command=submit)
    submit_button.pack()
    root.mainloop()
    return [var.get() for var in var_list]

#
def config_create(dicom_dir, output_path):
    series_info = extract_series_info(dicom_dir)
    root = tk.Tk()
    app = SeriesInfoGUI(root, series_info, output_path)
    root.mainloop()

# Run the checklist first
checkList = show_checklist()
# Run the functions
dicom_dir = None
config_output_path = None
if checkList[0]:
    dicom_dir = choose_directory('Choose original DICOM main directory')
    config_output_path = choose_directory('Choose the directory for the resulting config.json file') + os.sep + 'config.json'
    config_create(dicom_dir, config_output_path)
if checkList[1]: # works
    if not dicom_dir:
        dicom_dir = choose_directory('Choose original DICOM main directory')
    output_path = choose_directory('Choose the directory for scaffolding')
    print(dicom_scaffold(output_path))
if checkList[2]:
    if not dicom_dir:
        dicom_dir = choose_directory('Choose original DICOM main directory')
    if not config_output_path:
        config_output_path = choose_file('Choose the config.json file')
    output_path = choose_directory('Choose the directory for DICOM conversion')
    print(dicom_conv(dicom_dir, output_path, config_output_path))
