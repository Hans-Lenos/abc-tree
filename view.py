import load
import tkinter as tk
from tkinter import ttk, filedialog

class View(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # Create a Treeview Frame
        self.tree_frame = tk.Frame(self)
        self.tree_frame.pack(pady=10)

        # create scroll widgets
        self.tree_scroll = ttk.Scrollbar( self.tree_frame )
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Create Treeview 
        self.tree = ttk.Treeview(self.tree_frame,
                                 yscrollcommand=self.tree_scroll.set,
                                 show='tree headings',
                                 height=20)
        self.tree.pack()
        self.tree_scroll.config(command=self.tree.yview)
        self.tree['columns'] = ("Supplier", "Description", "Cost")

        # Formate Columns
        self.tree.column("#0", width=320)
        self.tree.column("Supplier", width=200)
        self.tree.column("Description", anchor=tk.W, width=200)
        self.tree.column("Cost", anchor=tk.E, width=100)

        # Create Headings
        self.tree.heading("#0", text="Tittle", anchor=tk.W)
        self.tree.heading("Supplier", text="Supplier", anchor=tk.W)
        self.tree.heading("Description", text="Description", anchor=tk.W)
        self.tree.heading("Cost", text="Cost", anchor=tk.CENTER)

        # When clicked on tree, update text widgets. So link to click event
        self.tree.bind("<ButtonRelease-1>", self.select_clicked)

        # Create file on menu bar
        self.menu_bar = tk.Menu(parent)
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        self.file_menu.add_command(label="New", command=self.remove_all)
        self.file_menu.add_command(label="Open", command=self.open_clicked)
        self.file_menu.add_command(label="Save", command=self.save_clicked)
        self.file_menu.add_command(label="Save as...", command=self.save_as_clicked)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=parent.quit)

        # Create edit on menu bar
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        self.edit_menu.add_command(label="Cut", command=self.cut_clicked)
        self.edit_menu.add_command(label="Copy", command=self.copy_clicked)
        self.edit_menu.add_command(label="Paste", command=self.paste_clicked)

        # Create help on menu bar
        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)
        self.help_menu.add_command(label="Help Index", command=self.todo)
        self.help_menu.add_command(label="About...", command=self.todo)

        parent.config(menu=self.menu_bar)

        # Add Record Entry Boxes
        self.data_frame = tk.LabelFrame(self, text="Record")
        self.data_frame.pack(fill="x", expand=1, padx=20)

        self.name_label = tk.Label(self.data_frame, text="Tittle")
        self.name_label.grid(row=0, column=0, padx=10, pady=10)
        self.tittle_entry = tk.Entry(self.data_frame)
        self.tittle_entry.grid(row=0, column=1, padx=10, pady=10)

        self.supplier_label = tk.Label(self.data_frame, text="Supplier")
        self.supplier_label.grid(row=0, column=2, padx=10, pady=10)
        self.supplier_entry = tk.Entry(self.data_frame)
        self.supplier_entry.grid(row=0, column=3, padx=10, pady=10)

        self.description_label = tk.Label(self.data_frame, text="Description")
        self.description_label.grid(row=0, column=4, padx=10, pady=10)
        self.description_entry = tk.Entry(self.data_frame)
        self.description_entry.grid(row=0, column=5, padx=10, pady=10)

        self.cost_label = tk.Label(self.data_frame, text="Cost")
        self.cost_label.grid(row=1, column=2, padx=10, pady=10)
        self.cost_entry = tk.Entry(self.data_frame)
        self.cost_entry.grid(row=1, column=3, padx=10, pady=10)

        # Add Buttons
        self.button_frame =tk.LabelFrame(self, text="Commands")
        self.button_frame.pack(fill="x", expand=1, padx=20)

        self.update_button = tk.Button(self.button_frame, text="Update", command=self.update_clicked, width=11)
        self.update_button.grid(row=0, column=1, padx=10, pady=10)

        self.add_button = tk.Button(self.button_frame, text="Add", command=self.add_clicked, width=11)
        self.add_button.grid(row=0, column=2, padx=10, pady=10)

        self.remove_one_button = tk.Button(self.button_frame, text="Remove", command=self.remove, width=11)
        self.remove_one_button.grid(row=0, column=3, padx=10, pady=10)

        self.move_up_button = tk.Button(self.button_frame, text="Move Up", command=self.up, width=11)
        self.move_up_button.grid(row=0, column=4, padx=10, pady=10)

        self.move_down_button = tk.Button(self.button_frame, text="Move Down", command=self.down, width=11)
        self.move_down_button.grid(row=0, column=5, padx=10, pady=10)

        self.move_left_button = tk.Button(self.button_frame, text="<<<", command=self.left, width=11)
        self.move_left_button.grid(row=0, column=6, padx=10, pady=10)

        self.move_right_button = tk.Button(self.button_frame, text=">>>", command=self.right, width=11)
        self.move_right_button.grid(row=0, column=7, padx=10, pady=10)

        self.message_label = tk.Label(self.button_frame, text="Application started!")
        self.message_label.grid(row=1, column=0, columnspan=8, padx=10, pady=10)

        # variables for copy/cut/paste
        self.paste_node = None
        self.copy = False
        self.cut = False

        # remember file name
        self.file_name = None

    def todo(self):
        self.filewin = tk.Toplevel(self)
        button = tk.Button(self.filewin, text="Todo, still need to program this")
        button.pack()
    
    def save_as_clicked(self):
        """
        Handle button click event
        :return:
        """
        self.file_name = filedialog.asksaveasfilename(title="Save Tree File",
                                                      filetypes=(("Tree File", "*.csv"), ("All", "*.*")))
        self.save_clicked()

    def save_clicked(self):
        """
        Handle button click event
        :return:
        """
        data = self.get_all_data()
        load.save(data, self.file_name)
        
    def open_clicked(self):
        """
        Handle button click event
        :return:
        """
        self.remove_all()
        self.file_name = filedialog.askopenfilename(title="Open Tree File",
                                                    filetypes=(("Tree File", "*.csv"), ("All", "*.*")))
        data = load.load(self.file_name)
        self.show_tree(data)
    
    def cut_clicked(self):
        pass

    def copy_clicked(self):
        self.paste_node = self.tree.focus()
        self.copy = True

    def paste_clicked(self):
        if self.copy or self.cut:
            selected = self.tree.focus()
            self.paste(selected)
        self.copy = False
        if self.cut:
            # delete selected node
            self.cut = False

    def paste(self, node):
        paste_text = self.tree.item(self.paste_node, 'text')
        paste_value = self.tree.item(self.paste_node, 'values')
        new_parent = self.tree.insert(parent=self.tree.parent(node),
                                      index=self.tree.index(node) + 1,
                                      text=paste_text,
                                      values=paste_value)
        self.copy_all_children(new_parent, self.paste_node)

    def copy_all_children(self, parent, copy_node):
        children = self.tree.get_children(copy_node)
        for child in children:
            paste_text = self.tree.item(child, 'text')
            paste_value = self.tree.item(child, 'values')
            new_parent = self.tree.insert(parent=parent,
                                          index='end',
                                          text=paste_text,
                                          values=paste_value)
            self.copy_all_children(new_parent, child)

    def calculate_cost(self, item):
        """"
        recursive calculation of the cost of a value
        parameters:
        item, the parent node to use to calculate the cost for
        """
        children = self.tree.get_children(item)
        total_cost = 0
        if children:
            # if children have children
            for child in children:
                cost = self.calculate_cost(child)
                total_cost += cost
            if item:    # starts with the root, so the highest level is no item and root can't have values
                parent_values = list(self.tree.item(item, 'values'))
                parent_text = self.tree.item(item, 'text')
                self.tree.item(item,
                               text=parent_text,
                               values=(parent_values[0],
                                       parent_values[1],
                                       f"{total_cost:.2f}"))
        else:
            child_values = self.tree.item(item, 'values')
            if child_values[2]:
                total_cost = float(child_values[2])
        return total_cost

    def get_selected_data(self):
        data = []
        selected = self.tree.focus()
        selected_parent = self.tree.parent(selected)
        selected_text = self.tree.item(selected, 'text')
        selected_value = self.tree.item(selected, 'values')
        data.append([selected_parent, selected, selected_text, selected_value[0], selected_value[1], selected_value[2],
                     selected_value[3]])
        items = self.get_all_children(item = selected)
        for this_item in items:
            item_parent = self.tree.parent(this_item)
            item_text = self.tree.item(this_item, 'text')
            item_value = self.tree.item(this_item, 'values')
            data.append([item_parent, this_item, item_text, item_value[0], item_value[1], item_value[2], item_value[3]])
        return data

    def get_all_data(self):
        data = []
        items = self.get_all_children(item ="")
        for this_item in items:
            item_parent = self.tree.parent(this_item)
            item_text = self.tree.item(this_item, 'text')
            item_value = self.tree.item(this_item, 'values')
            data.append([item_parent,
                         this_item,
                         item_text,         # tittle
                         item_value[0],     # supplier
                         item_value[1],     # description
                         item_value[2]])    # cost
        return data

    def get_all_children(self, item):
        children = self.tree.get_children(item)
        for child in children:
            children += self.get_all_children(child)
        return children

    def show_tree(self, data):
        for line in data:
            self.tree.insert(parent=line[0].strip(), index='end', iid=line[1].strip(), text=line[2].strip(), 
                             values=(line[3].strip(),   # supplier
                                     line[4].strip(),   # description
                                     line[5].strip()),  # cost
                             open=False)

    def show_error(self, message):
        self.message_label['text'] = message
        self.message_label['foreground'] = 'red'
        self.message_label.after(3000, self.hide_message)

    def show_success(self, message):
        """
        Show a success message
        :param message:
        :return:
        """
        self.message_label['text'] = message
        self.message_label['foreground'] = 'green'
        self.message_label.after(3000, self.hide_message)

    def hide_message(self):
        """
        Hide the message
        :return:
        """
        self.message_label['text'] = ''            

    def select_clicked(self, e):
        """
        Handle button click event
        :return:
        """
        self.tittle_entry.delete(0, tk.END)
        self.description_entry.delete(0, tk.END)
        self.supplier_entry.delete(0, tk.END)
        self.cost_entry.delete(0, tk.END)

        selected = self.tree.focus()
        selected_text = self.tree.item(selected, 'text')
        selected_value = self.tree.item(selected, 'values')

        self.tittle_entry.insert(0, selected_text)
        self.supplier_entry.insert(0, selected_value[0])
        self.description_entry.insert(0, selected_value[1])
        self.cost_entry.insert(0, selected_value[2])

    def update_clicked(self):
        """
        Handle button click event
        :return:
        """
        selected = self.tree.focus()
        cost = float(self.cost_entry.get() if self.cost_entry.get() else 0)
        self.tree.item(selected,
                       text=self.tittle_entry.get(),
                       values=(self.supplier_entry.get(),
                               self.description_entry.get(),
                               f"{cost:.2f}"),
                       open=False)
        self.calculate_cost("")
        
    def add_clicked(self):
        """
        Handle button click event
        :return:
        """
        selected = self.tree.focus()
        actual = float(self.cost_entry.get() if self.cost_entry.get() else 0)
        if selected != "":
            self.tree.insert(parent=self.tree.parent(selected), index=self.tree.index(selected)+1,
                             text=self.tittle_entry.get(), values=(self.supplier_entry.get(),
                                                                   self.description_entry.get(), f"{actual:.2f}"))
        else:
            self.tree.insert(parent="", index='end', text=self.tittle_entry.get(),
                             values=(self.supplier_entry.get(), self.description_entry.get(),
                                     f"{actual:.2f}"))
        self.calculate_cost("")

    def right(self):
        selected = self.tree.selection()
        self.tree.move(selected,self.tree.prev(selected),0)
        self.calculate_cost("")

    def left(self):
        selected = self.tree.selection()
        parent = self.tree.parent(selected)
        index = self.tree.index(parent) + 1
        self.tree.move(selected,self.tree.parent(parent), index)
        self.calculate_cost("")

    def up(self):
        rows = self.tree.selection()
        for row in rows:
            self.tree.move(row, self.tree.parent(row), self.tree.index(row)-1)

    def down(self):
        rows = self.tree.selection()
        for row in reversed(rows):
            self.tree.move(row, self.tree.parent(row), self.tree.index(row)+1)

    def remove(self):
        rows = self.tree.selection()
        for row in rows:
            self.tree.delete(row)
        self.calculate_cost("")

    def remove_all(self):
        for row in self.tree.get_children():
            self.tree.delete(row)