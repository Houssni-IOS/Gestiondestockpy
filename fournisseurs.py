from cgitb import text
import imp
from logging import root
import string
from tkinter import *
from tkinter.font import BOLD
from turtle import title #Tool kit interface permettant la création d'interfaces graphiques
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk , messagebox
import sqlite3
class Fournisseur:
    def __init__(self,root) : #comme un constructeur
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Gestionnaire de Stock")
        self.root.config(bg="white")
        self.root.focus_force()

#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        #Variables
        self.var_rechercherPar=StringVar()
        self.var_rechercherTxt=StringVar()

        self.var_invoice=StringVar()
        self.var_four_nom=StringVar()
        self.var_four_contact=StringVar()
       

        #---self.root---
        #---Options---
        lbl_search=Label(self.root,text="Nr facture :",bg="white",font=("goudy old style",15))
        lbl_search.place(x=700,y=80)

        txt_recherche=Entry(self.root,textvariable=self.var_rechercherTxt,font=("goudy old style",15),bg="#F7EFDE").place(x=800,y=80,width=160)
        btn_recherch=Button(self.root,text="Rechercher",command=self.rechercher,font=("goudy old style",20,"bold"),bg="#517B67",fg="white",cursor="hand2").place(x=950,y=79,width=133,height=28)

        #---Title---

        title=Label(self.root,text="Détails du Fournisseur :",font=("goudy old style",15),bg="#3E9CB6",fg="white").place(x=50,y=10,width=1000,height=40)
        
        #---Content---

            #---Row1

        lbl_fourInvoice=Label(self.root,text="Facture :",font=("goudy old style",15),bg="white").place(x=50,y=80)
        txt_lbl_fourInvoice=Entry(self.root,textvariable=self.var_invoice,font=("goudy old style",15),bg="#F7EFDE").place(x=180,y=80,width=180)

            #---Row2

        lbl_fourNom=Label(self.root,text="Nom :",font=("goudy old style",15),bg="white").place(x=50,y=120)

        txt_fourNom=Entry(self.root,textvariable=self.var_four_nom,font=("goudy old style",15),bg="#F7EFDE").place(x=180,y=120,width=180)

            #---Row3

        lbl_fourContact=Label(self.root,text="Contact :",font=("goudy old style",15),bg="white").place(x=50,y=160)
        txt_fourContact=Entry(self.root,textvariable=self.var_four_contact,font=("goudy old style",15),bg="#F7EFDE").place(x=180,y=160,width=180)

            #---Row4

        lbl_desc=Label(self.root,text="Description :",font=("goudy old style",15),bg="white").place(x=50,y=200)
        self.txt_desc=Text(self.root,font=("goudy old style",15),bg="#F7EFDE")
        self.txt_desc.place(x=180,y=200,width=470,height=120)

        #---Buttons---

        btn_enregistrer=Button(self.root,text="Enregistrer",command=self.ajouter,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=180,y=370,width=110,height=35)
        btn_modifier=Button(self.root,text="Modifier",command=self.modifier,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=300,y=370,width=110,height=35)
        btn_supprimer=Button(self.root,text="Supprimer",command=self.supprimer,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=420,y=370,width=110,height=35)
        btn_effacer=Button(self.root,text="Effacer",command=self.effacer,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=540,y=370,width=110,height=35)


        #----Details du fournisseur---

        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=700,y=120,width=380,height=350)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.FourTable=ttk.Treeview(emp_frame,columns=("invoice","nom","contact","descriptionf"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.FourTable.xview)
        scrolly.config(command=self.FourTable.yview)

        self.FourTable.heading("invoice",text="Nr Facture")
        self.FourTable.heading("nom",text="Nom")
        self.FourTable.heading("contact",text="Contact")
        self.FourTable.heading("descriptionf",text="Description")
        self.FourTable["show"]="headings"

        self.FourTable.column("invoice",width=90)
        self.FourTable.column("nom",width=100)
        self.FourTable.column("contact",width=100)
        self.FourTable.column("descriptionf",width=100)
        self.FourTable.pack(fill=BOTH,expand=1)
        self.FourTable.bind("<ButtonRelease-1>",self.get_data)
        self.afficher()
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def ajouter(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_invoice.get()=="":
                messagebox.showerror("Error","Le numéro de facture doit être fournit!",parent=self.root)
            else:
                cur.execute("SELECT * FROM fournisseur where invoice=?",(self.var_invoice.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Le numéro de facture saisie éxiste déja , essayez un aute!",parent=self.root)
                else:
                    cur.execute("INSERT INTO fournisseur (invoice,nom,contact,descriptionf) VALUES(?,?,?,?)",(
                                        self.var_invoice.get(),
                                        self.var_four_nom.get(),
                                        self.var_four_contact.get(),
                                        self.txt_desc.get('1.0',END),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Fournisseur inséré avec succès.",parent=self.root)
                    self.afficher()
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}")

    def afficher(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM fournisseur")
            rows=cur.fetchall()
            self.FourTable.delete(*self.FourTable.get_children())
            for row in rows:
                self.FourTable.insert('',END,values=row)
                
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}")

    def get_data(self,ev):
        f=self.FourTable.focus()
        content=(self.FourTable.item(f))
        row=content['values']
        #print(row)
        self.var_invoice.set(row[0]),
        self.var_four_nom.set(row[1]),
        self.var_four_contact.set(row[2]),
        self.txt_desc.delete('1.0',END),
        self.txt_desc.insert(END,row[3]),
    def modifier(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_invoice.get()=="":
                messagebox.showerror("Error","Le numéro de facture doit être fournit!",parent=self.root)
            else:
                cur.execute("SELECT * FROM fournisseur where invoice=?",(self.var_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Le numéro de facture est invalid!",parent=self.root)
                else:
                    cur.execute("UPDATE fournisseur SET nom=?,contact=?,descriptionf=? WHERE invoice=?",(
                                        self.var_four_nom.get(),
                                        self.var_four_contact.get(),
                                        self.txt_desc.get('1.0',END),
                                        self.var_invoice.get(),

                    ))
                    con.commit()
                    messagebox.showinfo("Success","Fournisseur modifié avec succès.",parent=self.root)
                    self.afficher()
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}")
    
    def supprimer(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_invoice.get()=="":
                    messagebox.showerror("Error","Le numéro de facture doit être fournit!",parent=self.root)
            else:
                cur.execute("SELECT * FROM fournisseur where invoice=?",(self.var_invoice.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Le numéro de facture est invalid!",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Voulez-vous vraiment supprimer le fournisseur?",parent=self.root)
                    if op==True:

                        cur.execute("DELETE FROM fournisseur WHERE invoice=?",(self.var_invoice.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Fournisseur supprimé avec succès.")
                        self.effacer()
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}")

    def effacer(self):
        self.var_invoice.set(""),
        self.var_four_nom.set(""),
        self.var_four_contact.set(""),
        self.txt_desc.delete('1.0',END),
        self.var_rechercherTxt.set("")
        self.afficher()

    def rechercher(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_rechercherTxt.get()=="":
                messagebox.showerror("Error","Veuillez saisir le numéro de facture que vous voulez rechercher!",parent=self.root)
            else:
                cur.execute("SELECT * FROM fournisseur WHERE invoice=?",(self.var_rechercherTxt.get(),))
                row=cur.fetchone()
                if row!=None:
                    self.FourTable.delete(*self.FourTable.get_children())
                    self.FourTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","Aucun fournisseur trouvé!",parent=self.root )
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}")
if __name__=="__main__":
    root=Tk()
    obj=Fournisseur (root)
    root.mainloop()