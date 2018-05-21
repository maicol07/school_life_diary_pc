from ttkthemes.themed_style import *


def init():
    """
    Inizializzazione stile widget
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
    s.configure('.', font=('Helvetica', 10))
