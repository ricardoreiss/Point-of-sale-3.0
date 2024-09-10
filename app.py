import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel
from tkcalendar import DateEntry
from tkinter import filedialog
import json
import os

from components.ServiceClass import Service
from JSON_db.manageJSONFile import save_data, def_address
from helper.createPDF import criar_nota

# Abrir o arquivo JSON e carregar os dados
with open("JSON_db/orderserver.json", "r") as file_json:
    val_orderserver = json.load(file_json)

old_service = ''

class Application(tk.Frame):
    def __init__(self, master = None, data = None):
        super().__init__(master)
        self.master = master
        self.val_orderserver = val_orderserver
        self.servico = Service(f"{(val_orderserver['ordem de servico'][-1] + 1):06d}", '', '', data, '', '', '', '', '', '', '', '', [], '')
        self.old_service = old_service
        if old_service:
            self.servico = Service(old_service['ordem'], old_service['ncliente'], old_service['telefone'], old_service['data'], old_service['placa'], old_service['marca'], old_service['modelo'], old_service['cor'], old_service['ano'], old_service['kmatual'], old_service['observacoes'], old_service['maodeobra'], old_service['pecas'], old_service['desconto'])
        self.grid()
        self.data = data
        self.produtos = self.servico.pecas
        self.valTot = 0
        self.aut = 0
        self.clic = ''
        self.posi_desc = 0
        self.posi_valUnit = 1
        self.posi_qtd = 2
        self.posi_valTot = 3
        self.travel_selecao = ''
        self.values = ''
        self.travel_tabel = ''
        self.point_click = ''
        self.enter_foc = ''
        self.d_f =[]
        self.travel_ValQtd = []
        self.label_TotServ = ''
        self.maodeobra = ''
        if old_service == '':
            self.create()

    def create(self):

        #Texto 
        self.label_s = tk.Label(self.master, text='', font=('Calibri', 100))
        self.label_s.grid(row=0, column=0, columnspan=2)

        self.image = PhotoImage(file="AUTOMEC.png")

        #Texto 
        self.label_img = tk.Label(self.master, image=self.image, font=('Calibri', 13))
        self.label_img.grid(row=0, column=0, columnspan=2, rowspan=5)

        #Botão Criar Novo
        self.botao_create = tk.Button(self.master, text='Criar Novo Serviço', font=('Calibri', 13), bg='#6a88b5', command=self.new_server, width=45)
        self.botao_create.grid(row=1, rowspan=1, pady=5, padx=5, column=0, columnspan=2)

        #Entry Serviço
        datas = []
        nomes_arquivos = os.listdir("./JSON_db/")
        for nome_arquivo in nomes_arquivos:
            if '.json' in nome_arquivo:
                datas.append(nome_arquivo[:-5])
        datas = datas[:-1]

        def listar_sus(*args):
            new_datas = []
            for data1 in datas:
                if (self.enter_data.get()).upper() in data1:
                    new_datas.append(data1)
            if self.enter_data == '':
                new_datas = datas

            self.enter_data.config(values=new_datas)

        #Texto
        self.label_select = tk.Label(self.master, text='OU SELECIONE UM JÁ EXISTENTE', font=('Calibri', 13), bg="#2a4e68", fg="white")
        self.label_select.grid(row=2, column=0, columnspan=2)

        #Entry Data
        self.entry_var_data = tk.StringVar()
        self.enter_data = ttk.Combobox(self.master, font=('Calibri', 13), width=36, values=datas, textvariable=self.entry_var_data, validate = "key")
        self.enter_data.grid(row=3, column=0,pady=0, padx=5)
        ttk.Style().configure("TCombobox", fieldbackground="#DCDCDC")

        #Botão Criar Novo
        self.botao_open = tk.Button(self.master, text='Abrir', font=('Calibri', 13), bg='#6a88b5', command=self.open_server, width=7)
        self.botao_open.grid(row=3, rowspan=1, pady=0, padx=0, column=1, columnspan=1)

        self.entry_var_data.trace_add("write", listar_sus)

    def new_server(self):
        global old_service
        old_service = def_address('')
        self.create_page()

    def open_server(self):
        global old_service
        old_service = def_address(self.enter_data.get())
        self.create_page()
    
    def create_page(self):
        self.label_s.destroy()
        self.label_img.destroy()
        self.botao_create.destroy()
        self.label_select.destroy()
        self.enter_data.destroy()
        self.botao_open.destroy()
        self.__init__(master=self.master, data=self.data)
        self.create_widgets()
        self.add_bbtc()

    def clean_ent(self):
        self.enter_desc.delete(0, 'end')
        self.enter_Qtd.destroy()
        self.enter_valUnit.destroy()
        self.enter_valUnit = tk.Entry(self.master, font=('Calibri', 20), width=6, validate="key", validatecommand=(self.validacao_numeros, "%S"))
        self.enter_valUnit.grid(row=12, column=7, sticky='e')
        self.enter_Qtd = tk.Entry(self.master, font=('Calibri', 20), width=4, validate="key")
        self.enter_Qtd['validatecommand'] = (self.enter_Qtd.register(self.testVal),'%P','%d')
        self.enter_Qtd.grid(row=12, column=8)

    def tabel(self):  
        if self.travel_tabel:
            self.my_tree.destroy()

        style = ttk.Style()
        style.theme_use("alt")
        # Pick a theme
        style.configure("Treeview", background="#DCDCDC", fieldbackground="#DCDCDC")
        style.configure('Treeview.Heading', background='#b1b3b2', foreground="black", font=('Calibri', 20))

        # Change selected color
        style.map('Treeview', background=[('selected', 'blue')])

        # Create Treeview Frame
        tree_frame = Frame(self.master)
        tree_frame.grid(row=2, rowspan=9, column=5, columnspan=5, sticky='wn', pady=5)

        # Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        # Create Treeview
        self.my_tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set, height=21)
        # Pack to the screen
        self.my_tree.pack()

        # Configure the scrollbar
        tree_scroll.config(command=self.my_tree.yview)

        # Define Our Columns
        self.my_tree['columns'] = ("N°", "Desc", "ValUnit", "Qtd", "ValTot")

        # Formate Our Columns
        self.my_tree.column("#0", width=0, stretch=NO)
        self.my_tree.column("N°", anchor=CENTER, width=40)
        self.my_tree.column("Desc", anchor=W, width=400)
        self.my_tree.column("ValUnit", anchor=W, width=150)
        self.my_tree.column("Qtd", anchor=CENTER, width=75)
        self.my_tree.column("ValTot", anchor=W, width=150)

        # Create Headings
        self.my_tree.heading("#0", text="", anchor=W)
        self.my_tree.heading("N°", text="N°", anchor=CENTER)
        self.my_tree.heading("Desc", text="Descrição", anchor=W)
        self.my_tree.heading("ValUnit", text="Val.Unit", anchor=CENTER)
        self.my_tree.heading("Qtd", text="Qtd", anchor=CENTER)
        self.my_tree.heading("ValTot", text="Val.Total", anchor=CENTER)

        for record in range(len(self.produtos)):
            self.my_tree.insert(
                parent='', index='end', text="", values=(record+1, (self.produtos[record])[0], f'R${(self.produtos[record])[1]:.2f}', (self.produtos[record])[2], f'R${(self.produtos[record])[3]:.2f}'))

        self.travel_tabel = 1

    def chamado_add(self, e):
        self.entrada_op = str(self.master.focus_get())
        print(self.entrada_op)
        if self.entrada_op == '.':
            self.enter_foc = self.enter_desc

        elif self.entrada_op == '.!entry10':
            self.enter_foc = self.enter_valUnit

        elif self.entrada_op == str(self.enter_valUnit):
            self.enter_foc = self.enter_Qtd

        elif self.entrada_op == str(self.enter_Qtd):
            self.enter_foc = self.enter_desc
            self.add_bbtc()

        self.enter_foc.focus_set()

    def voltar_entrada(self,e):
        self.entrada_op = str(self.master.focus_get())
        if '.!entry' in self.entrada_op:

            if self.entrada_op == '.!entry2':
                self.enter_foc = self.enter_desc

            elif self.entrada_op == '.!entry3':
                self.enter_foc = self.enter_valUnit

            if self.enter_foc:
                self.enter_foc.focus_set()

    def avancar_entrada(self,e):
        self.entrada_op = str(self.master.focus_get())
        if '.!entry' in self.entrada_op:

            if self.entrada_op == '.!entry':
                self.enter_foc = self.enter_valUnit

            elif self.entrada_op == '.!entry2':
                self.enter_foc = self.enter_Qtd

            if self.enter_foc:
                self.enter_foc.focus_set()

    def add_bbtc(self):

        #Inserindo Valores
        self.desc = (str(self.enter_desc.get())).upper()
        self.val_unit = str(self.enter_valUnit.get())
        if self.val_unit:
            if ',' in self.val_unit:
                self.val_unit = (self.val_unit).replace(',','.')

            if not self.val_unit[0].isalpha():
                self.val_unit = float(self.val_unit)


                self.qtd = self.enter_Qtd.get()
                if self.qtd:
                    self.qtd = int(self.enter_Qtd.get())
                    self.val_tot = self.val_unit * self.qtd

                    #Colocando os Valores dentro da Biblioteca
                    if self.qtd > 0 and self.desc and self.val_unit >= 0:
                        self.produtos.append([self.desc, self.val_unit, self.qtd, self.val_tot])

        


        #Quardando Valor Total
        self.valTot = 0
        for c in self.produtos:
            self.valTot += c[self.posi_valTot]

        #Inserido Vals Tot Qtd
        if self.travel_ValQtd:
            self.label_ValTot.destroy()
            self.label_TotServ.destroy()

        #Valor Mão de Obra
        self.maodeobra = self.enter_maodeobra.get()
        if ',' in self.maodeobra:
            self.maodeobra = (self.maodeobra).replace(',','.')
        if self.maodeobra == '':
            self.maodeobra = 0
        self.maodeobra = float(self.maodeobra)

        #Valor Desconto
        self.desconto = self.enter_desconto.get()
        if ',' in self.desconto:
            self.desconto = (self.desconto).replace(',','.')
        if self.desconto == '':
            self.desconto = 0
        self.desconto = float(self.desconto)

        #Inserindo Ordem de Serviço
        self.label_ValTot = tk.Label(self.master, text=f' Ordem de Serviço: {self.servico.ordem}  Data:', font=('Calibri', 20), fg='white', anchor='w', bg="#2f526b")
        self.label_ValTot.grid(row=1, rowspan=1, column=0,columnspan=3, pady=10, sticky='w')

        #Inserindo Total Peças
        valtot = ' Total Peças:R${:.2f}'.format(self.valTot)
        self.label_ValTot = tk.Label(self.master, text=valtot[:29], font=('Calibri', 26), bg='#99afbf', anchor='w')
        self.label_ValTot.grid(row=11, rowspan=1, column=0, columnspan=4, pady=0, sticky='w')

        #Inserindo Total Serviço
        valtots = f' Valor Total:R${((self.valTot + self.maodeobra)*(1-(self.desconto/100))):.2f}'
        self.label_TotServ = tk.Label(self.master, text=valtots[:31], font=('Calibri', 26), bg='#99afbf', anchor='w')
        self.label_TotServ.grid(row=12, rowspan=1, column=0, columnspan=4, pady=0, sticky='w')

        self.travel_ValQtd = 1

        # Limpando Entradas
        self.clean_ent()

        #Colocando Tabela
        self.tabel()

    def salvar_pdf(self):
        if self.valTot >= 0:
            
            nome_nota = (filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")], initialfile=save_data(self))).upper()
            if nome_nota:
                criar_nota(self, nome_nota, self.servico, self.valTot, self.desconto)

    def chamado_save_data(self):
        save_data(self)

    def chamado_restart(self,e):
        self.restart()

    def restart(self):
        val = askokcancel("Deletar-Peças", "Deletar todas as peças do serviço?")
        if val:
            self.produtos = []
            self.add_bbtc()

            # Espaço
            for record in self.my_tree.get_children():
                self.my_tree.delete(record)

    def chamado_deletar(self,e):
        if '.!treeview' in str(self.master.focus_get()):
            self.deletar_prod()

    def deletar_prod(self):
        if self.values:
            self.clean_ent()
            self.prod = self.my_tree.selection()[0]
            self.my_tree.delete(self.prod)

            posi_values = self.produtos.index(self.values)
            self.produtos.pop(posi_values)

            self.add_bbtc()

    def select_record(self,e):
        # Clear entry boxes
        self.clean_ent()

        # Grab record number
        selected = self.my_tree.focus()
        # Grab record values
        self.values = self.my_tree.item(selected, 'values')
        if self.values:
            self.values = [self.values[1], self.values[2], self.values[3], self.values[4]]
            self.values[1] = float(str(self.values[1]).replace('R$',''))
            self.values[2] = int(self.values[2])
            self.values[3] = float(str(self.values[3]).replace('R$',''))

            # output to entry boxes
            self.enter_desc.insert(0, self.values[0])
            self.enter_valUnit.insert(0, self.values[1])
            self.enter_Qtd.insert(0, self.values[2])

            self.travel_selecao = 1

    def selecao(self,e):

        self.select_record('')
        if not self.values:
            # Já deixar um item selecionado
            list = self.my_tree.get_children()
            if list:
                self.my_tree.selection_set(list[0])
                self.my_tree.focus(list[0])
                self.my_tree.focus_force()

        self.select_record('')

    def travel_d(self,e):
        self.select_record('')

    def not_selec(self,e):
        self.my_tree.bind("<ButtonRelease-1>", self.travel_d)

        if self.travel_selecao and self.point_click == '':
            self.my_tree.selection_set()
            self.my_tree.focus()
            self.my_tree.focus_force()
            self.travel_selecao = ''
            self.point_click = ''
            self.clean_ent()

        self.point_click = ''

    def lista_ata(self,e):
        self.root_listAta = tk.Tk()
        self.root_listAta.title('Lista-de-Atalhos')

        #Lista
        self.atalhos = """Ctrl+Enter: Gerar Nota
Delete: Deletar Compra
Backspace: Deletar Produto
Enter: Adicionar Produto
Seta-Baixo e Cima: Selecionar Produto
Double_Shift: Tirar Seleção
Ctrl+-Direita e Esquerda: Selecionar Entrada"""

        #Inserindo Lista
        self.label_ata = tk.Label(master=self.root_listAta, text=self.atalhos, anchor=W)
        self.label_ata.pack()
    def insert_entrys(self):
        self.enter_ncliente.insert(0, self.servico.ncliente)
        self.enter_telefone.insert(0, self.servico.telefone)
        self.enter_placa.insert(0, self.servico.placa)
        self.enter_marca.insert(0, self.servico.marca)
        self.enter_modelo.insert(0, self.servico.modelo)
        self.enter_cor.insert(0, self.servico.cor)
        self.enter_ano.set(self.servico.ano)
        self.enter_kmatual.insert(0, self.servico.kmatual)
        self.my_text.insert('1.0', self.servico.observacoes)
        if self.servico.maodeobra:
            self.entry_var.set(self.servico.maodeobra)
        if self.servico.desconto:
            self.entry_desconto.set(self.servico.desconto)
    
    # Função de validação para a entrada de números
    def testVal(self, inStr, acttyp):
                if acttyp == '1':
                    if not inStr.isdigit():
                        return False
                return True
    
    def create_widgets(self):
        self.master.configure(bg="#2f526b")

        def addm(*args):
            mdo = self.entry_var.get()
            if not mdo:
                mdo = 0
            self.maodeobra = mdo
            self.add_bbtc()

        def addmd(*args):
            mdo = self.entry_desconto.get()
            if not mdo:
                mdo = 0
            self.desconto = mdo
            self.add_bbtc()

        def validar_numeros(char):
            # Permite apenas caracteres numéricos
            r = char.isdigit() or char == "" or char in ".,"
            return r
        self.validacao_numeros = self.register(validar_numeros)

        #Título
        self.label_titulo = tk.Label(self.master, text='AUTOMEC - MECÂNICA AUTOMOTIVA', font=('Calibri', 40), bg='#133449', anchor='w', fg='white')
        self.label_titulo.grid(row=0, column=0, columnspan=10, sticky='nswe')

        #Data de Hoje
        self.label_datahoje = tk.Label(self.master, text=f'Data: {self.data} ', font=('Calibri', 20),bg='#133449', anchor='e', width=16, fg='white')
        self.label_datahoje.grid(row=0, column=7, columnspan=10, sticky='nswe')

        #Lista Atalhos
        self.label_listaatalhos = tk.Label(self.master, text='Acessar Atalhos:Ctrl+Tab', bg='#133449', anchor='s', fg='white')
        self.label_listaatalhos.grid(row=0, column=8, columnspan=10, sticky='s')
        self.master.bind('<Control-Tab>', self.lista_ata)

        #Entry Data
        import locale
        locale.setlocale(locale.LC_ALL, 'pt_BR.utf8')
        self.enter_date = DateEntry(self.master, font=('Calibri', 20), width=9, bg='#DCDCDC', locale='pt_BR', state="readonly")
        self.enter_date.grid(row=1, column=2, columnspan=2, pady=0, sticky='e')
        self.enter_date.set_date(self.servico.data)

        #Texto Cliente
        self.label_ncliente = tk.Label(self.master, text=' Cliente:', font=('Calibri', 20), anchor='w', width=9)
        self.label_ncliente.grid(row=2, column=0, columnspan=4, sticky='w')

        #Entry Cliente
        self.enter_ncliente = tk.Entry(self.master, font=('Calibri', 20), width=30, bg='#DCDCDC')
        self.enter_ncliente.grid(row=2, column=0, columnspan=4, pady=0, sticky='e')

        #Texto Telefone
        self.label_telefone = tk.Label(self.master, text=' Telefone:', font=('Calibri', 20), anchor='w', width=8)
        self.label_telefone.grid(row=3, column=0, columnspan=4, sticky='w')

        #Entry Telefone
        self.enter_telefone = tk.Entry(self.master, font=('Calibri', 20), width=16, bg='#DCDCDC', validate="key")
        self.enter_telefone['validatecommand'] = (self.enter_telefone.register(self.testVal),'%P','%d')
        self.enter_telefone.grid(row=3, column=0, columnspan=4, pady=0, sticky='w', padx=112)

        #Texto Placa
        self.label_placa = tk.Label(self.master, text=' PLACA DO VEÍCULO:', font=('Calibri', 20), anchor='w')
        self.label_placa.grid(row=4, column=0, columnspan=2, sticky='w')

        
        def placaexists(*args):
            placa = self.enter_placa.get()
            nomes_arquivos = os.listdir("./JSON_db/")
            print(placa)
            for nome_arquivo in nomes_arquivos:
                if '.json' in nome_arquivo and nome_arquivo != 'orderserver.json':
                    with open("./JSON_db/" + nome_arquivo, "r") as arquivo_json:
                        datas_for_placa = json.load(arquivo_json)

                        if placa == "" or (placa == datas_for_placa['placa'] != ""): 
                            self.enter_ncliente.delete(0, 'end')
                            self.enter_telefone.delete(0, 'end')
                            self.enter_marca.delete(0, 'end')
                            self.enter_modelo.delete(0, 'end')
                            self.enter_cor.delete(0, 'end')
                            self.enter_ano.set('') 

                            if placa == datas_for_placa['placa'] != "":
                                self.enter_ncliente.insert(0, datas_for_placa['ncliente'])
                                self.enter_telefone.insert(0, datas_for_placa['telefone'])
                                self.enter_marca.insert(0, datas_for_placa['marca'])
                                self.enter_modelo.insert(0, datas_for_placa['modelo'])
                                self.enter_cor.insert(0, datas_for_placa['cor'])
                                self.enter_ano.set(datas_for_placa['ano'])       
                        

        #Entry Placa           
        self.enter_placa = tk.Entry(self.master, font=('Calibri', 20), width=20, bg='#DCDCDC', validatecommand=(self.validacao_numeros, "%S"))
        self.enter_placa.grid(row=4, column=1, columnspan=3, pady=0, sticky='e')

        #Texto Placa
        self.label_branco = tk.Label(self.master, text='         ', font=('Calibri', 20), anchor='e')
        self.label_branco.grid(row=4, column=0, columnspan=4, sticky='e')

        #Botão Search For Placa
        self.botao_searchplaca = tk.Button(self.master, text='🔍', font=('Calibri', 17), bg='#6a88b5', command=placaexists)
        self.botao_searchplaca.grid(row=4, rowspan=1, column=3, padx=10, sticky='e')

        #Texto Marca
        self.label_marca = tk.Label(self.master, text=' MARCA:', font=('Calibri', 20), anchor='w')
        self.label_marca.grid(row=5, column=0, columnspan=1, sticky='w')

        #Entry Marca
        self.enter_marca = tk.Entry(self.master, font=('Calibri', 20), width=8, bg='#DCDCDC')
        self.enter_marca.grid(row=6, column=0, columnspan=1, pady=0, sticky='w', padx=10)

        #Texto Modelo
        self.label_modelo = tk.Label(self.master, text='MODELO:', font=('Calibri', 20), anchor='w')
        self.label_modelo.grid(row=5, column=1, columnspan=1, sticky='w')

        #Entry Modelo
        self.enter_modelo = tk.Entry(self.master, font=('Calibri', 20), width=9, bg='#DCDCDC')
        self.enter_modelo.grid(row=6, column=1, columnspan=1, pady=0, sticky='w', padx=0)

        #Texto Cor
        self.label_cor = tk.Label(self.master, text=' COR:', font=('Calibri', 20), anchor='w')
        self.label_cor.grid(row=5, column=2, columnspan=1, sticky='w')

        #Entry Cor
        self.enter_cor = tk.Entry(self.master, font=('Calibri', 20), width=8, bg='#DCDCDC')
        self.enter_cor.grid(row=6, column=2, columnspan=1, pady=0, sticky='w', padx=10)

        #Texto Ano
        self.label_ano = tk.Label(self.master, text='ANO:', font=('Calibri', 20), anchor='w')
        self.label_ano.grid(row=5, column=3, columnspan=1, sticky='w')

        #Entry Ano
        anos = [str(ano) for ano in range(int(self.data[6:])+1, 1979, -1)]
        self.enter_ano = ttk.Combobox(self.master, font=('Calibri', 20), width=7, values=anos, state="readonly")
        self.enter_ano.grid(row=6, column=3, columnspan=1, pady=0, sticky='w', padx=0)
        ttk.Style().configure("TCombobox", fieldbackground="#DCDCDC")

        #Texto Km Atual
        self.label_kmatual = tk.Label(self.master, text=' Quilometragem:', font=('Calibri', 20), anchor='w')
        self.label_kmatual.grid(row=7, column=0, columnspan=4, sticky='w')

        #Entry Km Atual
        self.enter_kmatual = tk.Entry(self.master, font=('Calibri', 20), width=15, bg='#DCDCDC')
        self.enter_kmatual.grid(row=7, column=1, columnspan=2, sticky='e', pady=0, padx=0)

        #Texto Observacoes
        self.label_observacoes = tk.Label(self.master, text=' Observações Gerais:', font=('Calibri', 20), anchor='w')
        self.label_observacoes.grid(row=8, column=0, columnspan=4, sticky='w')

        #Entry Observacoes
        text_frame = Frame(self.master)
        text_frame.grid(row=9, column=0, columnspan=4, pady=0, sticky='e', padx=0)
        text_scroll = Scrollbar(text_frame)
        text_scroll.pack(side=RIGHT, fill=Y)
        self.my_text = tk.Text(text_frame, yscrollcommand=text_scroll.set, width=54, bg='#DCDCDC', font=(10), height=8)
        self.my_text.pack()
        text_scroll.config(command=self.my_text.yview)

        #Texto Mao de Obra
        self.label_maodeobra = tk.Label(self.master, text=' Mão de Obra: R$', font=('Calibri', 20), anchor='w')
        self.label_maodeobra.grid(row=10, column=0, columnspan=4, sticky='w')

        #Entry Mao de Obra
        self.entry_var = tk.StringVar()
        self.enter_maodeobra = tk.Entry(self.master, font=('Calibri', 20), width=10, bg='#DCDCDC', validate="key", validatecommand=(self.validacao_numeros, "%S"), textvariable=self.entry_var)
        self.enter_maodeobra.grid(row=10, column=1, columnspan=2, pady=5, padx=0)
        
        #Texto Desconto
        self.label_desconto = tk.Label(self.master, text='Desc:', font=('Calibri', 20), anchor='e')
        self.label_desconto.grid(row=10, column=2, columnspan=1, sticky='e')

        #Entry Desconto
        self.entry_desconto = tk.StringVar()
        self.enter_desconto = tk.Entry(self.master, font=('Calibri', 20), width=8, bg='#DCDCDC', validate="key", validatecommand=(self.validacao_numeros, "%S"), textvariable=self.entry_desconto)
        self.enter_desconto.grid(row=10, column=3, columnspan=1, pady=5, padx=0, sticky='e')

        #Texto Porcentagem
        self.label_porcentagem = tk.Label(self.master, text='%', font=('Calibri', 20), anchor='e')
        self.label_porcentagem.grid(row=10, column=3, columnspan=1, sticky='e')

        #Frame Botões
        but_frame = Frame(self.master, bg="#2f526b")
        but_frame.grid(row=1, rowspan=1, pady=0, padx=0, column=5, columnspan=5)

        #Botão Limpar
        self.botao_limpar = tk.Button(but_frame, text='Deletar Peças', font=('Calibri', 17), bg='red', command=self.restart)
        self.botao_limpar.grid(row=0, rowspan=1, pady=0, padx=0, column=0)
        self.master.bind('<Delete>', self.chamado_restart)

        #Botão Deletar Item
        self.botao_delprod = tk.Button(but_frame, text='Deletar Peça', font=('Calibri', 17), bg='red', command=self.deletar_prod)
        self.botao_delprod.grid(row=0, rowspan=1, pady=0, padx=40, column=1)
        self.master.bind('<BackSpace>', self.chamado_deletar)

        #Botão Salvar Dados
        self.botao_nota = tk.Button(but_frame, text='Salvar Dados', font=('Calibri', 17), bg='#6a88b5', command=self.chamado_save_data)
        self.botao_nota.grid(row=0, rowspan=1, column=2, pady=0 , padx=0)
        self.master.bind('<Control-Return>', self.chamado_save_data)

        #Botão Nota Fiscal
        self.botao_nota = tk.Button(but_frame, text='Gerar Nota', font=('Calibri', 17), bg='#6a88b5', command=self.salvar_pdf)
        self.botao_nota.grid(row=0, rowspan=1, column=3, pady=0 , padx=40)
        self.master.bind('<Control-Return>', self.salvar_pdf)

        #Espaço
        self.espaco = tk.Label(self.master, text=' ')
        self.espaco.grid(row=1, rowspan=10, column=4)

        #Espaço entry
        self.background = tk.Label(self.master, bg='#99afbf', font=('Calibri', 20), width=37, height=3)
        self.background.grid(row=11, column=0, columnspan=4, rowspan=2, sticky='sne')

        #Espaço entry
        self.background = tk.Label(self.master, bg='#b1b3b2', font=('Calibri', 20), width=59, height=3)
        self.background.grid(row=11, column=5, columnspan=5, rowspan=2, sticky='sn')

        #Descrição
        self.descricao_itm = tk.Label(self.master, text='Descrição', font=('Calibri', 20), bg='#b1b3b2', width=36, anchor='w')
        self.descricao_itm.grid(row=11, column=5, columnspan=2)

        self.enter_desc = tk.Entry(self.master, font=('Calibri', 20), width=36)
        self.enter_desc.grid(row=12, column=5, columnspan=2, padx=5)

        #Val.Unit
        self.valUnit_itm = tk.Label(self.master, text='Val.Unit', font=('Calibri', 20), bg='#b1b3b2', width=8)
        self.valUnit_itm.grid(row=11, column=7)

        self.real = tk.Label(self.master, text='R$', font=('Calibri', 19), bg='#b1b3b2')
        self.real.grid(row=12, column=7, sticky='w')

        self.enter_valUnit = tk.Entry(self.master, font=('Calibri', 20), width=6, validate="key", validatecommand=(self.validacao_numeros, "%S"))
        self.enter_valUnit.grid(row=12, column=7, sticky='e')

        #Qtd
        self.Qtd_itm = tk.Label(self.master, text='Qtd', font=('Calibri', 20), bg='#b1b3b2', width=5)
        self.Qtd_itm.grid(row=11, column=8)

        self.enter_Qtd = tk.Entry(self.master, font=('Calibri', 20), width=4, validate="key")
        self.enter_Qtd['validatecommand'] = (self.enter_Qtd.register(self.testVal),'%P','%d')
        self.enter_Qtd.grid(row=12, column=8)

        # Botão Adicionar Produto
        self.botao_addprod = tk.Button(self.master, text='Adicionar\nPeça', font=('Calibri', 15), command=self.add_bbtc)
        self.botao_addprod.grid(row=11, rowspan=2, column=9, pady=7)
        self.master.bind('<Return>', self.chamado_add)
        self.master.bind('<Control-Left>', self.voltar_entrada)
        self.master.bind('<Control-Right>', self.avancar_entrada)

        #Setas Selecionar
        self.master.bind('<Up>', self.selecao)
        self.master.bind('<Down>', self.selecao)

        self.master.bind("<ButtonRelease-1>", self.not_selec)
        self.master.bind('<Shift_L>', self.not_selec)

        for widget in self.master.winfo_children():
            if isinstance(widget, tk.Label):
                if widget.cget("bg") == "SystemButtonFace":
                    widget.config(bg="#2f526b", fg="white")

        self.entry_var.trace_add("write", addm)
        self.entry_desconto.trace_add("write", addmd)

        self.insert_entrys()
