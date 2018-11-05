import os.path

from ttkthemes.themed_style import *


def style_init():
    """
    Inizializzazione delle variabili globali
    :return:
    """
    global s
    s = ThemedStyle()
    s.configure("TFrame", background="white")
    s.configure("TButton", height=100)
    s.configure("TLabel", background="white")
    s.configure("TPhotoimage", background="white")
    s.configure("TLabelframe", background="white")
    s.configure("TLabelframe.Label", background="white")
    s.configure("TScale", background="white")
    s.configure("TCheckbutton", background="white")
    s.configure('.', font=('Arial', 10, "normal roman"))


def path_init():
    global path
    if (not (os.path.exists("path.txt"))):
        path = os.path.expanduser(r'~\Documents\School Life Diary')
    else:
        txt = open("path.txt")
        path = txt.read() + "\School Life Diary"
        txt.close()
