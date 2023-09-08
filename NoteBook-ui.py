# Add the desired library.
import json5
import tkinter as tk
from tkinter import font
from tkinter import messagebox
from datetime import datetime   


# This class maintains a series of required values.
class Note:
    def __init__(self):
        self.Demo_ID = -1
        self.Title = None
        self.Comment = None
        self.Demo = {"Users":[]}

"""
Using the previous class, 
this class performs the main tasks such as creating a json file and generating an ID, 
getting the Title and comma, and saving information in the json file.
"""
class Repository:
    def __init__(self):
        self.Note = Note()
        # The location of the address of the json file.
        self.Json_File = "NoteBook.json"
        self.Json_Data = None
        self.Json_Dict = None
        self.Json_Remove = None
        self.Json_Remove_Index = None

    # Creating the Create function to Create a value in json.
    def Create(self):
        with open(self.Json_File, mode = "w") as Data:
            json5.dump(self.Note.Demo, Data)

    """
    Get_Title_And_Comment function to get the ID Created in 
    the previous function and the Title and Comment from the user.
    """
    def Get_Title_And_Comment(self, Title, Comment):
        self.Note.Demo_ID += 1
        self.Json_Dict = {
            "ID" : self.Note.Demo_ID,
            "Title" : Title,
            "Comment" : Comment,
            "Registration_Time" :  datetime.today().ctime()
        }

        # Save function to Save the values ​​we got in the json file.
        def Save():
            with open(self.Json_File, mode = "r") as Data:
                self.Json_Data = json5.load(Data)
            self.Json_Data["Users"].append(self.Json_Dict)
            with open(self.Json_File, mode = "w") as Data:
                json5.dump(self.Json_Data, Data, indent = 4)
        return Save()

    # Remove_Item function to delete values ​​or all items or delete with ID
    def Remove_Item(self, With_ID):
        self.Del_Item = None
        self.Del_Item_With_ID = None

        with open(self.Json_File, mode = "r") as Data:
            self.Json_Remove = json5.load(Data)
            self.Del_Item = self.Json_Remove

        # If it was without ID
        if With_ID == None:
            with open(self.Json_File, mode = "w") as Data:
                json5.dump(self.Note.Demo, Data, indent = 4)
            return self.Del_Item

        # If it was with Idi
        elif With_ID != None:
            List_Of_ID = []
            try:
                for everything in self.Json_Remove["Users"]:
                    List_Of_ID.append(everything["ID"])
                if With_ID not in List_Of_ID:
                    raise

                for everything in self.Json_Remove["Users"]:
                    if everything["ID"] == With_ID:
                        self.Json_Remove_Index = self.Json_Remove["Users"].index(everything)
                        self.Del_Item_With_ID = self.Json_Remove["Users"].pop(self.Json_Remove_Index)
                        with open(self.Json_File, mode = "w") as Data:
                            json5.dump(self.Json_Remove, Data, indent = 4)
            except:
                str_err = "This ID does not exist!"
                return str_err
            else:
                return self.Del_Item_With_ID

"""
This class is for displaying two modes of Data.
First mode: display all Data stored in json.
The second mode: displaying json Data based on the received ID.
"""
class View:
    def __init__(self):
        self.Method = Repository()
        self.Input_Id = None 

    # This function Shows the items in two modes, one without ID, which includes all items, and the other with ID.
    def Show_All(self, With_ID):
        with open(self.Method.Json_File, mode = "r") as Data:
            Show = json5.load(Data)
            
        # This function Shows all the items in the json file.
        if With_ID == None:
            return Show
        
        # This function is to Show the item based on ID.
        elif With_ID != None:
            try:
                List_Of_ID_V = []
                for everything in Show["Users"]:
                    List_Of_ID_V.append(everything["ID"])
                    if everything["ID"] == int(With_ID):
                        Result_Input = everything
                if With_ID not in List_Of_ID_V:
                    raise
            except:
                str_err = "Your entry is either incorrect or there is no such ID!"
                return str_err
            else:
                return Result_Input

# NoteBook class is for creating and launching functions of previous classes.
class NoteBook:
    def __init__(self):
        self.Repo = Repository()
        self.View = View()
        self.Repo.Create()

    # This function causes the Get_Title_And_Comment function to be executed.
    def Enter_Item(self, Title, Comment):
        self.Repo.Get_Title_And_Comment(Title, Comment)

    # This function causes a function to display all items in json.
    def Give_Item(self, With_ID = None):
        """By giving a numerical value to With_ID, calculations can be checked based on that ID"""
        return self.View.Show_All(With_ID)

    # This function executes the Remove_Item function.
    def Removing_Item(self, With_ID = None):
        """By giving a numerical value to With_ID, calculations can be checked based on that ID"""
        return self.Repo.Remove_Item(With_ID)
"""backend is finished"""
NoteBook = NoteBook()

# Window construction.
root = tk.Tk()
root.title("NoteBook")

# Function to return to the main window
def back_to_menu():
    for widget in root.winfo_children():
        widget.destroy()
    Meno()

# Send button
def submit_clicked():
    global title, comment

    title = entry_title.get()
    comment = entry_comment.get()
    messagebox.showinfo("    Data Of User    ", f"Title:           {title}\nComment:  {comment}")
    NoteBook.Enter_Item(Title = title, Comment = comment)
    button1_clicked()

# First key design
def button1_clicked():
    global entry_title, entry_comment

    for widget in root.winfo_children():
        widget.destroy()

    button_font = font.Font(family = "Calibri", size = 12)
    label_text = tk.Label(root, text = "Enter your value", font=button_font)
    label_title = tk.Label(root, text = "Title:")
    entry_title = tk.Entry(root, width=50)
    label_comment = tk.Label(root, text="Comment:")
    entry_comment = tk.Entry(root, width=50)
    button_submit = tk.Button(root, text="  Send  ", bg="#ff8080", fg="black", font=button_font)
    button_menu = tk.Button(root, text="  Back  ", bg="#80ff80", fg="black", font=button_font)

    label_text.pack(padx=0, pady=0)
    label_title.pack()
    entry_title.pack()
    label_comment.pack()
    entry_comment.pack()
    button_submit.pack()
    button_menu.pack(side=tk.RIGHT, padx=30, pady=10)

# Data display function
def Show_Item():
    global Search_ID
    Search_ID = id_entry.get()
    if Search_ID == '':
        Show_All = NoteBook.Give_Item(With_ID = None)
        text_box.delete(1.0, tk.END)  
        text_box.insert(tk.END, Show_All)
    else:
        Show_All = NoteBook.Give_Item(With_ID = int(Search_ID))
        text_box.delete(1.0, tk.END)  
        text_box.insert(tk.END, Show_All)

# Second button
def button2_clicked():
    global text_box, id_entry
    for widget in root.winfo_children():
        widget.destroy()

    top_frame = tk.Frame(root)
    top_frame.pack()
    show_label = tk.Label(top_frame, text="Show Item", font=("Calibri", 12))
    show_label.pack()
    
    bottom_frame = tk.Frame(root)
    bottom_frame.pack()
    id_label = tk.Label(bottom_frame, text="Search with ID:   ")
    id_label.pack(side=tk.LEFT)
    id_entry = tk.Entry(bottom_frame, width=10)
    id_entry.pack(side=tk.LEFT)
    button_submit = tk.Button(bottom_frame, text="Search", bg="#ff8080", fg="black", command = Show_Item)
    button_submit.pack(side=tk.LEFT, padx=30, pady=10)
    button_menu = tk.Button(bottom_frame, text="  Back  ", bg="#80ff80", fg="black", font=("Calibri", 10), command=back_to_menu)
    button_menu.pack(side=tk.RIGHT)
    
    extra_bottom_frame = tk.Frame(root)
    extra_bottom_frame.pack()
    scrollbar = tk.Scrollbar(extra_bottom_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_box = tk.Text(extra_bottom_frame, yscrollcommand=scrollbar.set)
    text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=text_box.yview)

# Creating a function to delete data
def Delete_Item():
    global Search_ID
    Delete_ID = id_entry1.get()
    if Delete_ID == '':
        Deleted = NoteBook.Removing_Item(With_ID = None)
        text_box.delete(1.0, tk.END)  
        text_box.insert(tk.END, Deleted)
    else:
        Deleted = NoteBook.Removing_Item(With_ID = int(Delete_ID))
        text_box.delete(1.0, tk.END)  
        text_box.insert(tk.END, Deleted)  

# The third button
def button3_clicked():
    global text_box, id_entry1
    for widget in root.winfo_children():
        widget.destroy()

    top_frame = tk.Frame(root)
    top_frame.pack()
    show_label = tk.Label(top_frame, text="Delete Item", font=("Calibri", 12))
    show_label.pack()
    
    bottom_frame = tk.Frame(root)
    bottom_frame.pack()
    id_label = tk.Label(bottom_frame, text="Delete with ID:   ")
    id_label.pack(side=tk.LEFT)
    id_entry1 = tk.Entry(bottom_frame, width=10)
    id_entry1.pack(side=tk.LEFT)
    button_submit = tk.Button(bottom_frame, text="Delete", bg="#ff8080", fg="black")
    button_submit.pack(side=tk.LEFT, padx=30, pady=10)
    button_menu = tk.Button(bottom_frame, text="  Back  ", bg="#80ff80", fg="black", font=("Calibri", 10), command=back_to_menu)
    button_menu.pack(side=tk.RIGHT)
    
    extra_bottom_frame = tk.Frame(root)
    extra_bottom_frame.pack()
    scrollbar = tk.Scrollbar(extra_bottom_frame)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    text_box = tk.Text(extra_bottom_frame, yscrollcommand=scrollbar.set)
    text_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.config(command=text_box.yview)

# Home buttons
def Meno():
    button_font = font.Font(family="Arial", size=14)
    button1 = tk.Button(root, text="Enter Item", bg="#ff8080", fg="black", font=button_font, command=button1_clicked)
    button2 = tk.Button(root, text="Show Item", bg="#80ff80", fg="black", font=button_font, command=button2_clicked)
    button3 = tk.Button(root, text="Delete Item", bg="#8080ff", fg="black", font=button_font)

    button1.pack(fill = tk.BOTH, expand=True)
    button2.pack(fill = tk.BOTH, expand=True)
    button3.pack(fill = tk.BOTH, expand=True)

Meno()
# Adjust window size.
window_width = 455
window_height = 200
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = int((screen_width / 2) - (window_width / 2))
y = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# The mainloop of the window
root.mainloop()
