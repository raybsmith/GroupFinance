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
        self.master = master
        # A frame to organize this window
        self.frame = Tk.Frame(self.master, padx=3, pady=12)
        self.frame.grid(column=0, row=0, sticky=("N,S,W,E"))
        self.frame.columnconfigure(0, weight=1)
        self.frame.rowconfigure(0, weight=1)
#        self.frame.pack()
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
#        self.file_label.pack()

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

    def save(self):
        if self.current_file_name == None:
            print "No file currently open."
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
            self.current_file_name = name
            f = open(name, "wb")
            pickle.dump(self.current_file, f)
            f.close()
#            f.write('The output\n')
#            f.close()
        return

    def load(self):
        name = tkFileDialog.askopenfilename()
        if name != '':
            self.current_file_name.set(name)
            f = open(name, "rb")
            self.current_file = pickle.load(f)
            f.close()
#            print lines
        return

    def create_new_group(self):
        print "TODO"
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
