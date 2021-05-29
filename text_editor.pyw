# -*- coding: utf-8 -*-

from tkinter import Tk, Toplevel, Menu, Frame, Label, StringVar
from tkinter.ttk import Entry, Button
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import askyesnocancel, askokcancel

from idlelib.textview import ScrollableTextFrame
from idlelib.undo import UndoDelegator
from idlelib.percolator import Percolator
from idlelib.search import find
from idlelib.replace import replace

from time import strftime
from os import remove, environ
from subprocess import call

from fpdf import FPDF


opened_file = {"name": None, "saved": True, "colorized": False, "changed": False,
               "before_changing": ""}

colors = {"a": "#ffff00", "b": "#ff8040", "c": "#ff8000", "d": "#804000",
          "e": "#808000", "f": "#80ff80", "g": "#00ff00", "h": "#008000",
          "i": "#004000", "j": "#808040", "k": "#00ff80", "l": "#008080",
          "m": "#004040", "n": "#808080", "o": "#00ffff", "p": "#004080",
          "q": "#0000ff", "r": "#000080", "s": "#408080", "t": "#0080ff",
          "u": "#0080c0", "v": "#8080ff", "w": "#0000a0", "x": "#c0c0c0",
          "y": "#ff80c0", "z": "#8080c0",

          "а": "#ffff00", "б": "#ff8040", "в": "#ff8000", "г": "#804000",
          "д": "#808000", "е": "#80ff80", "ё": "#00ff00", "ж": "#008000",
          "з": "#004000", "и": "#808040", "й": "#00ff80", "к": "#008080",
          "л": "#004040", "м": "#808080", "н": "#00ffff", "о": "#004080",
          "п": "#0000ff", "р": "#000080", "с": "#408080", "т": "#0080ff",
          "у": "#0080c0", "ф": "#8080ff", "х": "#0000a0", "ц": "#c0c0c0",
          "ч": "#ff80c0", "ш": "#8080c0", "щ": "#800040", "ъ": "#800080",
          "ы": "#ff80ff", "ь": "#ff00ff", "э": "#8000ff", "ю": "#400080",
          "я": "#ffb366"}


def hex_to_rgb(h):
    return tuple(int(h.lstrip("#")[i:i+2], 16) for i in (0, 2, 4))


def save_pdf(f):
    data = text_filed.text.get("1.0", "end")
    data = data[:len(data) - 1]
    pdf = FPDF(unit="pt")
    pdf.add_page()
    pdf.add_font("Courier", "", r"c:\windows\fonts\cour.ttf", uni=True)
    pdf.set_font("Courier", size=9)
    if opened_file["colorized"]:
        for ln_i, ln in enumerate(data.split("\n")):
            for col_i, col in enumerate(ln):
                if col.lower() in colors.keys():
                    pdf.set_text_color(*hex_to_rgb(colors[col.lower()]))
                else:
                    pdf.set_text_color(0, 0, 0)
                pdf.set_xy(col_i * 6, ln_i * 10)
                pdf.cell(10, 10, txt=col)
    else:
        pdf.set_text_color(0, 0, 0)
        pdf.cell(10, 10, txt=data)
    pdf.output(f)


def read():
    f = askopenfilename(title="Open")
    if not opened_file["saved"]:
        ans = askyesnocancel(title="Text", message="Save changes?")
        if ans is None:
            return
        elif ans:
            save()
    if f is not None and f != '':  # Открыть только существующий файл
        text_filed.text.delete("1.0", "end")
        root.title("Text - %s" % f)
        opened_file["name"] = f
        with open(f, "rb") as rf:
            r = rf.read().decode()
            text_filed.text.insert("end", r)
            opened_file["before_changing"] = r


def save(_as=False):
    # Если файл уже открыт, нужно сохранить изменения
    if opened_file["name"] is not None and not _as:
        if opened_file["name"].split(".")[1] != "pdf":
            with open(opened_file["name"], "w") as sf:
                opened_file["saved"] = True
                sf.write(text_filed.text.get("1.0", "end"))
        else:
            save_pdf(opened_file["name"])

    if _as or opened_file["name"] is None:
        f = asksaveasfilename(title="Save as...", defaultextension=".txt",
                              filetypes=(("Text File", "*.txt"), ("Portable Document Format", "*.pdf"),
                                         ("All Files", "*.*")))
        if f is not None and f != '':
            if f.split(".")[1] != "pdf":
                with open(f, "w") as wf:
                    root.title("Text - %s" % f)
                    wf.write(text_filed.text.get("1.0", "end"))

            else:
                save_pdf(f)
            opened_file["name"] = f
            opened_file["saved"] = True
            root.title("Text - %s" % opened_file["name"])


def new():
    if not (opened_file["saved"] and opened_file["changed"]):
        ans = askyesnocancel(title="Text", message="Save changes?")
        if ans is None:
            return
        elif ans:
            save()
        # Возврат всего в изначальное состояние
        text_filed.text.delete("1.0", "end")
        opened_file["name"] = None
        opened_file["saved"] = False
        opened_file["colorized"] = False
        root.title("Text")


def exit_from_shell():
    if (not opened_file["saved"]) and opened_file["changed"]:
        ans = askyesnocancel(title="Text", message="Save changes?")
        if ans is None:
            return
        elif ans:
            save()
    exit(0)


def print_dialog():
    if not askokcancel("Print", "Print to default printer?"):
        return
    if not opened_file["saved"]:
        t_file = open(environ["TEMP"] + "\\printtmpedittext654.txt", "w")
        t_file.write(text_filed.text.get("1.0", "end"))
        t_file.close()
        call("notepad.exe /p %s" % t_file.name)
        remove(environ["TEMP"] + "\\printtmpedittext654.txt")
    else:
        call("notepad.exe /p %s" % opened_file["name"])


def colorize():
    text = text_filed.text.get("1.0", "end").lower()
    for ln_index, line in enumerate(text.split("\n"), start=1):
        for cl_index, column in enumerate(line):
            if column in colors.keys():
                text_filed.text.tag_add(colors[column], "%s.%s" % (ln_index, cl_index),
                                        "%s.%s" % (ln_index, cl_index+1))
                text_filed.text.tag_config(colors[column], foreground=colors[column])
    opened_file["colorized"] = True


def make_black():
    for tag in text_filed.text.tag_names():
        text_filed.text.tag_delete(tag)
    opened_file["colorized"] = False


def on_type_text(event):
    if text_filed.text.get("1.0", "end") != opened_file["before_changing"]:
        opened_file["changed"] = True  # Теперь файл изменен,
        opened_file["saved"] = False  # Но не сохранен
    status_label.config(text=text_filed.text.index("insert").replace(".", " | "))


class GotoDialog:

    def __init__(self, master, text_field):
        self.root = Toplevel(master)
        self.root.geometry("400x100+%s+%s" % (int(master.winfo_x() + (master.winfo_width() - 400) / 2),
                                              int(master.winfo_y() + (master.winfo_height() - 100) / 2)))
        self.root.resizable(0, 0)
        self.root.title("Go to...")
        self.root.transient(master)
        self.root.grab_set()
        self.root.focus_set()
        Label(self.root, text="Enter positive line index\n('end' - end of file)").pack()

        self.index_var = StringVar()
        self.index_entry = Entry(self.root, textvariable=self.index_var)
        self.index_entry.pack(fill="x", padx=10, pady=5)

        self.ok = Button(self.root, text="OK", width=15, command=self.goto)
        self.ok.pack(anchor="ne", padx=5, pady=5)
        self.root.bind_all("<KeyPress-Return>", lambda event: self.goto())

        self.text_field = text_field.text

    def destroy(self):
        self.root.destroy()

    def goto(self):
        if self.index_var.get().lower() == "end":
            self.text_field.mark_set("insert", "end")
        else:
            self.text_field.mark_set("insert", "%s.0" % self.index_var.get())
        self.destroy()

    def mainloop(self):
        self.root.mainloop()


root = Tk()
menu = Menu(root)

root.config(menu=menu)
root.geometry("580x700")
root.title("Text")

root.bind_all("<KeyPress-F5>", lambda event: text_filed.text.insert("end", strftime("%H:%M %d.%m.%Y")))  # Дата и время

text_filed = ScrollableTextFrame(root)
text_filed.pack(fill="both", expand=1)
text_filed.text.config(inactiveselectbackground="#0078d7")
text_filed.text.undo_block_start = lambda: None
text_filed.text.undo_block_stop = lambda: None

file_menu = Menu(menu, tearoff=0)
file_menu.add_command(label="New", accelerator="Ctrl+N", command=new)
file_menu.add_command(label="Open", accelerator="Ctrl+O", command=read)
file_menu.add_command(label="Save", accelerator="Ctrl+S", command=save)
file_menu.add_command(label="Save as...", accelerator="Ctrl+Shift+S", command=lambda: save(_as=True))
file_menu.add_separator()
file_menu.add_command(label="Print File", accelerator="Ctrl+P", command=print_dialog)
file_menu.add_separator()
file_menu.add_command(label="Exit", accelerator="Alt+F4", command=exit_from_shell)

edit_menu = Menu(menu, tearoff=0)
edit_menu.add_command(label="Undo", accelerator="Ctrl+Z", command=lambda: undo_delegator.undo_event(None))
edit_menu.add_command(label="Redo", accelerator="Ctrl+Y", command=lambda: undo_delegator.redo_event(None))
edit_menu.add_separator()
edit_menu.add_command(label="Cut", accelerator="Ctrl+X",
                      command=lambda: text_filed.text.event_generate("<Control-x>"))
edit_menu.add_command(label="Copy", accelerator="Ctrl+C",
                      command=lambda: text_filed.text.event_generate("<Control-c>"))
edit_menu.add_command(label="Paste", accelerator="Ctrl+V",
                      command=lambda: text_filed.text.event_generate("<Control-v>"))
edit_menu.add_command(label="Select all", accelerator="Ctrl+A",
                      command=lambda: text_filed.text.event_generate("<Control-a>"))
edit_menu.add_separator()
edit_menu.add_command(label="Find", accelerator="Ctrl+F",
                      command=lambda: find(text_filed.text))
edit_menu.add_command(label="Replace...", accelerator="Ctrl+R",
                      command=lambda: replace(text_filed.text))
edit_menu.add_command(label="Go to...", accelerator="Ctrl+G",
                      command=lambda: GotoDialog(root, text_filed).mainloop())
edit_menu.add_command(label="Time and date    ", accelerator="F5",  # Вставить дату и время
                      command=lambda: text_filed.text.insert("end", strftime("%H:%M %d.%m.%Y")))
edit_menu.add_separator()
edit_menu.add_command(label="Fun", command=colorize)
edit_menu.add_command(label="Normalize", command=make_black)

menu.add_cascade(label="File", menu=file_menu)
menu.add_cascade(label="Edit", menu=edit_menu)

context_menu = Menu(text_filed.text, tearoff=0)
context_menu.add_command(label="Undo", command=lambda: undo_delegator.undo_event(None))
context_menu.add_command(label="Redo", command=lambda: undo_delegator.redo_event(None))
context_menu.add_separator()
context_menu.add_command(label="Cut", command=lambda: text_filed.text.event_generate("<Control-x>"))
context_menu.add_command(label="Copy", command=lambda: text_filed.text.event_generate("<Control-c>"))
context_menu.add_command(label="Paste", command=lambda: text_filed.text.event_generate("<Control-v>"))
context_menu.add_command(label="Select all", command=lambda: text_filed.text.event_generate("<Control-a>"))
context_menu.add_separator()
context_menu.add_command(label="Fun", command=colorize)
context_menu.add_command(label="Normalize", command=make_black)
text_filed.text.bind("<Button-3>", lambda event: context_menu.post(event.x_root, event.y_root))

percolator = Percolator(text_filed.text)
undo_delegator = UndoDelegator()
percolator.insertfilter(undo_delegator)

# Показать текущее расположение курсора (текстового)
text_filed.text.bind("<ButtonRelease-1>", on_type_text)
text_filed.text.bind("<KeyRelease>", on_type_text)

text_filed.text.bind("<Control-o>", lambda event: read())
text_filed.text.bind("<Control-s>", lambda event: save())
text_filed.text.bind("<Control-Shift-S>", lambda event: save(_as=True))
text_filed.text.bind("<Control-n>", lambda event: new())
text_filed.text.bind("<Control-p>", lambda event: print_dialog())

text_filed.text.bind("<Control-z>", lambda event: undo_delegator.undo_event(None))
text_filed.text.bind("<Control-y>", lambda event: undo_delegator.redo_event(None))
text_filed.text.bind("<Control-g>", lambda event: GotoDialog(root, text_filed).mainloop())
text_filed.text.bind("<Control-f>", lambda event: find(text_filed.text))
text_filed.text.bind("<Control-r>", lambda event: replace(text_filed.text))

text_filed.text.focus_set()

status_bar = Frame(root, height=20, relief="raised", bd=2)
status_bar.pack(anchor="nw", fill="both")
status_label = Label(status_bar, text="1 | 0", font="Helvetica 10")
status_label.pack(anchor="ne")

root.protocol("WM_DELETE_WINDOW", exit_from_shell)
root.mainloop()
