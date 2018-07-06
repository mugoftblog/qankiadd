"""
The calsses and methods responsible for creating and showing GUI elements.

All GUI elements are created using Tkinter library to make the whole application
lighter and more cross-platform.
Currently GUI performs the role of controller and view together. TODO: maybe should be separated
"""


from tkinter import *
from tkinter.scrolledtext import ScrolledText
import time


class FieldController:
    """ This class contains field config and runtime related information for this field
    (e.g. current text, or action ID)
    """
    def __init__(self, id):
        self._id = id

    def set_text(self, text):
        """

        :rtype:
        :type text: str
        """
        # assert isinstance(text, str)
        #
        # txt = text
        # txt = txt.replace("\r", " ")
        # txt = txt.replace("\n", " ")
        #
        # if self.addmode == Addmode.I and self.text == "":  # TODO test more elegantly for empty strings
        #     self.text = txt
        # elif self.addmode == Addmode.W:
        #     self.text = txt
        # elif self.addmode == Addmode.A:
        #     self.text = self.text + txt

        # print("Field %s has the text: %s" % (self.name, txt))

class WindowController:
    def __init__(self, cfg):
        self._cfg = cfg
        self._fields = []

        # # clculate action ids for each field
        # # action ids here are also used as indexes to access correct field config
        # act_id = 0
        # for field in self._cfg.get_fields():
        #     #if field.shortkey != None:
        #         # self.hotkeys.append((id, field.shortkey))
        #     self._fields.append(FieldModel(act_id))
        #     act_id += 1
        #
        # self._id_max = act_id #TODO here act id will be one bigger than the latest one (act_id += 1 should not be performed for the last operation)


    def get_id_max(self):
        return self._id_max

def center(toplevel):
    toplevel.update_idletasks()
    w = toplevel.winfo_screenwidth()
    h = toplevel.winfo_screenheight()
    size = tuple(int(_) for _ in toplevel.geometry().split('+')[0].split('x'))
    x = w/2 - size[0]/2
    y = h/2 - size[1]/2
    toplevel.geometry("%dx%d+%d+%d" % (size + (x, y)))


class Gui(Frame):
    """ Class responsible for creating GUI main window.

    GUI main window shows, for example, edit boxes which allow to see and edit
    currently stored text from the data fields (e.g. questions and answers).
    """

    def __init__(self, cfg):
        self.root = Tk()
        self._cfg = cfg


        # # calculate action ids for GUI itself
        # self.id_show = act_id #show GUI
        # self.hotkey_show = ("ctrl", "o")
        # act_id += 1
        # self.id_hide = act_id #hide GUI
        # self.hotkey_hide = ("ctrl", "h")
        # act_id += 1
        # self.id_save = act_id #save TODO selected? field
        # self.hotkey_save = ("ctrl", "s")
        # act_id += 1
        # self.id_reset = act_id #reset TODO selected? field
        # self.hotkey_reset = ("ctrl", "r")

    def key_pressed(self, event):
        entry_text = event.widget.get('1.0', END)
        field = event.widget.field
        field.set_text(entry_text)

    def take_action(self, action_id):
        if action_id <= self._act_id_last:
            if id == self.id_show:
                self.show()
            elif id == self.id_hide:
                self.hide()
            elif id == self.id_save:
                self.save()
            elif id == self.id_reset:
                self.reset()
            else:
                # TODO each time perform loop not optimal solution at all
                for field in self._cfg.get_fields():
                    if field.get_id() == action_id:
                        # get the name of the data provider
                        name = field.get_data_provider_name()
                        data_provider = data_provider.get_data(name)
                        data = data_provider.get_data(field.get_text())
        else:
            print("GUI: unhandled action id %u max_id=%u" % (action_id, self._act_id_last))


    def show(self):
        """ Show GUI main window """
        Frame.__init__(self,  self.root,  bg="green")
        #self.root.resizable(width=False, height=False)

        row = 0
        for field in self.cfg.fields:
            Label(self.root, text=field.name).grid(row=row)
            #e1 = Entry(self.root, width=200)
            e1 = ScrolledText(self.root, height=10, width=100)
            e1.insert(END, field.text)
            e1.field = field
            e1.bind("<KeyRelease>", self.key_pressed)
            e1.grid(row=row, column=1)
            row+=1

        Button(self.root, text='Reset', command=self.root.quit).grid(row=row, column=0, sticky=W, pady=4)
        Button(self.root, text='Save', command=None).grid(row=row, column=1, sticky=W, pady=4)

        #self.root.minsize(width = 100, height=100)
        self.root.title(self.cfg.name)
        #self.root.overrideredirect(1) #Remove border
        center(self.root)

        #self.app = Application(cfg)
        self.root.mainloop()

        #self.lbl = Label(self.root, text="Red", bg="red", fg="white", font = ('Comic Sans MS',30))
        #self.lbl.pack(fill=BOTH)
        #self.entrythingy.minsize(width = 100, height=100)
        #self.entrythingy.pack(side = "right")
        #self.lbl.pack(expand = 1)

    def hide(self):
        """ Hide GUI main window """
        self.root.quit()

    def get_hotkeys(self):
        hotkeys = self.cfg.get_hotkeys()
        hotkeys.append(self.id_show, self.hotkey_show)
        hotkeys.append(self.id_hide, self.hotkey_hide)
        hotkeys.append(self.id_save, self.hotkey_reset)
        hotkeys.append(self.id_reset, self.hotkey_reset)

