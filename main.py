import sqlite3
import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk

mainWindow = Tk()
mainWindow.title('App Name')
mainWindow.resizable(FALSE, FALSE)
mainWindow_width = 780
mainWindow_height = 400

screen_width = mainWindow.winfo_screenwidth()
screen_height = mainWindow.winfo_screenheight()

x = (screen_width / 2) - (mainWindow_width / 2)
y = (screen_height / 2) - (mainWindow_height / 2)

mainWindow.geometry(f'{mainWindow_width}x{mainWindow_height}+{int(x)}+{int(y)}')

def uzsakymai():
    # mainWindow.withdraw()
    mainWindow.iconify()

    uzsakymai_frame = Toplevel(mainWindow)
    uzsakymai_frame.title("UZSAKYMAI")
    uzsakymai_frame_width = 1024
    uzsakymai_frame_height = 600

    screen_width = uzsakymai_frame.winfo_screenwidth()
    screen_height = uzsakymai_frame.winfo_screenheight()

    x = (screen_width / 2) - (uzsakymai_frame_width / 2)
    y = (screen_height / 2) - (uzsakymai_frame_height / 2)

    uzsakymai_frame.geometry(f'{uzsakymai_frame_width}x{uzsakymai_frame_height}+{int(x)}+{int(y)}')

    conn = sqlite3.connect('uzsakymai.db')

    c = conn.cursor()

    c.execute("""CREATE TABLE if not exists uzsakymai (
        IMONE text,
        TELEFONAS text,
        PROJEKTAS text,
        TERMINAS text,
        STATUSAS text,
        ID text
        )
        """)

    # Refresh database
    def query_database():
        for record in my_tree.get_children():
            my_tree.delete(record)

        conn = sqlite3.connect('uzsakymai.db')

        c = conn.cursor()

        c.execute("SELECT rowid, * FROM uzsakymai")
        records = c.fetchall()

        my_tree.tag_configure('oddrow', background='white')
        my_tree.tag_configure('evenrow', background='lightblue')

        global count
        count = 0

        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[1], record[2], record[3],
                                       record[4], record[5], record[0]), tags='oddrow')
            else:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[1], record[2], record[3],
                                       record[4], record[5], record[0]), tags='evenrow')

            count += 1

        conn.commit()

        conn.close()

    # Upper buttons frame and search bar
    upper_frame_buttons = LabelFrame(uzsakymai_frame, text='Search')
    upper_frame_buttons.pack(padx=10, pady=(5, 0), anchor=W)

    upper_frame_buttons.columnconfigure(0, weight=1)
    upper_frame_buttons.columnconfigure(1, weight=1)
    upper_frame_buttons.columnconfigure(2, weight=1)
    upper_frame_buttons.columnconfigure(3, weight=1)
    upper_frame_buttons.columnconfigure(4, weight=1)
    upper_frame_buttons.rowconfigure(0, weight=1)
    upper_frame_buttons.rowconfigure(1, weight=1)

    # Search Bar
    search_box = Entry(upper_frame_buttons, bd=3, width=30)
    search_box.grid(row=1, column=0, sticky="w", padx=5)

    def search_records():
        search_record = search_box.get()

        for record in my_tree.get_children():
            my_tree.delete(record)

        conn = sqlite3.connect('uzsakymai.db')

        c = conn.cursor()

        c.execute("SELECT rowid, * FROM uzsakymai WHERE projektas like ?", (search_record,))
        records = c.fetchall()

        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[1], record[2], record[3],
                                       record[4], record[5], record[0]), tags='oddrow')
            else:
                my_tree.insert(parent='', index='end', iid=count, text='',
                               values=(record[1], record[2], record[3],
                                       record[4], record[5], record[0]), tags='evenrow')
            count += 1

        conn.commit()

        conn.close()

    search_record = Button(upper_frame_buttons, text='Search', command=search_records, bg='lightgrey', width=6,
                           font='sans 10')
    search_record.grid(row=2, column=0, sticky="w", pady=(3, 5), padx=5)

    undo_search_record = Button(upper_frame_buttons, text="Cancel", command=query_database, bg='lightgrey', width=6,
                                font='sans 10')
    undo_search_record.grid(row=2, column=0, sticky="w", pady=(3, 5), padx=(65, 0))

    # Style
    style = ttk.Style()

    # Theme
    style.theme_use("clam")
    # Treeview colors
    style.configure("Treeview",
                    background="white",
                    foreground="black",
                    rowheight=(25),
                    fieldbackground="white"
                    )
    # Change selected color
    style.map('Treeview',
              background=[('selected', 'blue')])

    # TreeView frame
    tree_frame = Frame(uzsakymai_frame)
    tree_frame.pack(side=TOP, pady=10, padx=10, fill=tkinter.BOTH, expand=TRUE)

    # Scrollbar
    tree_scroll = Scrollbar(tree_frame)
    tree_scroll.pack(side=RIGHT, fill=Y)

    # selectmode='browse' - leidzia tik 1 eilute selectint
    my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)
    my_tree.pack(side=TOP, fill=tkinter.BOTH, expand=TRUE)

    # Sort columns
    def tvsort_column(tv, col, reverse):
        l = [(tv.set(k, col), k) for k in tv.get_children('')]
        l.sort(reverse=reverse)

        # rearrange items in sorted positions
        for index, (val, k) in enumerate(l):
            tv.move(k, '', index)

        # reverse sort next time
        tv.heading(col, text=col, command=lambda _col=col:
        tvsort_column(tv, _col, not reverse))

    # Column list names
    my_tree['columns'] = ("IMONE", "TELEFONAS", "PROJEKTAS", "TERMINAS", "STATUSAS", "ID")

    # Column size
    my_tree.column("#0", width=0, stretch=NO)
    my_tree.column("IMONE", anchor=W, width=100)
    my_tree.column("TELEFONAS", anchor=W, width=100)
    my_tree.column("PROJEKTAS", anchor=W, width=100)
    my_tree.column("TERMINAS", anchor=W, width=100)
    my_tree.column("STATUSAS", anchor=W, width=100, stretch=NO)
    my_tree.column("ID", anchor=W, width=0, stretch=NO)

    # Column name
    my_tree.heading("#0", text="", anchor=W)
    my_tree.heading("IMONE", text="IMONE", anchor=W)
    my_tree.heading("TELEFONAS", text="TELEFONAS", anchor=W)
    my_tree.heading("PROJEKTAS", text="PROJEKTAS", anchor=W)
    my_tree.heading("TERMINAS", text="TERMINAS", anchor=W)
    my_tree.heading("STATUSAS", text="STATUSAS", anchor=W)
    my_tree.heading("ID", text="ID", anchor=W)

    # Configure scrollbar
    tree_scroll.config(command=my_tree.yview)
    # sort column
    for col in my_tree['columns']:
        my_tree.heading(col, text=col, command=lambda _col=col:
        tvsort_column(my_tree, _col, False))

    # delete records
    def delete_record():
        lentele = messagebox.askyesno("DELETE RECORD", "Ar tikrai norit istrinti?", parent=uzsakymai_frame)
        if lentele == 1:
            # norimas pasirinkimas
            x = my_tree.selection()

            # create list of ids
            ids_to_delete = []

            # prideti ka nori istrint
            for record in x:
                ids_to_delete.append(my_tree.item(record, 'values')[5])
            # istrinti
            for record in x:
                my_tree.delete(record)

            conn = sqlite3.connect('uzsakymai.db')

            c = conn.cursor()

            c.executemany("DELETE FROM uzsakymai WHERE oid = ?", [(a,) for a in ids_to_delete])

            ids_to_delete = []

            conn.commit()

            conn.close()

            query_database()

    def new_record():
        new_record_frame = Toplevel(uzsakymai_frame)
        new_record_frame.title('NEW RECORD')
        mainWindow.resizable(FALSE, FALSE)

        new_record_frame_width = 380
        new_record_frame_height = 270

        screen_width = new_record_frame.winfo_screenwidth()
        screen_height = new_record_frame.winfo_screenheight()

        x = (screen_width / 2) - (new_record_frame_width / 2)
        y = (screen_height / 2) - (new_record_frame_height / 2)

        new_record_frame.geometry(f'{new_record_frame_width}x{new_record_frame_height}+{int(x)}+{int(y)}')

        data_frame = Frame(new_record_frame)
        data_frame.pack(pady=5, padx=5, anchor=N)

        id = Label(data_frame, text="ID", relief=RAISED, bd=3, font='sans 10', bg='lightyellow', width=15, height=2)
        id.grid(row=4, column=0, sticky="nsew")

        pv = Label(data_frame, text="IMONE", relief=RAISED, bd=3, font='sans 10', bg='lightyellow', width=15,
                   height=2)
        pv.grid(row=0, column=0, sticky="nsew")

        vt = Label(data_frame, text="TELEFONAS", relief=RAISED, bd=3, font='sans 10', bg='lightyellow', width=15,
                   height=2)
        vt.grid(row=1, column=0, sticky="nsew")

        ks = Label(data_frame, text="PROJEKTAS", relief=RAISED, bd=3, font='sans 10', bg='lightyellow', width=15,
                   height=2)
        ks.grid(row=2, column=0, sticky="nsew")

        km = Label(data_frame, text="TERMINAS", relief=RAISED, bd=3, font='sans 10', bg='lightyellow', width=15,
                   height=2)
        km.grid(row=3, column=0, sticky="nsew")

        km1 = Label(data_frame, text="STATUSAS", relief=RAISED, bd=3, font='sans 10', bg='lightyellow', width=15,
                    height=2)
        km1.grid(row=4, column=0, sticky="nsew")

        # Data input
        id_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED, width=30)
        id_box.grid(row=4, column=1, sticky="nsew")

        pv_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED, width=30)
        pv_box.grid(row=0, column=1, sticky="nsew")

        vt_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED, width=30)
        vt_box.grid(row=1, column=1, sticky="nsew")

        ks_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED, width=30)
        ks_box.grid(row=2, column=1, sticky="nsew")

        km_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED, width=30)
        km_box.grid(row=3, column=1, sticky="nsew")

        km1_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED, width=30)
        km1_box.grid(row=4, column=1, sticky="nsew")
        km1_box.insert(END, 'GAMINA')

        def add_record():
            conn = sqlite3.connect('uzsakymai.db')

            c = conn.cursor()

            c.execute("""INSERT INTO uzsakymai VALUES (:imone, :telefonas, :projektas, 
            :terminas, :statusas, :id)""",
                      {
                          'imone': pv_box.get(),
                          'konstruktorius': vt_box.get(),
                          'projektas': ks_box.get(),
                          'terminas': km_box.get(),
                          'statusas': km1_box.get(),
                          'id': id_box.get(),
                      })

            conn.commit()

            conn.close()

            pv_box.delete(0, END)
            vt_box.delete(0, END)
            ks_box.delete(0, END)
            km_box.delete(0, END)
            km1_box.delete(0, END)
            id_box.delete(0, END)

            my_tree.delete(*my_tree.get_children())
            query_database()

            new_record_frame.destroy()

        def cancel_add_record():
            new_record_frame.destroy()

        add_record = Button(data_frame, text="OK", command=add_record, width=8, bg='lightgrey', font='sans 10',
                            height=2)
        add_record.grid(row=5, column=0, sticky="w", pady=(10, 0))

        cancel_add_record = Button(data_frame, text="Cancel", command=cancel_add_record, width=8, bg='lightgrey',
                                   font='sans 10', height=2)
        cancel_add_record.grid(row=5, column=0, sticky="w", padx=(76, 0), pady=(10, 0))

    # exit gamyba_frame
    def exit_top_level():
        uzsakymai_frame.destroy()
        # mainWindow.deiconify()

    # update record double click frame
    update_name_frame = Frame(uzsakymai_frame)
    update_name_frame.pack(anchor=W, padx=10)

    def update_record_double(e):
        top_level_update = Toplevel(uzsakymai_frame)
        top_level_update.title('EDIT RECORD')

        top_level_update_width = 1024
        top_level_update_height = 150

        screen_width = top_level_update.winfo_screenwidth()
        screen_height = top_level_update.winfo_screenheight()

        x = (screen_width / 2) - (top_level_update_width / 2)
        y = (screen_height / 2) - (top_level_update_height / 2)

        top_level_update.geometry(f'{top_level_update_width}x{top_level_update_height}+{int(x)}+{int(y)}')

        data_frame = Frame(top_level_update, relief=SUNKEN)
        data_frame.pack(anchor=N, fill=tkinter.X, pady=5, padx=5)

        data_frame.columnconfigure(0, weight=1)
        data_frame.columnconfigure(1, weight=1)
        data_frame.columnconfigure(2, weight=1)
        data_frame.columnconfigure(3, weight=1)
        data_frame.columnconfigure(4, weight=1)
        data_frame.rowconfigure(0, weight=1)
        data_frame.rowconfigure(1, weight=1)
        data_frame.rowconfigure(2, weight=1)

        # Data name, ID pasleptas
        id = Label(data_frame, text="ID", font='sans 10', relief=RAISED, bd=3, bg='lightyellow', height=2)
        id.grid(row=0, column=0, sticky="nsew")

        pv = Label(data_frame, text="IMONES", font='sans 10', relief=RAISED, bd=3, bg='lightyellow', height=2)
        pv.grid(row=0, column=0, sticky="nsew")

        vt = Label(data_frame, text="TELEFONAS", font='sans 10', relief=RAISED, bd=3, bg='lightyellow', height=2)
        vt.grid(row=0, column=1, sticky="nsew")

        ks = Label(data_frame, text="PROJEKTAS", font='sans 10', relief=RAISED, bd=3, bg='lightyellow', height=2)
        ks.grid(row=0, column=2, sticky="nsew")

        km = Label(data_frame, text="TERMINAS", font='sans 10', relief=RAISED, bd=3, bg='lightyellow', height=2)
        km.grid(row=0, column=3, sticky="nsew")

        km1 = Label(data_frame, text="STATUSAS", font='sans 10', relief=RAISED, bd=3, bg='lightyellow', height=2)
        km1.grid(row=0, column=4, sticky="nsew")

        # Data input
        id_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED)
        id_box.grid(row=1, column=0, sticky="nsew", ipady=8)

        pv_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED)
        pv_box.grid(row=1, column=0, sticky="nsew", ipady=8)

        vt_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED)
        vt_box.grid(row=1, column=1, sticky="nsew", ipady=8)

        ks_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED)
        ks_box.grid(row=1, column=2, sticky="nsew", ipady=8)

        km_box = Entry(data_frame, bd=3, font='sans 10', relief=RAISED)
        km_box.grid(row=1, column=3, sticky="nsew", ipady=8)

        km1_box = ttk.Combobox(data_frame, font='sans 10', state='normal', textvariable=StringVar())
        km1_box['values'] = ('GAMINA', 'VELUOJA', 'PAGAMINTA')
        km1_box.grid(row=1, column=4, sticky="nsew", ipady=8)

        def select_record(e):
            # istrina sena irasa
            pv_box.delete(0, END)
            vt_box.delete(0, END)
            ks_box.delete(0, END)
            km_box.delete(0, END)
            km1_box.delete(0, END)
            id_box.delete(0, END)

            selected = my_tree.focus()
            values = my_tree.item(selected, 'values')

            # uzpildo langelius
            pv_box.insert(0, values[0])
            vt_box.insert(0, values[1])
            ks_box.insert(0, values[2])
            km_box.insert(0, values[3])
            km1_box.insert(0, values[4])
            id_box.insert(0, values[5])

        def update_record_all():
            selected = my_tree.focus()
            my_tree.item(selected, text="", values=(pv_box.get(), vt_box.get(), ks_box.get(), km1_box.get(),
                                                    km_box.get(), id_box.get()))

            conn = sqlite3.connect('uzsakymai.db')

            c = conn.cursor()

            c.execute("""UPDATE uzsakymai SET
                   imone = :imone,
                   telefonas = :telefonas,
                   projektas = :projektas,
                   terminas = :terminas,
                   statusas = :statusas

                   WHERE oid = :oid""",
                      {
                          'imone': pv_box.get(),
                          'telefonas': vt_box.get(),
                          'projektas': ks_box.get(),
                          'terminas': km_box.get(),
                          'statusas': km1_box.get(),
                          'oid': id_box.get(),
                      }
                      )

            conn.commit()

            conn.close()

            pv_box.delete(0, END)
            vt_box.delete(0, END)
            ks_box.delete(0, END)
            km_box.delete(0, END)
            km1_box.delete(0, END)
            id_box.delete(0, END)

            query_database()

            top_level_update.destroy()

        my_tree.bind("<ButtonRelease-1>", select_record)

        def exit_update_record_all():
            top_level_update.destroy()

        update_record1 = Button(data_frame, text="OK", font='sans 10', command=update_record_all, width=8,
                                bg='lightgrey', height=2)
        update_record1.grid(row=2, column=0, sticky="w", pady=(10, 0))

        cancel_entries = Button(data_frame, text="Cancel", font='sans 10', command=exit_update_record_all, width=8,
                                bg='lightgrey', height=2)
        cancel_entries.grid(row=2, column=0, sticky="w", padx=(76, 0), pady=(10, 0))

    # bind on DELETE button
    def delete_record1(e):
        lentele = messagebox.askyesno("DELETE RECORD", "Ar tikrai norit istrinti?", parent=uzsakymai_frame)
        if lentele == 1:
            # norimas pasirinkimas
            x = my_tree.selection()

            # create list of ids
            ids_to_delete = []

            # prideti ka nori istrint
            for record in x:
                ids_to_delete.append(my_tree.item(record, 'values')[5])
            # istrinti
            for record in x:
                my_tree.delete(record)

            conn = sqlite3.connect('uzsakymai.db')

            c = conn.cursor()

            c.executemany("DELETE FROM uzsakymai WHERE oid = ?", [(a,) for a in ids_to_delete])

            ids_to_delete = []

            conn.commit()

            conn.close()

            query_database()

    # # clear entries command
    # def clear_entries():
    #     pv_box.delete(0, END)
    #     vt_box.delete(0, END)
    #     ks_box.delete(0, END)
    #     km_box.delete(0, END)
    #     id_box.delete(0, END)

    # # only this window is activate, others are locked
    # mainWindow.focus_set()
    # mainWindow.grab_set()

    # Menu bar
    menu_bar1 = Menu(uzsakymai_frame)
    uzsakymai_frame.config(menu=menu_bar1)
    # tearoff nuima File menu atskyrima
    file_menu1 = Menu(menu_bar1, tearoff=0)
    menu_bar1.add_cascade(label="File", menu=file_menu1)
    file_menu1.add_command(label="New", command=new_record)
    file_menu1.add_command(label="Delete", command=delete_record)
    file_menu1.add_separator()
    file_menu1.add_command(label="Exit", command=exit_top_level)

    def do_popup(event):
        try:
            my_menu2.tk_popup(event.x_root, event.y_root)
        finally:
            my_menu2.grab_release()

    my_menu2 = Menu(my_tree, tearoff=False)
    my_menu2.add_command(label='New', command=new_record)
    my_menu2.add_command(label='Delete', command=delete_record)

    # Bind Treeview (pass with 'e' in function), select
    my_tree.bind('<Button-3>', do_popup)
    my_tree.bind('<Double-Button-1>', update_record_double)
    my_tree.bind('<Key-Delete>', delete_record1)

    # put data back to table
    query_database()

uzsakymai()

mainloop()
