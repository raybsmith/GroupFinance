import Tkinter as Tk
import tkFileDialog
import pickle

import group_obj

def main():
    # Set up a basic Tk interface.
    root = Tk.Tk()
    root.title("myTitle")
    root.option_add("*tearOff", False)
#    frame = Tk.Frame(root)#, borderwidth=2, relief="sunken")
#    frame.pack(side="left", padx=5, pady=5)
#    label = Tk.Label(root, text='I am frame')
#    label.pack()

    gui_main = main_interface(master=root)
    # Actually enter the event loop to run.
#    gui_main.mainloop()
    root.mainloop()
#    root.destroy()

class main_interface:
    def __init__(self, master):
        # Make the root frame "public".
        self.master = master
        # A frame to organize this window
        self.frame = Tk.Frame(self.master, padx=25, pady=25)
        self.frame.grid(column=0, row=0, sticky=("N,S,W,E"))
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
        # Keep track of the file that's currently being edited.
        self.current_file_name = Tk.StringVar()
        self.current_file_name.set("None")
        self.current_file = None
        self.file_label_pre = Tk.Label(self.frame,
                text="Current File:")
        self.file_label_pre.grid(row=1, column=1)
        self.file_label = Tk.Label(self.frame,
                textvariable = self.current_file_name)
        self.file_label.grid(row=1, column=2)
#        # Keep track of a list of transactions.
#        self.transactions = []

        # Creating a menu bar in the current top level window (root).
        self.menubar = Tk.Menu(self.master)
        # Set the master window (root) to use that menu as it's
        # menubar.
        self.master.config(menu=self.menubar)
        # Create File sub-menu
        self.menu_file = Tk.Menu(self.menubar)
        self.menubar.add_cascade(label="File",
                menu=self.menu_file)
        self.menu_file.add_command(label="New...",
                command=self.create_new_group)
        self.menu_file.add_command(label="Save As...",
                command=self.saveas)
        self.menu_file.add_command(label="Open...",
                command=self.load)
        self.menu_file.add_separator()
        self.menu_file.add_command(label="Quit",
                command=self.frame.quit)
        # Create a Help sub-menu
        self.menu_help = Tk.Menu(self.menubar)
        self.menubar.add_cascade(label="Help",
                menu=self.menu_help)
        self.menu_help.add_command(label="About...",
                command=self.callback)

        # Relevant buttons
        self.btn_show_people = Tk.Button(self.frame,
                text="Show Current People",
                command=self.show_current_list)
        self.btn_show_people.grid(row=2, column=1)
        self.btn_add_person = Tk.Button(self.frame,
                text="Add person",
                command=self.add_person)
        self.btn_add_person.grid(row=2, column=2)
        return

    def add_transaction(self):
        print "TODO"
        return
    def add_remove_person(self):
        print "TODO"
        return
    def save(self):
        if self.current_file_name == "None":
            alert = Tk.Toplevel(self.master)
            text = Tk.label(alert, text="No file currently open!")
            return
        name = self.current_file_name
        f = open(name, "wb")
        pickle.dump(self.current_file, f)
        f.close()
        return

    def saveas(self):
        name = tkFileDialog.asksaveasfilename(
                initialfile='group.p')
        if name != '':
            self.current_file_name.set(name)
            f = open(name, "wb")
            pickle.dump(self.current_file, f)
            f.close()
        return

    def load(self):
        name = tkFileDialog.askopenfilename()
        if name != '':
            self.current_file_name.set(name)
            f = open(name, "rb")
            self.current_file = pickle.load(f)
            f.close()
        return

    def create_new_group(self):
        # Open a new window for creation of the group.
        new_group_win = Tk.Toplevel(self.master)
        new_group_win.title("New Group")
        # Set up the overall frame for that window.
        new_gr_frame = Tk.Frame(new_group_win, padx=10, pady=10)
        new_gr_frame.grid(column=0, row=0, sticky=("N,S,W,E"))
        new_gr_frame.columnconfigure(0, weight=1)
        new_gr_frame.rowconfigure(0, weight=1)
        # Text explaining what to do
        explain_label = Tk.Label(new_gr_frame,
                text="Enter the names of the people in the " +\
                        "group one by one.\n To edit a name, " +\
                        "highlight the name in the list,\n " +\
                        "type the replacement in the text " +\
                        "field, then press 'Edit'.")
        explain_label.grid(row=1, column=1,
                rowspan=2, columnspan=2)
        # Text asking for a new person's name
        new_name_label = Tk.Label(new_gr_frame, text="Name?")
        new_name_label.grid(row=3, column=1)
        # Entry field for asking for name to add to list.
        new_name_current = Tk.StringVar()
        new_name_entry = Tk.Entry(new_gr_frame,
                textvariable=new_name_current)
        new_name_entry.grid(row=3, column=2)
        # Label to identify box of current names
        names_list_label = Tk.Label(new_gr_frame,
                text="Current list of names:", padx=10, pady=5)
        names_list_label.grid(row=2, column=4)
        # Listbox to display a list of current names
        listboxframe = Tk.Frame(new_gr_frame, padx=5, pady=5)
        listboxframe.grid(row=3, column=4,
                rowspan=10, columnspan=2)
        scrollbary = Tk.Scrollbar(listboxframe,
                orient="vertical")
        scrollbarx = Tk.Scrollbar(listboxframe,
                orient="horizontal")
        names_listbox = Tk.Listbox(listboxframe,
                yscrollcommand=scrollbary.set,
                xscrollcommand=scrollbary.set)
        scrollbary.config(command=names_listbox.yview)
        scrollbarx.config(command=names_listbox.xview)
        scrollbary.pack(side="right", fill="y")
        scrollbarx.pack(side="bottom", fill="x")
        names_listbox.pack(side="left", fill="both", expand=1)
        # Define a list of names we're going to add.
        new_name_list = []

        # Functions for buttons
        def new_name(*args):
            try:
                name = str(new_name_current.get())
                if name != '':
                    new_name_list.append(name)
                    new_name_current.set('')
                    names_listbox.insert("end", name)
#                    print new_name_list
            except(ValueError):
                pass
            return
        def edit_name(*args):
            try:
                # Get the index of the name to delete
                name_index = int(names_listbox.curselection()[0])
                # Edit it in the stored list
                edited_name = new_name_current.get()
                if edited_name != '':
                    new_name_list[name_index] = edited_name
                    # Delete the old from the stored list and replace
                    names_listbox.delete(name_index)
                    names_listbox.insert(name_index, edited_name)
#                    print new_name_list
            except(IndexError):
                pass
            return
        def delete_name(*args):
            try:
                # Get the index of the name to delete
                name_index = int(names_listbox.curselection()[0])
                # Delete it from the stored list
                new_name_list.pop(name_index)
                # Delete it from the displayed list
                names_listbox.delete(name_index)
                print new_name_list
            except(IndexError):
                pass
            return
        def create_group(*args):
            if new_name_list != []:
                self.current_file = \
                        group_obj.Group(new_name_list)
                self.saveas()
                new_group_win.destroy()
            return

        # Button to accept the entered name.
        add_name_btn = Tk.Button(new_gr_frame,
                text="Add name to list",
                command=new_name)
        add_name_btn.grid(row=4, column=2)
        # Button to edit an entered name.
        edit_name_btn = Tk.Button(new_gr_frame,
                text="Edit",
                command=edit_name)
        edit_name_btn.grid(row=13, column=4)
        # Button to delete an entered name.
        delete_name_btn = Tk.Button(new_gr_frame,
                text="Delete",
                command=delete_name)
        delete_name_btn.grid(row=13, column=5)
        # Button to finish it up and create the group.
        done_button = Tk.Button(new_gr_frame,
                text="Finish up and create the file!",
                command=create_group)
        done_button.grid(row=4, column=1, columnspan=1)

        # "Focus" the new name entry field so less clicking.
        new_name_entry.focus()
        # Bind "Return" to the new_name function
        new_name_entry.bind('<Return>', new_name)
        return

    def show_current_list(self):
        print "TODO"
        return
    def add_person(self):
        print "TODO"
        return
    def callback(self):
        print "called the callback"
        return

if __name__ == "__main__":
    main()
