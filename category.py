from cProfile import label
from tkinter import *
from tkinter.font import BOLD
from turtle import bgcolor, title #Tool kit interface permettant la création d'interfaces graphiques
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk , messagebox
import sqlite3
class Categori:
    def __init__(self,root) : #comme un constructeur
        self.root=root
        self.root.geometry("1100x500+220+130")
        self.root.title("Gestionnaire de Stock")
        self.root.config(bg="white")
        self.root.focus_force()
        self.var_cat_id=StringVar()
        self.var_name=StringVar()
        lbl_title=Label(self.root,text="Gestion des Catégorie des produits ",font=("goudy old style",30),bg="#184a45",fg="white",bd=3,relief=RIDGE).pack(side=TOP,fill=X,padx=10,pady=20)
        lbl_name=Label(self.root,text="Entrer le nom de la Catégorie ",font=("goudy old style",30),bg="white").place(x=50,y=100)
        txt_name=Entry(self.root,textvariable=self.var_name,font=("goudy old style",18),bg="lightyellow").place(x=50,y=170,width=300)
        btn_add=Button(self.root,text="Ajouter",command=self.ajouter,font=("goudy old style",15),bg="#4caf50",fg='white',cursor="hand2").place(x=360,y=170,width=150,height=30)
        btn_delete=Button(self.root,text="Supprimer",command=self.supprimer,font=("goudy old style",15),bg="red",fg='white',cursor="hand2").place(x=520,y=170,width=150,height=30)
        
 #----Details de catégori---

        cat_frame=Frame(self.root,bd=3,relief=RIDGE)
        cat_frame.place(x=700,y=100,width=380,height=100)

        scrolly=Scrollbar(cat_frame,orient=VERTICAL)
        scrollx=Scrollbar(cat_frame,orient=HORIZONTAL)

        self.CatTable=ttk.Treeview(cat_frame,columns=("cid","nom",),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CatTable.xview)
        scrolly.config(command=self.CatTable.yview)

        self.CatTable.heading("cid",text="C ID")
        self.CatTable.heading("nom",text="Nom")
        self.CatTable["show"]="headings"

        self.CatTable.column("cid",width=90)
        self.CatTable.column("nom",width=100)
        self.CatTable.pack(fill=BOTH,expand=1)
        self.CatTable.bind("<ButtonRelease-1>",self.get_data)

        self.im1=Image.open("Images/1cate.png")
        self.iml=self.im1.resize((500,200),Image.ANTIALIAS)
        self.iml=ImageTk.PhotoImage(self.iml)
        self.lbl_im1=Label(self.root,image=self.iml,bd=2,relief=RAISED)
        self.lbl_im1.place(x=50,y=220)
       
        self.im2=Image.open("Images/2cat.png")
        self.im2=self.im2.resize((500,200),Image.ANTIALIAS)
        self.im2=ImageTk.PhotoImage(self.im2)
        self.lbl_im2=Label(self.root,image=self.im2,bd=2,relief=RAISED,bg="white")
        self.lbl_im2.place(x=580,y=220)
        

        self.afficher()

    def ajouter(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_name.get()=="":
                messagebox.showerror("Error","Le nom de la catégorie doit être fournit!",parent=self.root)
            else:
                cur.execute("SELECT * FROM categorie where nom=?",(self.var_name.get(),))
                row=cur.fetchone()
                if row!=None:
                    messagebox.showerror("Error","Catégorie éxiste déja , essayez un aute!",parent=self.root)
                else:
                    cur.execute("INSERT INTO categorie (nom) VALUES(?)",(self.var_name.get(),))
                    con.commit()
                    messagebox.showinfo("Success","Catégorie inséré avec succès.",parent=self.root)
                    self.afficher()
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}",parent=self.root)



    def afficher(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT * FROM categorie")
            rows=cur.fetchall()
            self.CatTable.delete(*self.CatTable.get_children())
            for row in rows:
                self.CatTable.insert('',END,values=row)
                
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}") 

    def get_data(self,ev):
        f=self.CatTable.focus()
        content=(self.CatTable.item(f))
        row=content['values']
        #print(row)
        self.var_cat_id.set(row[0]),
        self.var_name.set(row[1]),                  
       

    def supprimer(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_cat_id.get()=="":
                    messagebox.showerror("Error","Veuillez selectionner la  catégorie",parent=self.root)
            else:
                cur.execute("SELECT * FROM categorie where cid=?",(self.var_cat_id.get(),))
                row=cur.fetchone()
                if row==None:
                    messagebox.showerror("Error","Erreur , Veuillez essayer ultérieurement !",parent=self.root)
                else:
                    op=messagebox.askyesno("Confirm","Voulez-vous vraiment supprimer ?",parent=self.root)
                    if op==True:

                        cur.execute("DELETE FROM categorie WHERE cid=?",(self.var_cat_id.get(),))
                        con.commit()
                        messagebox.showinfo("Delete","catégorie supprimé avec succès.")
                        self.afficher()
                        self.var_cat_id.set("")
                        self.var_name.set("")  
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}")

if __name__=="__main__": 
    root=Tk()
    obj=Categori (root)
    root.mainloop()