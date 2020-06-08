from tkinter import *
from tkinter import filedialog
import os

root = Tk()
root.title('Real Serious Substance File Renamer')

root.geometry('400x600')
root.columnconfigure(0, weight=1)

##img = PhotoImage(file="me.png")
##panel = Label(image=img)
##panel.grid(row=0)

## Browse file directory
dirName =''

def fileDialog():
    file_list.delete(0,'end')
    global dirName
    select_dir = filedialog.askdirectory()
    dirName = select_dir
    for file in os.listdir(dirName):
        suffixes = (".png", ".targa", ".tga")
        if file.endswith(suffixes):
            file_list.insert(END, file)
    
browse_button = Button(root, text = 'Find Directory', command=fileDialog, pady=5)
browse_button.grid(row=1, column = 0)

## List of image files

file_list = Listbox(root, height = 10, width = 60,selectmode='multiple')
file_list.grid(row=2)

## Auto rename
auto_name = BooleanVar()

rename_group = LabelFrame(root, text = 'Auto rename', padx = 5, pady = 5)
rename_group.grid(row=3)

mesh_name = Radiobutton(rename_group, text = 'Mesh name', variable=auto_name, value=0)
mesh_name.grid(row=0, column = 0)

material_name = Radiobutton(rename_group, text = 'Material name',variable=auto_name, value=1)
material_name.grid(row=0, column = 1)

## Manual rename
def disableButtons(*args):
    if len(man_rename_string.get()) > 0:
        mesh_name.configure(state = DISABLED)
        material_name.configure(state = DISABLED)
    else:
        mesh_name.configure(state = ACTIVE)
        material_name.configure(state = ACTIVE)

man_rename_string = StringVar()
man_rename_string.trace('w', disableButtons)

man_rename_group = LabelFrame(root, text = 'Create own prefix', padx = 5, pady = 5)
man_rename_group.grid(row=4)

prefix_entry = Entry(man_rename_group, text = 'Type own prefix here', textvariable = man_rename_string)
prefix_entry.grid(row=0, column=0)

texture_name_example = Label(man_rename_group, text = '_AlbedoTransparency.png')
texture_name_example.grid(row=0, column=1)

## Execute button
def rename_all():
    global dirName
    for file in enumerate(file_list.get(0,END)):
        mesh_string = file[1].split('_')
        if len(prefix_entry.get()) == 0:
            if len(mesh_string) > 2:
                if auto_name.get() == False:
                    new_file_name = mesh_string[0] + '_' + mesh_string[-1]
                    os.rename(os.path.join(dirName,file[1]), os.path.join(dirName,new_file_name))
                else:
                    new_file_name = mesh_string[1] + '_' + mesh_string[-1]
                    os.rename(os.path.join(dirName,file[1]), os.path.join(dirName,new_file_name))
            else:
                status['text'] = 'Filename needs to contain both Mesh Name and Material Name'
                break
        else:
            new_file_name = man_rename_string.get() + '_' + mesh_string[-1]
            os.rename(os.path.join(dirName,file[1]), os.path.join(dirName,new_file_name))
            status['text'] = 'Renamed!'

    file_list.delete(0,'end')
    for file in os.listdir(dirName):
        suffixes = (".png", ".targa", ".tga")
        if file.endswith(suffixes):
            file_list.insert(END, file)

def rename_selected():
    try:
        global dirName
        files = file_list.selection_get()
        file_split = files.split('\n')
        for file in file_split:
            mesh_string = file.split('_')
            if len(prefix_entry.get()) == 0:
                if len(mesh_string) > 2:
                    if auto_name.get() == False:
                        new_file_name = mesh_string[0] + '_' + mesh_string[-1]
                        os.rename(os.path.join(dirName,file), os.path.join(dirName,new_file_name))
                    else:
                        new_file_name = mesh_string[1] + '_' + mesh_string[-1]
                        os.rename(os.path.join(dirName,file), os.path.join(dirName,new_file_name))
                else:
                    status['text'] = 'Filename needs to contain both Mesh Name and Material Name'
                    break
            else:
                new_file_name = man_rename_string.get() + '_' + mesh_string[-1]
                os.rename(os.path.join(dirName,file), os.path.join(dirName,new_file_name))

        file_list.delete(0,'end')
        for file in os.listdir(dirName):
            suffixes = (".png", ".targa", ".tga")
            if file.endswith(suffixes):
                file_list.insert(END, file)
    except:
        status['text'] = 'Please select a file first'

execute_button = Button(root, text = 'Rename Selected', height = 2, width = 20, command=rename_selected)
execute_button.grid(row=5)

execute_button = Button(root, text = 'Rename All', height = 2, width = 20, command=rename_all)
execute_button.grid(row=6)

status = Label(root, text ='', pady=10)
status.grid(row=7)

##root.iconbitmap('me.ico')
root.mainloop()
