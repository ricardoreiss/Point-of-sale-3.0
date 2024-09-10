from tkinter import Tk
from helper.dateFunction import getDateToday
from app import Application

import ctypes
import sys

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

if is_admin():
    # Se o programa está sendo executado como administrador, continue com o código principal aqui
    print("Executando como administrador.")
    #Start da Janela

    root_principal = Tk()
    root_principal.title('AutoMec')
    root_principal.iconbitmap("logo.ico")
    #root_principal.state('zoomed')
    app = Application(master=root_principal, data=getDateToday())
    app.mainloop()
else:
    # Se o programa não está sendo executado como administrador, mostre uma mensagem de aviso
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

# root_principal = Tk()
# root_principal.title('Point-of-Sale')
# root_principal.iconbitmap("logo.ico")
# #root_principal.state('zoomed')
# app = Application(master=root_principal, data=getDateToday())
# app.mainloop()