from cgitb import text
import imp
from logging import root
from operator import index
import string
from tkinter import *
from tkinter.font import BOLD
from turtle import title
from unicodedata import category #Tool kit interface permettant la création d'interfaces graphiques
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk , messagebox
import sqlite3
import os
class Vente:
    def __init__(self,root) : #comme un constructeur
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Gestionnaire de Stock")
        self.root.config(bg="white")
        self.root.focus_force()

        self.bill_list=[]
        self.var_invoice=StringVar()
    #---Title---
        lbl_title=Label(self.root,text="Voir facture client :",font=("goudy old style",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)

        lbl_invoice=Label(self.root,text="Num Facture :",font=("times new roman",15),bg="white").place(x=50,y=100)

        txt_invoice=Entry(self.root,textvariable=self.var_invoice,font=("times new roman",15),bg="#F7EFDE").place(x=170,y=100,width=180,height=28)

        btn_rechercher=Button(self.root,text="Rechercher",command=self.rechercher,font=("times new roman",15,"bold"),bg="#2196f3",fg="white",cursor="hand2").place(x=360,y=100,width=120,height=28)
        btn_effacer=Button(self.root,text="Effacer",command=self.effacer,font=("times new roman",15,"bold"),bg="#607d8b",cursor="hand2").place(x=490,y=100,width=120,height=28)
    #---Bill Liste---
        ventes_Frame=Frame(self.root,bd=3,relief=RIDGE)
        ventes_Frame.place(x=50,y=140,width=200,height=330)
        
        scrolly=Scrollbar(ventes_Frame,orient=VERTICAL)
        self.ventes_Liste=Listbox(ventes_Frame,font=("goudy old style",15),bg="white",yscrollcommand=scrolly.set)
        scrolly.pack(side=RIGHT,fill=Y)
        scrolly.config(command=self.ventes_Liste.yview)
        self.ventes_Liste.pack(fill=BOTH,expand=1)
        self.ventes_Liste.bind("<ButtonRelease-1>",self.get_data)

    #---Bill Area---
        bill_Frame=Frame(self.root,bd=3,relief=RIDGE)
        bill_Frame.place(x=280,y=140,width=410,height=330)

        lbl_title2=Label(bill_Frame,text="Zone de facture client :",font=("goudy old style",20),bg="#E75A23",fg="white").pack(side=TOP,fill=X)


        scrolly2=Scrollbar(bill_Frame,orient=VERTICAL)
        self.bill_area=Text(bill_Frame,bg="#F7EFDE",yscrollcommand=scrolly2.set)
        scrolly2.pack(side=RIGHT,fill=Y)
        scrolly2.config(command=self.ventes_Liste.yview)
        self.bill_area.pack(fill=BOTH,expand=1)

    #---Images---

        self.bill_image=Image.open("Images/ventes.png")
        self.bill_image=self.bill_image.resize((450,300),Image.ANTIALIAS)
        self.bill_image=ImageTk.PhotoImage(self.bill_image)

        lbl_image=Label(self.root,image=self.bill_image,bd=0,bg="white")
        lbl_image.place(x=690,y=110)

        self.afficher()
#------------------------------------------------------------------------------------------------------   
    def afficher(self):
        del self.bill_list[:]
        self.ventes_Liste.delete(0,END)
        #print(os.listdir('../PROJET PYTHON')) bill1.txt, category.py
        for i in os.listdir('bill'):
            #print(i.split('.'),i.split('.')[-1])
            if i.split('.')[-1]=='txt':
                self.ventes_Liste.insert(END,i)
                self.bill_list.append(i.split('.')[0])

    def get_data(self,ev):
        index_=self.ventes_Liste.curselection()
        file_name=self.ventes_Liste.get(index_)
        #print(file_name)
        self.bill_area.delete('1.0',END) 
        fp=open(f'bill/{file_name}','r')
        for i in fp:
            self.bill_area.insert(END,i)
        fp.close()

    def rechercher(self):
        if self.var_invoice.get()=="":
            messagebox.showerror("Error","Le numéro de facture doit  être saisi!",parent=self.root)
        else:
            if self.var_invoice.get() in self.bill_list:
                print("Numéro de facture trouvé.")
                fp=open(f'bill/{self.var_invoice.get()}.txt','r')
                self.bill_area.delete('1.0',END)
                for i in fp:
                    self.bill_area.insert(END,i)
                fp.close()
            else:
                messagebox.showerror("Error","Le numéro de facture est invalid !",parent=self.root)

    def effacer(self):
        self.afficher()
        self.bill_area.delete('1.0',END)
if __name__=="__main__":
    root=Tk()
    obj=Vente (root)
    root.mainloop()