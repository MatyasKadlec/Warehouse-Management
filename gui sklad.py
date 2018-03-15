# !/usr/bin/python3
from tkinter import *
from sklad import *
from tkinter import messagebox
from tkinter import font


class GUI:
    def __init__(self):
        mainWindow.title("Warehouse GUI v. 1.1")
        mainWindow.geometry("640x480-600-300")
        mainWindow['padx'] = 8

        self.value = ""
        self.store_unit = ""
        self.position = ""
        self.scrollbarX = ""
        self.scrollbar = ""
        self.scrollbarY = ""
        self.screenWidth = mainWindow.winfo_screenwidth()
        self.my_font = font.Font(family="Monaco", size=10)
        self.label_font = ("Times New Roman", 12, "bold")
        mainWindow.columnconfigure(0, weight=1)
        mainWindow.rowconfigure(0, weight=1)
        mainWindow.rowconfigure(1, weight=1)
        mainWindow.rowconfigure(2, weight=1)
        mainWindow.rowconfigure(3, weight=1)
        mainWindow.rowconfigure(4, weight=1)
        mainWindow.rowconfigure(5, weight=1)
        mainWindow.rowconfigure(6, weight=1)
        mainWindow.rowconfigure(7, weight=1)
        mainWindow.rowconfigure(8, weight=1)

# frames
        self.ware_inFrame = Frame(mainWindow)
        self.ware_toFrame = Frame(mainWindow)
        self.ware_outFrame = Frame(mainWindow)
        self.buttonFrame = Frame(mainWindow)
        self.store_unitFrame = Frame(mainWindow)
        self.resultFrame = Frame(mainWindow)
        self.wTresultFrame = Frame(mainWindow)
        self.scrollFrame = Frame(mainWindow)
        self.positionFrame = Frame(mainWindow)
        self.search_articleFrame = Frame(mainWindow)
        self.radioFrame = Frame(mainWindow)
        self.radioFrameH = Frame(mainWindow)
        self.textFrame = Frame(mainWindow)

        self.content = StringVar()
        self.content2 = IntVar()
        self.content3 = StringVar()
        self.content4 = IntVar()
        self.content5 = IntVar()
        menubar = Menu(mainWindow)
        mainWindow.config(menu=menubar)

        filemenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.add_command(label="Close", command=self.remove_screen)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=mainWindow.quit)

        action_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Action", menu=action_menu)
        action_menu.add_command(label="Ware In", command=self.ware_in_widgets)
        action_menu.add_command(label="Ware To", command=self.ware_to_widgets)
        action_menu.add_command(label="Ware Out", command=self.ware_out_widgets)

        search_menu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Search", menu=search_menu)
        search_menu.add_command(label="Search Article", command=self.search_article_widgets)
        search_menu.add_command(label="Search Store Unit", command=self.search_store_unit_widgets)
        search_menu.add_command(label="Search Position", command=self.search_position_widgets)
        search_menu.add_command(label="Display all", command=self.view_table_widgets)

        helpmenu = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=helpmenu)
        helpmenu.add_command(label="Help function", command=self.help_me)
        helpmenu.add_command(label="About...", command=self.about)

    def call_ware_in(self):
        try:
            self.value = ""
            ar = self.content.get()
            am = self.content2.get()
            value = zbozi.ware_in(ar, am)
            self.ware_in_widgets()
            if value:
                messagebox.showinfo("info", value)
            if zbozi.Ware_in_error:
                messagebox.showerror("Error", zbozi.Ware_in_error)
            if zbozi.Positions_error:
                messagebox.showerror("Error", zbozi.Positions_error)
            return value
        except TclError:
            messagebox.showerror("Error", "Wrong parameter entered (both article and amount must be entered)\n"
                                          "Article must be a string in format one capital letter followed by six "
                                          "numbers. Amount must be an positive integer")

    def call_ware_to(self):
        try:
            self.value = ""
            ar = self.content.get()
            am = self.content2.get()
            su = self.content4.get()
            value = zbozi.ware_to(ar, am, su)
            self.ware_to_widgets()
            if value:
                for item in value:
                    self.w_t_result.insert(END, item)
            if zbozi.Ware_to_error:
                messagebox.showerror("Error", zbozi.Ware_to_error)
        except TclError:
            messagebox.showerror("Error",  "Wrong parameter entered (article, amount and store unit must be entered)\n"
                                           "Article must be a string in format one capital letter followed by six "
                                           "numbers. Amount must be an positive integer\n"
                                           "Store unit must be a positive six character number, existing in database")

    def call_ware_out(self):
        try:
            self.value = ""
            ar = self.content.get()
            am = self.content2.get()
            value = zbozi.ware_out(ar, am)
            self.ware_out_widgets()
            if value:
                for item in value:
                    self.result.insert(END, item)
            if zbozi.Ware_out_error:
                messagebox.showerror("Error", zbozi.Ware_out_error)
        except TclError:
            messagebox.showerror("Error", "Wrong parameter entered (both article and amount must be entered)\n"
                                          "Article must be a string in format one capital letter followed by six "
                                          "numbers. Amount must be an positive integer")

    def call_search_article(self):

        try:
            self.value = ""
            ar = self.content.get()
            value = zbozi.find_article(ar)
            self.search_article_widgets()
            if value:
                for item in value:
                    self.result.insert(END, item)
            if zbozi.find_article_error:
                messagebox.showerror("Error", zbozi.find_article_error)
        except TclError:
            messagebox.showerror("Error", "Wrong parameter entered article must be entered"
                                          "Article must be a string in format one letter followed by six numbers")

    def call_search_store_unit(self):
        try:
            self.value = ""
            self.store_unit = self.content2.get()
            value = zbozi.find_store_unit(self.store_unit)
            if value:
                for item in value:
                    self.result.insert(END, item)
            if zbozi.find_store_unit_error:
                messagebox.showerror("Error", zbozi.find_store_unit_error)
        except TclError:
            messagebox.showerror("Error", "Wrong parameter entered (Store unit field must be entered)\n"
                                          "Store unit must be a positive six character number, existing in database")

    def call_search_position(self):
        try:
            self.value = ""
            self.position = self.content.get()
            value = zbozi.find_position(self.position)
            if value:
                for item in value:
                    self.result.insert(END, item)

            if zbozi.find_position_error:
                messagebox.showerror("Error", zbozi.find_position_error)
        except TclError:
            messagebox.showerror("Error", "Wrong parameter entered (position field must be entered)\n"
                                          "Position must be a string with length more than 4 characters but less than"
                                          "9 characters")

    def call_view_table(self, ):
        zbozi.view_table()
        v = self.content2.get()
        self.view_table_widgets()
        if v == 1:
            for item in zbozi.ar_view_table_list:
                self.result.insert(END, item)
        elif v == 2:
            for item in zbozi.am_view_table_list:
                self.result.insert(END, item)
        elif v == 3:
            for item in zbozi.su_view_table_list:
                self.result.insert(END, item)
        elif v == 4:
            for item in zbozi.po_view_table_list:
                self.result.insert(END, item)
        elif v == 5:
            for item in zbozi.da_view_table_list:
                self.result.insert(END, item)

    def call_help(self):
        v = self.content5.get()
        self.help_me()
        if v == 1:
            self.result.insert(END, zbozi.ware_in.__doc__)
        elif v == 2:
            self.result.insert(END, zbozi.ware_to.__doc__)
        elif v == 3:
            self.result.insert(END, zbozi.ware_out.__doc__)
        elif v == 4:
            self.result.insert(END, zbozi.find_article.__doc__)
        elif v == 5:
            self.result.insert(END, zbozi.find_store_unit.__doc__)
        elif v == 6:
            self.result.insert(END, zbozi.find_position.__doc__)
        elif v == 7:
            self.result.insert(END, zbozi.view_table.__doc__)

    @staticmethod
    def about():
        messagebox.showinfo("info", "Created by Matyas Kadlec, 2018, version 1.3")

    def remove_screen(self):
        self.ware_inFrame.grid_forget()
        self.ware_toFrame.grid_forget()
        self.ware_outFrame.grid_forget()
        self.buttonFrame.grid_forget()
        self.buttonFrame.grid_forget()
        self.store_unitFrame.grid_forget()
        self.resultFrame.grid_forget()
        self.scrollFrame.grid_forget()
        self.positionFrame.grid_forget()
        self.search_articleFrame.grid_forget()
        self.radioFrame.grid_forget()
        self.radioFrameH.grid_forget()
        self.wTresultFrame.grid_forget()

    def ware_in_widgets(self):
        self.remove_screen()
        self.ware_inFrame.grid(row=0, column=0, sticky="w", columnspan=2)
        ware_in_label = Label(self.ware_inFrame, text="WARE IN")
        ware_in_label.configure(font=self.label_font)
        ware_in_label.grid(row=0, column=0, padx=250, sticky="we", columnspan=2)
        article_label = Label(self.ware_inFrame, text="Article")
        article_label.grid(row=1, column=0, sticky="w")
        entry_article = Entry(self.ware_inFrame, textvariable=self.content)
        entry_article.grid(row=2, column=0, sticky="w")
        entry_article.delete(0, END)

        amount_label = Label(self.ware_inFrame, text="Amount")
        amount_label.grid(row=3, column=0, sticky="w")
        entry_amount = Entry(self.ware_inFrame, textvariable=self.content2)
        entry_amount.grid(row=4, column=0, sticky="w")
        entry_amount.delete(0, END)

        self.buttonFrame.grid(row=1, column=0, sticky="nsew")
        ok_button = Button(self.buttonFrame, text="OK", command=self.call_ware_in)
        ok_button.grid(row=0, column=0, sticky="w")

    def ware_to_widgets(self):
        self.remove_screen()
        self.ware_toFrame.grid(row=0, column=0, sticky="w")
        self.ware_toFrame.columnconfigure(0, weight=1)
        self.ware_toFrame.rowconfigure(0, weight=1)

        ware_to_label = Label(self.ware_toFrame, text="WARE TO")
        ware_to_label.configure(font=self.label_font)
        ware_to_label.grid(row=0, column=0, padx=250, sticky="we", columnspan=2)

        article_label = Label(self.ware_toFrame, text="Article")
        article_label.grid(row=1, column=0, sticky="w")
        entry_article = Entry(self.ware_toFrame, textvariable=self.content)
        entry_article.grid(row=2, column=0, sticky="w")
        entry_article.delete(0, END)

        amount_label = Label(self.ware_toFrame, text="Amount")
        amount_label.grid(row=3, column=0, sticky="w")
        entry_amount = Entry(self.ware_toFrame, textvariable=self.content2)
        entry_amount.grid(row=4, column=0, sticky="w")
        entry_amount.delete(0, END)

        store_unit_label = Label(self.ware_toFrame, text="Store unit")
        store_unit_label.grid(row=5, column=0, sticky="w")
        entry_store_unit = Entry(self.ware_toFrame, textvariable=self.content4)
        entry_store_unit.grid(row=6, column=0, sticky="w")
        entry_store_unit.delete(0, END)

        self.buttonFrame.grid(row=1, column=0, sticky="w")
        ok_button = Button(self.buttonFrame, text="OK", command=self.call_ware_to)
        ok_button.grid(row=0, column=0, sticky="w")

        self.wTresultFrame.grid(row=2, column=0, sticky="nsew")
        self.wTresultFrame.columnconfigure(0, weight=1)
        self.wTresultFrame.rowconfigure(0, weight=1)
        self.w_t_result = Listbox(self.wTresultFrame)
        self.w_t_result.grid(row=0, column=0, sticky="nsew")

        self.scrollFrame.columnconfigure(0, weight=1)
        self.scrollFrame.rowconfigure(0, weight=1)
        self.scrollFrame.grid(row=2, column=1, sticky="nsew")
        self.scrollbar = Scrollbar(self.scrollFrame)
        self.scrollbar.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.config(command=self.w_t_result.yview)

        self.scrollbarX = Scrollbar(self.resultFrame)
        self.scrollbarX.grid(row=1, column=0, sticky="nsew")
        self.scrollbarX.config(orient=HORIZONTAL, command=self.w_t_result.xview)
        self.textFrame.columnconfigure(0, weight=1)
        self.textFrame.rowconfigure(0, weight=1)

    def ware_out_widgets(self):
        self.remove_screen()
        self.ware_outFrame.grid(row=0, column=0, sticky="w")

        ware_out_label = Label(self.ware_outFrame, text="WARE OUT")
        ware_out_label.configure(font=self.label_font)
        ware_out_label.grid(row=0, column=0, padx=250, sticky="we", columnspan=2)

        article_label = Label(self.ware_outFrame, text="Article")
        article_label.grid(row=1, column=0, sticky="w")
        entry_article = Entry(self.ware_outFrame, textvariable=self.content)
        entry_article.grid(row=2, column=0, sticky="w")
        entry_article.delete(0, END)

        amount_label = Label(self.ware_outFrame, text="Amount")
        amount_label.grid(row=3, column=0, sticky="w")
        entry_amount = Entry(self.ware_outFrame, textvariable=self.content2)
        entry_amount.grid(row=4, column=0, sticky="w")
        entry_amount.delete(0, END)

        self.buttonFrame.grid(row=1, column=0, sticky="w")
        ok_button = Button(self.buttonFrame, text="OK", command=self.call_ware_out)
        ok_button.grid(row=0, column=0, sticky="w")

        self.resultFrame.grid(row=2, column=0, sticky="nsew")
        self.resultFrame.columnconfigure(0, weight=1)
        self.resultFrame.rowconfigure(0, weight=1)
        self.result = Listbox(self.resultFrame)
        self.result.grid(row=0, column=0, sticky="nsew")

        self.scrollFrame.columnconfigure(0, weight=1)
        self.scrollFrame.rowconfigure(0, weight=1)
        self.scrollFrame.grid(row=2, column=1, sticky="nsew")
        self.scrollbar = Scrollbar(self.scrollFrame)
        self.scrollbar.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.config(command=self.result.yview)

        self.scrollbarX = Scrollbar(self.resultFrame)
        self.scrollbarX.grid(row=1, column=0, sticky="nsew")
        self.scrollbarX.config(orient=HORIZONTAL, command=self.result.xview)
        self.textFrame.columnconfigure(0, weight=1)
        self.textFrame.rowconfigure(0, weight=1)

    def search_article_widgets(self):
        self.remove_screen()
        self.search_articleFrame.grid(row=0, column=0, sticky="w")

        search_article_label = Label(self.search_articleFrame, text="SEARCH ARTICLE")
        search_article_label.configure(font=self.label_font)
        search_article_label.grid(row=0, column=0, padx=250, sticky="we", columnspan=2)

        article_label = Label(self.search_articleFrame, text="Article")
        article_label.grid(row=1, column=0, sticky="w")
        entry_article = Entry(self.search_articleFrame, textvariable=self.content)
        entry_article.grid(row=2, column=0, sticky="w")
        entry_article.delete(0, END)

        self.buttonFrame.grid(row=1, column=0, sticky="w")
        ok_button = Button(self.buttonFrame, text="OK", command=self.call_search_article)
        ok_button.grid(row=0, column=0, sticky="w")

        self.resultFrame.grid(row=2, column=0, sticky="nsew")
        self.resultFrame.columnconfigure(0, weight=1)
        self.resultFrame.rowconfigure(0, weight=1)
        self.result = Listbox(self.resultFrame)
        self.result.grid(row=0, column=0, sticky="nsew")

        self.scrollFrame.columnconfigure(0, weight=1)
        self.scrollFrame.rowconfigure(0, weight=1)
        self.scrollFrame.grid(row=2, column=1, sticky="nsew")
        self.scrollbar = Scrollbar(self.scrollFrame)
        self.scrollbar.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.config(command=self.result.yview)

        self.scrollbarX = Scrollbar(self.resultFrame)
        self.scrollbarX.grid(row=1, column=0, sticky="nsew")
        self.scrollbarX.config(orient=HORIZONTAL, command=self.result.xview)
        self.textFrame.columnconfigure(0, weight=1)
        self.textFrame.rowconfigure(0, weight=1)

    def search_store_unit_widgets(self):
        self.remove_screen()
        self.store_unitFrame.grid(row=0, column=0, sticky="nw")
        self.store_unitFrame.columnconfigure(0, weight=0)
        self.store_unitFrame.rowconfigure(0, weight=1)

        search_store_unit_label = Label(self.store_unitFrame, text="SEARCH STORE UNIT")
        search_store_unit_label.configure(font=self.label_font)
        search_store_unit_label.grid(row=0, column=0, padx=250, sticky="we", columnspan=2)

        store_unit_label = Label(self.store_unitFrame, text="Store unit")
        store_unit_label.grid(row=1, column=0, sticky="nw")
        entry_store_unit = Entry(self.store_unitFrame, textvariable=self.content2)
        entry_store_unit.grid(row=2, column=0, sticky="nw")
        entry_store_unit.delete(0, END)

        self.buttonFrame.grid(row=1, column=0, sticky="w")
        ok_button = Button(self.buttonFrame, text="OK", command=self.call_search_store_unit)
        ok_button.grid(row=0, column=0, sticky="w")

        self.resultFrame.grid(row=2, column=0, sticky="nsew")
        self.resultFrame.columnconfigure(0, weight=1)
        self.resultFrame.rowconfigure(0, weight=1)
        self.result = Listbox(self.resultFrame)
        self.result.grid(row=0, column=0, sticky="nsew")

        self.scrollFrame.columnconfigure(0, weight=1)
        self.scrollFrame.rowconfigure(0, weight=1)
        self.scrollFrame.grid(row=2, column=1, sticky="nsew")
        self.scrollbar = Scrollbar(self.scrollFrame)
        self.scrollbar.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.config(command=self.result.yview)

        self.scrollbarX = Scrollbar(self.resultFrame)
        self.scrollbarX.grid(row=1, column=0, sticky="nsew")
        self.scrollbarX.config(orient=HORIZONTAL, command=self.result.xview)
        self.textFrame.columnconfigure(0, weight=1)
        self.textFrame.rowconfigure(0, weight=1)

    def search_position_widgets(self):
        self.remove_screen()
        self.positionFrame.grid(row=0, column=0, sticky="nw")
        self.positionFrame.columnconfigure(0, weight=0)
        self.positionFrame.rowconfigure(0, weight=1)

        search_position_label = Label(self.positionFrame, text="SEARCH POSITION")
        search_position_label.configure(font=self.label_font)
        search_position_label.grid(row=0, column=0, padx=250, sticky="we", columnspan=2)

        position_label = Label(self.positionFrame, text="Position")
        position_label.grid(row=1, column=0, sticky="nw")
        entry_position = Entry(self.positionFrame, textvariable=self.content)
        entry_position.grid(row=2, column=0, sticky="nw")
        entry_position.delete(0, END)

        self.buttonFrame.grid(row=1, column=0, sticky="w")
        ok_button = Button(self.buttonFrame, text="OK", command=self.call_search_position)
        ok_button.grid(row=0, column=0, sticky="w")

        self.resultFrame.grid(row=2, column=0, sticky="nsew")
        self.resultFrame.columnconfigure(0, weight=1)
        self.resultFrame.rowconfigure(0, weight=1)
        self.result = Listbox(self.resultFrame)
        self.result.grid(row=0, column=0, sticky="nsew")

        self.scrollFrame.columnconfigure(0, weight=1)
        self.scrollFrame.rowconfigure(0, weight=1)
        self.scrollFrame.grid(row=2, column=1, sticky="nsew")
        self.scrollbar = Scrollbar(self.scrollFrame)
        self.scrollbar.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.config(command=self.result.yview)

        self.scrollbarX = Scrollbar(self.resultFrame)
        self.scrollbarX.grid(row=1, column=0, sticky="nsew")
        self.scrollbarX.config(orient=HORIZONTAL, command=self.result.xview)
        self.textFrame.columnconfigure(0, weight=1)
        self.textFrame.rowconfigure(0, weight=1)

    def view_table_widgets(self):
        self.remove_screen()

        view_table_label = Label(self.radioFrame, text="DISPLAY ALL")
        view_table_label.configure(font=self.label_font)
        view_table_label.grid(row=0, column=0, padx=250, sticky="we", columnspan=2)

        self.resultFrame.grid(row=1, column=0, sticky="nsew")
        self.resultFrame.columnconfigure(0, weight=1)
        self.resultFrame.rowconfigure(0, weight=1)
        self.result = Listbox(self.resultFrame, font=self.my_font)
        self.result.grid(row=0, column=0, sticky="nsew", columnspan=2)

        self.scrollFrame.columnconfigure(0, weight=1)
        self.scrollFrame.rowconfigure(0, weight=1)
        self.scrollFrame.grid(row=1, column=1, sticky="nsew")
        self.scrollbar = Scrollbar(self.scrollFrame)
        self.scrollbar.grid(row=0, column=0, sticky="nsew")
        self.scrollbar.config(command=self.result.yview)

        self.scrollbarX = Scrollbar(self.resultFrame)
        self.scrollbarX.grid(row=1, column=0, sticky="nsew")
        self.scrollbarX.config(orient=HORIZONTAL, command=self.result.xview)
        self.textFrame.columnconfigure(0, weight=1)
        self.textFrame.rowconfigure(0, weight=1)

        self.radioFrame.grid(row=0, column=0, sticky="w")
        # self.radioFrame.columnconfigure(0, weight=1)
        # self.radioFrame.rowconfigure(0, weight=1)
        label = Label(self.radioFrame, text="Sort data by: ")
        label.grid(row=1, column=0, sticky="w")
        label.columnconfigure(0, weight=1)
        label.rowconfigure(0, weight=1)
        r1 = Radiobutton(self.radioFrame, variable=self.content2, text="Article", value=1,
                         command=self.call_view_table)

        r1.grid(row=2, column=0, sticky="w")
        r1.columnconfigure(0, weight=1)
        r1.rowconfigure(0, weight=1)
        r2 = Radiobutton(self.radioFrame, variable=self.content2, text="Amount", value=2,
                         command=self.call_view_table)
        r2.grid(row=3, column=0, sticky="w")

        r3 = Radiobutton(self.radioFrame, variable=self.content2, text="Store unit", value=3,
                         command=self.call_view_table)
        r3.grid(row=4, column=0, sticky="w")

        r4 = Radiobutton(self.radioFrame, variable=self.content2, text="Position", value=4,
                         command=self.call_view_table)
        r4.grid(row=5, column=0, sticky="w")

        r5 = Radiobutton(self.radioFrame, variable=self.content2, text="Date", value=5,
                         command=self.call_view_table)
        r5.grid(row=6, column=0, sticky="w")

        header = Label(self.radioFrame, font=self.my_font, text="{:<8}{:>13}{:>13}{:>10}{:>15}".format
                                                                ("Article", "Amount", "Store unit", "Position", "Date"))
        header.grid(row=7, column=0, sticky="w")

    def help_me(self):
        self.remove_screen()
        self.radioFrameH.grid(row=0, column=0, sticky="nsew", columnspan=2)
        self.radioFrameH.columnconfigure(0, weight=1)
        self.radioFrameH.rowconfigure(0, weight=1)

        help_me_label = Label(self.radioFrameH, text="HELP")
        help_me_label.configure(font=self.label_font)
        help_me_label.grid(row=0, column=0, padx=250, sticky="we", columnspan=2)

        label = Label(self.radioFrameH, text="Documentation to function: ")
        label.grid(row=1, column=0, sticky="w")

        r1 = Radiobutton(self.radioFrameH, variable=self.content5, text="Ware In", value=1,
                         command=self.call_help)
        r1.grid(row=2, column=0, sticky="w")

        r2 = Radiobutton(self.radioFrameH, variable=self.content5, text="Ware To", value=2,
                         command=self.call_help)
        r2.grid(row=3, column=0, sticky="w")

        r3 = Radiobutton(self.radioFrameH, variable=self.content5, text="Ware Out", value=3,
                         command=self.call_help)
        r3.grid(row=4, column=0, sticky="w")

        r4 = Radiobutton(self.radioFrameH, variable=self.content5, text="Search Article", value=4,
                         command=self.call_help)
        r4.grid(row=5, column=0, sticky="w")

        r5 = Radiobutton(self.radioFrameH, variable=self.content5, text="Search Store Unit", value=5,
                         command=self.call_help)
        r5.grid(row=6, column=0, sticky="w")

        r6 = Radiobutton(self.radioFrameH, variable=self.content5, text="Search Position", value=6,
                         command=self.call_help)
        r6.grid(row=7, column=0, sticky="w")

        r7 = Radiobutton(self.radioFrameH, variable=self.content5, text="Display All", value=7,
                         command=self.call_help)
        r7.grid(row=8, column=0, sticky="w")

        self.resultFrame.grid(row=1, column=0, sticky="nsew")
        self.resultFrame.columnconfigure(0, weight=1)
        self.resultFrame.rowconfigure(0, weight=1)
        self.result = Text(self.resultFrame, font=self.my_font, wrap=WORD, width=20, height=10)
        self.result.grid(row=0, column=0, sticky="nsew", rowspan=1)

        self.scrollFrame.grid(row=1, column=1, sticky="nsew")
        self.scrollbarY = Scrollbar(self.scrollFrame)
        self.scrollbarY.grid(row=0, column=0, sticky="nsew")
        self.scrollbarY.config(command=self.result.yview)
        self.scrollFrame.columnconfigure(0, weight=1)
        self.scrollFrame.rowconfigure(0, weight=1)


mainWindow = Tk()

GUI()

mainWindow.mainloop()
