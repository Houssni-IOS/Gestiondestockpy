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
class Employee:
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

        self.var_emp_id=StringVar()
        self.var_emp_genre=StringVar()
        self.var_emp_contact=StringVar()
        self.var_emp_nom=StringVar()
        self.var_emp_dateNaissance=StringVar()
        self.var_emp_dateEntree=StringVar()
        self.var_emp_email=StringVar()
        self.var_emp_mdp=StringVar()
        self.var_emp_type=StringVar()
        self.var_emp_salaire=StringVar()

        #---SearchFrame---

        SearchFrame=LabelFrame(self.root,text="Rechercher un employé :", font=("goudy old style",12,"bold"),bd=2,relief=RIDGE,bg="white")
        SearchFrame.place(x=250,y=20,width=600,height=70)

        #---Options---
        cmb_search=ttk.Combobox(SearchFrame,textvariable=self.var_rechercherPar,values=("Sélectionner :","ID","Nom","Contact","E-mail"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_search.place(x=10,y=10,width=180)
        cmb_search.current(0)

        txt_recherche=Entry(SearchFrame,textvariable=self.var_rechercherTxt,font=("goudy old style",15),bg="#F7EFDE").place(x=200,y=10)
        btn_recherch=Button(SearchFrame,text="Rechercher",command=self.rechercher,font=("goudy old style",15),bg="#517B67",fg="white",cursor="hand2").place(x=410,y=9,width=150,height=30)

        #---Title---

        title=Label(self.root,text="Détails de l'employé :",font=("goudy old style",15),bg="#3E9CB6",fg="white").place(x=50,y=100,width=1000)
        
        #---Content---

            #---Row1

        lbl_empId=Label(self.root,text="ID :",font=("goudy old style",15),bg="white").place(x=50,y=150)
        lbl_empGenre =Label(self.root,text="Genre :",font=("goudy old style",15),bg="white").place(x=400,y=150)
        lbl_empId=Label(self.root,text="Contact :",font=("goudy old style",15),bg="white").place(x=750,y=150)

        txt_empId=Entry(self.root,textvariable=self.var_emp_id,font=("goudy old style",15),bg="#F7EFDE").place(x=150,y=150,width=180)
        cmb_Genre=ttk.Combobox(self.root,textvariable=self.var_emp_genre,values=("Sélectionner :","Femme","Homme","Personnalisé"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_Genre.place(x=500,y=150,width=180)
        cmb_Genre.current(0)
        txt_empContact=Entry(self.root,textvariable=self.var_emp_contact,font=("goudy old style",15),bg="#F7EFDE").place(x=850,y=150,width=180)

            #---Row2

        lbl_empNom=Label(self.root,text="Nom :",font=("goudy old style",15),bg="white").place(x=50,y=190)
        lbl_empDateNaissance =Label(self.root,text="D.O.B :",font=("goudy old style",15),bg="white").place(x=400,y=190)
        lbl_empDateEntree=Label(self.root,text="D.O.J :",font=("goudy old style",15),bg="white").place(x=750,y=190)

        txt_empNom=Entry(self.root,textvariable=self.var_emp_nom,font=("goudy old style",15),bg="#F7EFDE").place(x=150,y=190,width=180)
        txt_empDateNaissance=Entry(self.root,textvariable=self.var_emp_dateNaissance,font=("goudy old style",15),bg="#F7EFDE").place(x=500,y=190,width=180)
        txt_empDateEntree=Entry(self.root,textvariable=self.var_emp_dateEntree,font=("goudy old style",15),bg="#F7EFDE").place(x=850,y=190,width=180)

            #---Row3

        lbl_empEmail=Label(self.root,text="E-mail :",font=("goudy old style",15),bg="white").place(x=50,y=230)
        lbl_empMdp =Label(self.root,text="P.W.D :",font=("goudy old style",15),bg="white").place(x=400,y=230)
        lbl_empType=Label(self.root,text="Type :",font=("goudy old style",15),bg="white").place(x=750,y=230)

        txt_empEmail=Entry(self.root,textvariable=self.var_emp_email,font=("goudy old style",15),bg="#F7EFDE").place(x=150,y=230,width=180)
        txt_empMdp=Entry(self.root,textvariable=self.var_emp_mdp,font=("goudy old style",15),bg="#F7EFDE").place(x=500,y=230,width=180)
        cmb_Type=ttk.Combobox(self.root,textvariable=self.var_emp_type,values=("Admin :","Employé"),state='readonly',justify=CENTER,font=("goudy old style",15))
        cmb_Type.place(x=850,y=230,width=180)
        cmb_Type.current(0)

            #---Row4

        lbl_empAddr=Label(self.root,text="Adresse :",font=("goudy old style",15),bg="white").place(x=50,y=270)
        lbl_empSalaire =Label(self.root,text="Salaire :",font=("goudy old style",15),bg="white").place(x=500,y=270)

        self.txt_empAddr=Text(self.root,font=("goudy old style",15),bg="#F7EFDE")
        self.txt_empAddr.place(x=150,y=270,width=300,height=60)
        txt_empSalaire=Entry(self.root,textvariable=self.var_emp_salaire,font=("goudy old style",15),bg="#F7EFDE").place(x=600,y=270,width=180)

        #---Buttons---

        btn_enregistrer=Button(self.root,text="Enregistrer",command=self.ajouter,font=("goudy old style",15),bg="#2196f3",fg="white",cursor="hand2").place(x=500,y=305,width=110,height=28)
        btn_modifier=Button(self.root,text="Modifier",command=self.modifier,font=("goudy old style",15),bg="#4caf50",fg="white",cursor="hand2").place(x=620,y=305,width=110,height=28)
        btn_supprimer=Button(self.root,text="Supprimer",command=self.supprimer,font=("goudy old style",15),bg="#f44336",fg="white",cursor="hand2").place(x=740,y=305,width=110,height=28)
        btn_effacer=Button(self.root,text="Effacer",command=self.effacer,font=("goudy old style",15),bg="#607d8b",fg="white",cursor="hand2").place(x=860,y=305,width=110,height=28)


        #----Details de l'employee---

        emp_frame=Frame(self.root,bd=3,relief=RIDGE)
        emp_frame.place(x=0,y=350,relwidth=1,height=150)

        scrolly=Scrollbar(emp_frame,orient=VERTICAL)
        scrollx=Scrollbar(emp_frame,orient=HORIZONTAL)

        self.EmployeeTable=ttk.Treeview(emp_frame,columns=("id","nom","email","genre","contact","dob","doj","pwd","utype","adresse","salaire"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.EmployeeTable.xview)
        scrolly.config(command=self.EmployeeTable.yview)

        self.EmployeeTable.heading("id",text="ID")
        self.EmployeeTable.heading("nom",text="Nom")
        self.EmployeeTable.heading("email",text="E-mail")
        self.EmployeeTable.heading("genre",text="Genre")
        self.EmployeeTable.heading("contact",text="Contact")
        self.EmployeeTable.heading("dob",text="D.O.B")
        self.EmployeeTable.heading("doj",text="D.O.J")
        self.EmployeeTable.heading("pwd",text="P.W.D")
        self.EmployeeTable.heading("utype",text="Type")
        self.EmployeeTable.heading("adresse",text="Adresse")
        self.EmployeeTable.heading("salaire",text="Salaire")

        self.EmployeeTable["show"]="headings"

        self.EmployeeTable.column("id",width=90)
        self.EmployeeTable.column("nom",width=100)
        self.EmployeeTable.column("email",width=100)
        self.EmployeeTable.column("genre",width=100)
        self.EmployeeTable.column("contact",width=100)
        self.EmployeeTable.column("dob",width=100)
        self.EmployeeTable.column("doj",width=100)
        self.EmployeeTable.column("pwd",width=100)
        self.EmployeeTable.column("utype",width=100)
        self.EmployeeTable.column("adresse",width=100)
        self.EmployeeTable.column("salaire",width=100)
        self.EmployeeTable.pack(fill=BOTH,expand=1)
        self.EmployeeTable.bind("<ButtonRelease-1>",self.get_data)
        self.afficher()
#-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    def ajouter(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","L'Id de l'employé doit être fournit!",parent=self.root)
            else:
                cur.execute("SELECT * FROM employee where id=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","L'ID de l'employé saisie éxiste déja , essayez une aute!",parent=self.root)
                else:
                    cur.execute("INSERT INTO employee (id,nom,email,genre,contact,dob,doj,pwd,utype,adresse,salaire) VALUES(?,?,?,?,?,?,?,?,?,?,?)",(
                                        self.var_emp_id.get(),
                                        self.var_emp_nom.get(),
                                        self.var_emp_email.get(),
                                        self.var_emp_genre.get(),
                                        self.var_emp_contact.get(),
                                        self.var_emp_dateNaissance.get(),
                                        self.var_emp_dateEntree.get(),
                                        self.var_emp_mdp.get(),
                                        self.var_emp_type.get(),
                                        self.txt_empAddr.get('1.0',END),
                                        self.var_emp_salaire.get(),
                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employé inséré avec succès.",parent=self.root)
                    self.afficher()
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}")

    def afficher(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM employee")
            rows=cur.fetchall()
            self.EmployeeTable.delete(*self.EmployeeTable.get_children())
            for row in rows:
                self.EmployeeTable.insert('',END,values=row)
                
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}")

    def get_data(self,ev):
        f=self.EmployeeTable.focus()
        content=(self.EmployeeTable.item(f))
        row=content['values']
        #print(row)
        self.var_emp_id.set(row[0]),
        self.var_emp_nom.set(row[1]),
        self.var_emp_email.set(row[2]),
        self.var_emp_genre.set(row[3]),
        self.var_emp_contact.set(row[4]),
        self.var_emp_dateNaissance.set(row[5]),
        self.var_emp_dateEntree.set(row[6]),
        self.var_emp_mdp.set(row[7]),
        self.var_emp_type.set(row[8]),
        self.txt_empAddr.delete('1.0',END),
        self.txt_empAddr.insert(END,row[9]),

        self.var_emp_salaire.set(row[10]),        

    def modifier(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                messagebox.showerror("Error","L'Id de l'employé doit être fournit!",parent=self.root)
            else:
                cur.execute("SELECT * FROM employee where id=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","L'ID de l'employé est invalid!",parent=self.root)
                else:
                    cur.execute("UPDATE employee SET nom=?,email=?,genre=?,contact=?,dob=?,doj=?,pwd=?,utype=?,adresse=?,salaire=? WHERE id=?",(
                                        self.var_emp_nom.get(),
                                        self.var_emp_email.get(),
                                        self.var_emp_genre.get(),
                                        self.var_emp_contact.get(),
                                        self.var_emp_dateNaissance.get(),
                                        self.var_emp_dateEntree.get(),
                                        self.var_emp_mdp.get(),
                                        self.var_emp_type.get(),
                                        self.txt_empAddr.get('1.0',END),
                                        self.var_emp_salaire.get(),
                                                                                self.var_emp_id.get(),

                    ))
                    con.commit()
                    messagebox.showinfo("Success","Employé modifié avec succès.",parent=self.root)
                    self.afficher()
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}")
    
    def supprimer(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_emp_id.get()=="":
                    messagebox.showerror("Error","L'Id de l'employé doit être fournit!",parent=self.root)
            else:
                cur.execute("SELECT * FROM employee where id=?",(self.var_emp_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","L'ID de l'employé est invalid!",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Voulez-vous vraiment supprimer l'employé?",parent=self.root)
                    if op==True:

                        cur.execute("DELETE FROM employee WHERE id=?",(self.var_emp_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","Employé supprimé avec succès.")
                        self.effacer()
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}")

    def effacer(self):
        self.var_emp_id.set(""),
        self.var_emp_nom.set(""),
        self.var_emp_email.set(""),
        self.var_emp_genre.set("Sélectionner"),
        self.var_emp_contact.set(""),
        self.var_emp_dateNaissance.set(""),
        self.var_emp_dateEntree.set(""),
        self.var_emp_mdp.set(""),
        self.var_emp_type.set("Admin"),
        self.txt_empAddr.delete('1.0',END),
        self.var_emp_salaire.set(""), 
        self.var_rechercherTxt.set("")
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
                cur.execute("SELECT * FROM employee WHERE "+self.var_rechercherPar.get()+" LIKE '%"+self.var_rechercherTxt.get()+"%'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.EmployeeTable.delete(*self.EmployeeTable.get_children())
                    for row in rows:
                        self.EmployeeTable.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","Aucun employé trouvé!",parent=self.root )
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}")
if __name__=="__main__":
    root=Tk()
    obj=Employee (root)
    root.mainloop()