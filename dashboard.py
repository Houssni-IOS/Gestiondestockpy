from logging import root
from tkinter import *
from turtle import title #Tool kit interface permettant la création d'interfaces graphiques
from PIL import Image,ImageTk #pip install pillow
from employees import Employee
from fournisseurs import Fournisseur
from category import Categori
from produits import Produits
from ventes import Vente
import sqlite3
from tkinter import messagebox
import os
import time
class Interface:
    def __init__(self,root) : #comme un constructeur
        self.root=root
        self.root.geometry("3000x830+0+0")
        self.root.title("Gestionnaire de Stock")
        self.root.config(bg="white")
        #---Title---
        self.icon_title=PhotoImage(file="Images/StockLogo.png")
        title=Label(self.root,text="Gestionnaire de Stock",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#2D7082",fg="white").place(x=0,y=0,relwidth=1,height=70)

        #---Lougout_Button---
        btn_logout=Button(self.root,text="Déconnexion",font=("times new roman",15,"bold"),bg="#F21B18",cursor="hand2").place(x=1200,y=40,height=30,width=150)

        #---Clock---
        self.label_clock=Label(self.root,text="Bienvenue dans le Gestionnaire de Stock \t\t Date: DD-MM-YYYY\t\t Heure: HH:MM:SS",font=("times new roman",15),bg="#3A494D",fg="white")
        self.label_clock.place(x=0,y=70,relwidth=1,height=30)

        #---Left_Menu
        self.MenuLogo=Image.open("Images/MenuLogo.png")
        self.MenuLogo=self.MenuLogo.resize((200,200),Image.ANTIALIAS)
        self.MenuLogo=ImageTk.PhotoImage(self.MenuLogo)

        Left_Menu=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Left_Menu.place(x=0,y=102,width=200,height=565)

        label_MenuLogo=Label(Left_Menu,image=self.MenuLogo)
        label_MenuLogo.pack(side=TOP,fill=X)

        self.icon_employe=PhotoImage(file="Images/employe.png")
        self.icon_fournisseur=PhotoImage(file="Images/fournisseur.png")
        self.icon_category=PhotoImage(file="Images/category.png")
        self.icon_products=PhotoImage(file="Images/products.png")
        self.icon_sales=PhotoImage(file="Images/sales.png")
        self.icon_exit=PhotoImage(file="Images/exit.png")


        label_Menu=Label(Left_Menu,text="Menu",font=("times new roman",20),bg="#519086").pack(side=TOP,fill=X)
        btn_employees=Button(Left_Menu,text="Employés",command=self.employees,image=self.icon_employe,compound=LEFT,padx=0,anchor="w",font=("times new roman",20,"bold"),bg="#BEDAD6",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_fournisseur=Button(Left_Menu,text="Fournisseurs",command=self.fournisseurs,image=self.icon_fournisseur,compound=LEFT,padx=0,anchor="w",font=("times new roman",20,"bold"),bg="#BEDAD6",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_category=Button(Left_Menu,text="Catégories",command=self.category,image=self.icon_category,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="#BEDAD6",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_products=Button(Left_Menu,text="Produits",command=self.produit,image=self.icon_products,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="#BEDAD6",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_sales=Button(Left_Menu,text="Ventes",command=self.ventes,image=self.icon_sales,compound=LEFT,padx=0,anchor="w",font=("times new roman",20,"bold"),bg="#BEDAD6",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        btn_exit=Button(Left_Menu,text="Quitter",image=self.icon_exit,compound=LEFT,padx=5,anchor="w",font=("times new roman",20,"bold"),bg="#BEDAD6",bd=3,cursor="hand2").pack(side=TOP,fill=X)
        
        #---Content---
        self.label_employees=Label(self.root,text="Employés\n[0]",bd=5,relief=RIDGE,bg="#BEDAD6",fg="Black",font=("goudy old style",20,"bold"))
        self.label_employees.place(x=400,y=200,height=150,width=300)

        self.label_fournisseur=Label(self.root,text="Fournisseurs\n[0]",bd=5,relief=RIDGE,bg="#D16052",fg="Black",font=("goudy old style",20,"bold"))
        self.label_fournisseur.place(x=750,y=200,height=150,width=300)

        self.label_category=Label(self.root,text="Catégories\n[0]",bd=5,relief=RIDGE,bg="#2D7082",fg="Black",font=("goudy old style",20,"bold"))
        self.label_category.place(x=1100,y=200,height=150,width=300)

        self.label_products=Label(self.root,text="Produits\n[0]",bd=5,relief=RIDGE,bg="#9F7527",fg="Black",font=("goudy old style",20,"bold"))
        self.label_products.place(x=550,y=380,height=150,width=300)

        self.label_sales=Label(self.root,text="Ventes\n[0]",bd=5,relief=RIDGE,bg="#B6A7A4",fg="Black",font=("goudy old style",20,"bold"))
        self.label_sales.place(x=900,y=380,height=150,width=300)

        #---Footer---
        label_footer=Label(self.root,text="Accueil du Gestionnaire de Stock | Réalisé par : BAKAROU Hajar - NAJALI Chaimae - DOUAIBI Houssni - ABENAY Khalid",font=("times new roman",15),bg="#3A494D",fg="white").pack(side=BOTTOM,fill=X)
        
        self.update_content()
#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def employees(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Employee(self.new_win)

    def fournisseurs(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Fournisseur(self.new_win)
    
    def category(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Categori(self.new_win)  

    def produit(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Produits(self.new_win)  

    def ventes(self):
        self.new_win=Toplevel(self.root)
        self.new_obj=Vente(self.new_win)
    
    def update_content(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("select * from Produits")
            Produits=cur.fetchall()
            self.label_products.config(text=f"Produits\n[ {str(len(Produits))}  ]")
            
            cur.execute("select * from Fournisseur")
            Fournisseur=cur.fetchall()
            self.label_fournisseur.config(text=f"Fournissur\n[ {str(len(Fournisseur))}  ]")
            
            cur.execute("select * from categorie")
            categorie=cur.fetchall()
            self.label_category.config(text=f"Catégorie\n[ {str(len(categorie))}  ]")
            
            cur.execute("select * from Employee")
            Employee=cur.fetchall()
            self.label_employees.config(text=f"Employée\n[ {str(len(Employee))}  ]")
            bill=str(len(os.listdir('bill')))
            self.label_sales.config(text=f'Total Sales[ {str(bill)}  ]')

            time_=time.strftime("%I:%M:%S")
            date_=time.strftime("%d-%m-%Y")
            self.label_clock.config(text=f"Bienvenue dans le Gestionnaire de Stock\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
            self.label_clock.after(200,self.update_content)
    



        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}")    
     

if __name__=="__main__":
    root=Tk()
    obj=Interface (root)
    root.mainloop()