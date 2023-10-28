from cgitb import text
import imp
from importlib.resources import contents
from logging import root
import string
from tkinter import *
from tkinter.font import BOLD
from turtle import title #Tool kit interface permettant la création d'interfaces graphiques
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
class Produits:
    def __init__(self,root) : #comme un constructeur
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Gestionnaire de Stock")
        self.root.config(bg="white")
        self.root.focus_force()
        #====================================
        self.var_rechercherPar=StringVar()
        self.var_rechercherTxt=StringVar()
        self.var_id=StringVar()
        self.cat_liste=[]
        self.fou_liste=[]
        self.fetch_cat_fou()
        self.var_cat=StringVar()
        self.var_fou=StringVar()

        self.var_name=StringVar()
        self.var_prix=StringVar()
        self.var_quantite=StringVar()
        self.var_status=StringVar()
        Produits_Frame=Frame(self.root,bd=3,relief=RIDGE,bg="white")
        Produits_Frame.place(x=10,y=10,width=450,height=480)

        #---column1---

        title=Label(Produits_Frame,text="Détails de Produits :",font=("goudy old style",18),bg="#3E9CB6",fg="white").pack(side=TOP,fill=X)

        lbl_categories=Label(Produits_Frame,text="categories :",font=("goudy old style",18),bg="white").place(x=30,y=60)
        lbl_fournisseurs=Label(Produits_Frame,text="fournisseurs :",font=("goudy old style",18),bg="white").place(x=30,y=110)
        lbl_name=Label(Produits_Frame,text="name :",font=("goudy old style",18),bg="white").place(x=30,y=160)
        lbl_prix=Label(Produits_Frame,text="prix :",font=("goudy old style",18),bg="white").place(x=30,y=210)
        lbl_Quantite=Label(Produits_Frame,text="Quantite :",font=("goudy old style",18),bg="white").place(x=30,y=260)
        lbl_status=Label(Produits_Frame,text="status :",font=("goudy old style",18),bg="white").place(x=30,y=310)


        #txt_categories=Label(Produits_Frame,text="categories :",font=("goudy old style",18),bg="white").place(x=30,y=60)
         #---column2---
        cmb_cat=ttk.Combobox(Produits_Frame,textvariable=self.var_cat,values=self.cat_liste,state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_cat.place(x=150,y=60,width=200)
        cmb_cat.current(0)


        cmb_fou=ttk.Combobox(Produits_Frame,textvariable=self.var_fou,values=self.fou_liste,state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_fou.place(x=150,y=110,width=200)
        cmb_fou.current(0)

        txt_name=Entry(Produits_Frame,textvariable=self.var_name,font=("goudy old style",15),bg='lightyellow').place(x=150,y=160,width=200)
        txt_prix=Entry(Produits_Frame,textvariable=self.var_prix,font=("goudy old style",15),bg='lightyellow').place(x=150,y=210,width=200)
        txt_quantite=Entry(Produits_Frame,textvariable=self.var_quantite,font=("goudy old style",15),bg='lightyellow').place(x=150,y=260,width=200)

        cmb_status=ttk.Combobox(Produits_Frame,textvariable=self.var_status,values=("Active","Inactive"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_status.place(x=150,y=310,width=200)
        cmb_status.current(0)
        #---Buttons---

        btn_enregistrer=Button(Produits_Frame,text="Enregistrer",command=self.ajouter,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=10,y=400,width=100,height=40)
        btn_modifier=Button(Produits_Frame,text="Modifier",command=self.modifier,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=120,y=400,width=100,height=40)
        btn_supprimer=Button(Produits_Frame,text="Supprimer",command=self.supprimer,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=230,y=400,width=100,height=40)
        btn_effacer=Button(Produits_Frame,text="Effacer",command=self.effacer,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=340,y=400,width=100,height=40)

         #---SearchFrame---

        SearchFrame=LabelFrame(self.root,text="Rechercher un employé :", font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=480,y=10,width=600,height=80)

        #---Options---
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_rechercherPar,values=("Sélectionner :","categories","fournisseurs","Name"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_recherche=Entry(SearchFrame,textvariable=self.var_rechercherTxt,font=("goudy old style",15),bg="#F7EFDE").place(x=200,y=10)
        btn_recherch=Button(SearchFrame,text="Rechercher",command=self.rechercher,font=("goudy old style",15),bg="#517B67",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)

         #----Details de produits---

        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=480,y=100,width=600,height=390)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.Produits_Table=ttk.Treeview(emp_frame,columns=("id","fournisseurs","categories","Name","Prix","Quantite","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.Produits_Table.xview)
        scrolly.config(command=self.Produits_Table.yview)

        self.Produits_Table.heading("id",text="ID")
        self.Produits_Table.heading("categories",text="Categories")
        self.Produits_Table.heading("fournisseurs",text="Fournisseurs")
        self.Produits_Table.heading("Name",text="Name")
        self.Produits_Table.heading("Prix",text="Prix")
        self.Produits_Table.heading("Quantite",text="Quantite")
        self.Produits_Table.heading("status",text="Status")

        self.Produits_Table["show"]="headings"

        self.Produits_Table.column("id",width=90)
        self.Produits_Table.column("categories",width=100)
        self.Produits_Table.column("fournisseurs",width=100)
        self.Produits_Table.column("Name",width=100)
        self.Produits_Table.column("Prix",width=100)
        self.Produits_Table.column("Quantite",width=100)
        self.Produits_Table.column("status",width=100)
        self.Produits_Table.pack(fill=BOTH,expand=1)
        self.Produits_Table.bind("<ButtonRelease-1>",self.get_data)
        self.afficher()
        


        #==========================================================

    def fetch_cat_fou(self):
        self.cat_liste.append("Empty")
        self.fou_liste.append("Empty")
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT nom FROM categorie")
            cat=cur.fetchall()
            if len(cat)>0:
                del self.cat_liste[:]
                self.cat_liste.append("Sélectionner")
                for i in cat:
                     self.cat_liste.append(i[0])

            cur.execute("SELECT nom FROM fournisseur")
            fou=cur.fetchall()
            if len(fou)>0:
                del self.fou_liste[:]
                self.fou_liste.append("Sélectionner")
                for i in fou:
                     self.fou_liste.append(i[0])
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}")


    def ajouter(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat.get()=="Sélectionner" or self.var_cat.get()=="Empty" or self.var_fou.get()=="Sélectionner" or self.var_name.get()=="":
                messagebox.showerror("Error","veuillez remplire tous les champs",parent=self.root)
            else:
                cur.execute("SELECT * FROM produits where name=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","L'ID de l'employé saisie éxiste déja , essayez une autre!",parent=self.root)
                else:
                    cur.execute("INSERT INTO produits (categories,fournisseurs,Name,Prix,Quantite,status) VALUES(?,?,?,?,?,?)",(
                                        self.var_cat.get(),
                                        self.var_fou.get(),
                                        self.var_name.get(),
                                        self.var_prix.get(),
                                        self.var_quantite.get(),
                                        self.var_status.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Produits inséré avec succès.",parent=self.root)
                    self.afficher()
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}")

    def afficher(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM produits")
            rows=cur.fetchall()
            self.Produits_Table.delete(*self.Produits_Table.get_children())
            for row in rows:
                self.Produits_Table.insert('',END,values=row)
                
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}")

    def get_data(self,ev):
        f=self.Produits_Table.focus()
        content=(self.Produits_Table.item(f))
        row=content['values']
        self.var_id.set(row[0])
        self.var_cat.set(row[1])
        self.var_fou.set(row[2])
        self.var_name.set(row[3])
        self.var_prix.set(row[4])
        self.var_quantite.set(row[5])
        self.var_status.set(row[6])     

    def modifier(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_id.get()=="":
                messagebox.showerror("Error","SVP Select produits from liste",parent=self.root)
            else:
                cur.execute("SELECT * FROM produits where id=?",(self.var_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","invalid produits ",parent=self.root)
                else:
                    cur.execute("UPDATE produits SET categories=?,fournisseurs=?,name=?,prix=?,quantite=?,status=? WHERE id=?",(
                                        self.var_cat.get(),
                                        self.var_fou.get(),
                                        self.var_name.get(),
                                        self.var_prix.get(),
                                        self.var_quantite.get(),
                                        self.var_status.get(),
                                        self.var_id.get(),
                   
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Produits modifié avec succès.",parent=self.root)
                    self.afficher()
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}")
    
    def supprimer(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_id.get()=="":
                    messagebox.showerror("Error","Select produits from the liste",parent=self.root)
            else:
                cur.execute("SELECT * FROM produits where id=?",(self.var_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","invalid produit",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Voulez-vous vraiment supprimer l'employé?",parent=self.root)
                    if op==True:

                        cur.execute("DELETE FROM produits WHERE id=?",(self.var_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Produits supprimé avec succès.",parent=self.root)
                        self.effacer()
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}")

    def effacer(self):
       self.var_cat.set("Select"),
       self.var_fou.set("Select"),
       self.var_name.set(""),
       self.var_prix.set(""),
       self.var_quantite.set(""),
       self.var_status.set("Active"),
       self.var_id.set(""),
       self.var_rechercherTxt.set(""),
       self.var_rechercherPar.set("Sélectionner"),
       self.afficher()

    def rechercher(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_rechercherPar.get()=="Sélectionner :":
                messagebox.showerror("Error","Veuillez sélectionner l'option par laquelle vous voulez rechercher!",parent=self.root)
            elif self.var_rechercherTxt.get()=="":
                messagebox.showerror("Error","Veuillez saisir la valeur que vous voulez rechercher!",parent=self.root)
            else:
                cur.execute("SELECT * FROM produits WHERE "+self.var_rechercherPar.get()+" LIKE '%"+self.var_rechercherTxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.Produits_Table.delete(*self.Produits_Table.get_children())
                    for row in rows:
                        self.Produits_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","Aucun employé trouvé!",parent=self.root )
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}")



if __name__=="__main__":
    root=Tk()
    obj=Produits (root)
    root.mainloop()