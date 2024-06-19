# Jacky Zhou
# Mr. David Park - ICS 4U
# 2024/06/10
# AOL 6 - color selector

import tkinter as tk
from tkinter import ttk
from tkinter import colorchooser
import json
# import threading
import random
#from matplotlib import colors
with open("color_settings.json", "r") as file:
    settings = json.load(file)

color_name_list = []

# Get color list from individual dictionary (include color name and RGB info)
for individual_dict in settings["settings"]:
    color_name_list.append(individual_dict["color_name"])
# Initialize window settings
window = tk.Tk()
window.title("Demonstration")
window.geometry("800x600")
window.config(bg="light gray")
# Initialize color chooser
color_chooser = tk.colorchooser.Chooser(window)
# Display selected color from the drop-down
def color_selection(event_object):
    for i in settings["settings"]:
        if i["color_name"] == menu.get():
            text_label.config(text=menu.get() + " -RGB: " + str(i["color_RGB"][0])+ "," + str(i["color_RGB"][1])+ ","  + str(i["color_RGB"][2])+ " -Hex: " + i["color_hex"])
            color_label.config(bg=i["color_hex"])
# Transfer rgb values (a,b,c) into hexadecimal format
# def from_rgb(rgb):
#     r, g, b = rgb
#     return f'#{r:02x}{g:02x}{b:02x}'
# add color in the drop-down
def add_color(new_color_name):
    # Reset error output
    error_output.config(bg="light gray")
    error_output.config(text="")
    error_output.forget()
    error_output.grid(row=4, column=2)
    # Check if the custom name is blank
    if new_color_name == "":
        error_output.config(bg="red")
        error_output.config(text="Color's name cannot be blank")
        return
    # Check if the custom name is same with one of the exited custom names
    for i in settings["settings"]:
        if i["color_name"] == new_color_name:
            error_output.config(bg="red")
            error_output.config(text="Color's name should be different")
            return
    # generate the color chooser window
    # new_color will get a return value from colorchooser after user click confirm
    new_color = colorchooser.askcolor()
    # Cancel operation - while user click cancel in the color chooser window, it will exit the function
    if new_color[0] == None or new_color[1] == None:
        return
    # color addition success
    error_output.config(bg="light green")
    error_output.config(text="Success")
    # Update the list which stores colors name, colors RGB values, and colors hexadecimal values
    settings["settings"].append({"color_name": new_color_name,"color_RGB": new_color[0],"color_hex":new_color[1]})
    # Update the list for color name
    color_name_list.append(new_color_name)
    # Update the drop-down menu
    menu["value"] = color_name_list
    # Store new color's info into the json file
    with open("color_settings.json", "w") as file:
        json.dump(settings,file)
# double click to choose a color randomly to display
def color_loop(event_object):
    color_label.config(bg=settings["settings"][random.randint(0, len(settings["settings"]) - 1)]["color_hex"])
    # t1 = threading.Thread(target=color_loop,args=(None,))
    # t1.start()
    # # while True:
    # for i in settings['settings']:
    #     window.after(500, color_label.config(bg=i["color_hex"]))
    # t1.join()
# Delete exited color
def delete_color(event_object):
    # update error output
    error_output.forget()
    error_output.grid(row=5, column=2)
    # Delete the chosen color
    for i in settings["settings"]:
        if i["color_name"] == menu.get():
            # Delete success
            error_output.config(bg="light green")
            error_output.config(text="Success")
            # Remove from the list for colors name, colors RGB values, and colors hexadecimal values
            settings["settings"].remove(i)
            # Remove from the list for colors name
            color_name_list.remove(i["color_name"])
            # Update drop-down menu
            menu["value"] = color_name_list
            # Update info for the json file
            with open("color_settings.json", "w") as file:
                json.dump(settings, file)
# Variables
new_color_variable = tk.StringVar()
# color display labels
color_list_label = tk.Label(window, borderwidth=1, relief="solid",bg="light blue",text="Color List:" )
add_color_entry = tk.Entry(window,textvariable=new_color_variable, font=("Times New Roman", 16, "bold"))
add_color_button = tk.Button(window, text="Add Color", font=("Times New Roman", 16, "bold"),command=lambda :add_color(new_color_variable.get()))
color_name_label = tk.Label(window, borderwidth=1, relief="solid",bg="light blue",text="Name a custom color you want to add:",)
# Error output label
error_output = tk.Label(window,font=("Times New Roman", 16, "bold"),bg="light gray")  # set a combing output label
# Drop-down settings
menu = ttk.Combobox(window, values=color_name_list)
menu.bind("<<ComboboxSelected>>", color_selection)
# The text shows the color information
text_label = tk.Label(window,text="",bg="light gray")
# A Border for color display
color_label = tk.Label(window, borderwidth=2, relief="solid", height=4, width=20)
color_label.bind("<Double 1>",color_loop)
# Color delete by double click
color_delete_label = tk.Label(window, borderwidth=1, relief="solid" , height=2, width=30,text="Delete chosen color (Double Click)")
color_delete_label.bind("<Double 1>", delete_color)
# Grid
color_list_label.grid(row=0,column=0,sticky="e")
menu.grid(row=0,column=1,pady=20)
text_label.grid(row=1,column=1)
color_label.grid(row=2,column=1)
color_name_label.grid(row=3,column=0,padx=5)
add_color_entry.grid(row=3,column=1,pady=20)
add_color_button.grid(row=3,column=2,padx=5)
error_output.grid(row=4,column=2)
color_delete_label.grid(row=5,column=1)
# Mainloop to maintain the window running
window.mainloop()