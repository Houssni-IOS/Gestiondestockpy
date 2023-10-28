from cProfile import label
from cgitb import text
from itertools import product
from tkinter import *
#from typing_extensions import Self
from unittest import result
from PIL import Image,ImageTk #pip install pillow
from tkinter import ttk,messagebox
import sqlite3
import time
import os
import tempfile
class BillClass:
    def __init__(self,root) : #comme un constructeur
        self.root=root
        self.root.geometry("1350x700+0+0")
        self.root.title("Gestionnaire de Stock")
        self.root.config(bg="white")
        self.cart_list=[]
        self.chk_print=0
        #---Title---
        self.icon_title=PhotoImage(file="Images/StockLogo.png")
        title=Label(self.root,text="Gestionnaire de Stock",image=self.icon_title,compound=LEFT,font=("times new roman",40,"bold"),bg="#2D7082",fg="white").place(x=0,y=0,relwidth=1,height=70)

        #---Lougout_Button---
        btn_logout=Button(self.root,text="Quitté",font=("times new roman",15,"bold"),bg="yellow",cursor="hand2").place(x=1200,y=40,height=30,width=150)

        #---Clock---
        self.label_clock=Label(self.root,text="Bienvenue dans le Gestionnaire de Stock \t\t Date: DD-MM-YYYY\t\t Heure: HH:MM:SS",font=("times new roman",15),bg="#3A494D",fg="white")
        self.label_clock.place(x=0,y=70,relwidth=1,height=30)
        #====Product_frame
        
        ProductFrame1=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        ProductFrame1.place(x=6,y=110,width=410,height=550)

        pTitle=Label(ProductFrame1,text="Tous les produits",font=("goudy old style",20,"bold"),bg="#262626",fg="white").pack(side=TOP,fill=X)

         #=====Product Search frame==========
        self.var_search=StringVar()
        ProductFrame2=Frame(ProductFrame1,bd=2,relief=RIDGE,bg="white")
        ProductFrame2.place(x=2,y=42,width=398,height=90)

        #lbl_search=Label(ProductFrame2,text="Rechercher un Produit | Par Nom",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5)

        lbl_search=Label(ProductFrame2,text="Rechercher par nom du produit ",font=("times new roman",15,"bold"),bg="white",fg="green").place(x=2,y=5) 
        
        lbl_Name=Label(ProductFrame2,text="Nom produit ",font=("times new roman",15,"bold"),bg="white").place(x=2,y=45)
        
        txt_search=Entry(ProductFrame2,textvariable=self.var_search,font=("times new roman",15),bg="lightyellow").place(x=128 ,y=47,width=150,height=22)
        btn_search=Button(ProductFrame2,text="Search",command=self.rechercher,font=("goudy old style",15),bg="#2196F3",fg="white",cursor="hand2").place(x=275 ,y=47,width=140,height=25) 
        btn_show_all=Button(ProductFrame2,text="Afficher",command=self.afficher,font=("goudy old style",15),bg="#083531",fg="white",cursor="hand2").place(x=275,y=10,width=140,height=25)

        #=======Product Details Frame========= 
        ProductFrame3=Frame(ProductFrame1,bd=3,relief=RIDGE,bg="white")
        ProductFrame3.place(x=2,y=140,width=398,height=375)

        scrolly=Scrollbar(ProductFrame3,orient=VERTICAL)
        scrollx=Scrollbar(ProductFrame3,orient=HORIZONTAL)

        self.product_Table=ttk.Treeview(ProductFrame3,columns=("id","nom","prix","Quantite","status"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.product_Table.xview)
        scrolly.config(command=self.product_Table.yview)

        self.product_Table.heading("id",text="id")
        self.product_Table.heading("nom",text="Nom")
        self.product_Table.heading("prix",text="prix")
        self.product_Table.heading("Quantite",text="Quantite")
        self.product_Table.heading("status",text="status")
        self.product_Table["show"]="headings"

        self.product_Table.column("id",width=40)
        self.product_Table.column("nom",width=100)
        self.product_Table.column("prix",width=100)
        self.product_Table.column("Quantite",width=40)
        self.product_Table.column("status",width=90)
        self.product_Table.pack(fill=BOTH,expand=1)
       
        self.product_Table.bind("<ButtonRelease-1>",self.get_data)

        lbl_note=Label(ProductFrame1,text="Note : Entrer 0 Quantite pour enlever le produit",font=("goudy old style",11),anchor='w',bg="white",fg="red").pack(side=BOTTOM,fill=X)
        

        #======CustomerFrame====
        self.var_cName=StringVar()
        self.var_contact=StringVar()
        CustomerFrame=Frame(self.root,bd=4,relief=RIDGE,bg="white")
        CustomerFrame.place(x=420,y=110,width=530,height=70)
        
        cTitle=Label(CustomerFrame,text="Details Clients",font=("goudy old style",15),bg="lightgray").pack(side=TOP,fill=X)
        lbl_Name=Label(CustomerFrame,text="Nom ",font=("times new roman",15),bg="white",fg="green").place(x=5,y=35) 
        txt_Name=Entry(CustomerFrame,textvariable=self.var_cName,font=("times new roman",13),bg="lightyellow").place(x=80 ,y=35,width=180)

        lbl_contact=Label(CustomerFrame,text="Contact No",font=("times new roman",15),bg="white",fg="green").place(x=270,y=35) 
        txt_contact=Entry(CustomerFrame,textvariable=self.var_contact,font=("times new roman",13),bg="lightyellow").place(x=380 ,y=35,width=140)

        #====Cal cart frame =================
        
        Cal_cart_Frame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Cal_cart_Frame.place(x=420,y=190,width=530,height=360)

        




         #====Calculator frame =================
        self.var_cal_input=StringVar()

        Cal_Frame=Frame(Cal_cart_Frame,bd=2,relief=RIDGE,bg="white")
        Cal_Frame.place(x=5,y=10,width=268,height=340)

        txt_cal_input=Entry(Cal_Frame,textvariable=self.var_cal_input,font=('arial',15,'bold'),width=21,bd=10,relief=GROOVE,state='readonly',justify=RIGHT)
        txt_cal_input.grid(row=0,columnspan=4)

        btn_7=Button(Cal_Frame,text=7,font=('arial',15,'bold'),command=lambda:self.get_input(7),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=0)
        btn_8=Button(Cal_Frame,text=8,font=('arial',15,'bold'),command=lambda:self.get_input(8),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=1)
        btn_9=Button(Cal_Frame,text=9,font=('arial',15,'bold'),command=lambda:self.get_input(9),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=2)
        btn_sum=Button(Cal_Frame,text='+',font=('arial',15,'bold'),command=lambda:self.get_input('+'),bd=5,width=4,pady=10,cursor="hand2").grid(row=1,column=3)

        btn_4=Button(Cal_Frame,text=4,font=('arial',15,'bold'),command=lambda:self.get_input(4),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=0)
        btn_5=Button(Cal_Frame,text=5,font=('arial',15,'bold'),command=lambda:self.get_input(5),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=1)
        btn_6=Button(Cal_Frame,text=6,font=('arial',15,'bold'),command=lambda:self.get_input(6),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=2)
        btn_sub=Button(Cal_Frame,text='-',font=('arial',15,'bold'),command=lambda:self.get_input('-'),bd=5,width=4,pady=10,cursor="hand2").grid(row=2,column=3)
        
        btn_1=Button(Cal_Frame,text=1,font=('arial',15,'bold'),command=lambda:self.get_input(1),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=0)
        btn_2=Button(Cal_Frame,text=2,font=('arial',15,'bold'),command=lambda:self.get_input(2),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=1)
        btn_3=Button(Cal_Frame,text=3,font=('arial',15,'bold'),command=lambda:self.get_input(3),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=2)
        btn_null=Button(Cal_Frame,text='*',font=('arial',15,'bold'),command=lambda:self.get_input('*'),bd=5,width=4,pady=10,cursor="hand2").grid(row=3,column=3)
        
        btn_0=Button(Cal_Frame,text='0',font=('arial',15,'bold'),command=lambda:self.get_input(0),bd=5,width=4,pady=17,cursor="hand2").grid(row=4,column=0)
        btn_c=Button(Cal_Frame,text='C',font=('arial',15,'bold'),command=self.clear_cal,bd=5,width=4,pady=17,cursor="hand2").grid(row=4,column=1)
        btn_eq=Button(Cal_Frame,text='=',font=('arial',15,'bold'),command=self.perform_cal,bd=5,width=4,pady=17,cursor="hand2").grid(row=4,column=2)
        btn_div=Button(Cal_Frame,text='/',font=('arial',15,'bold'),command=lambda:self.get_input('/'),bd=5,width=4,pady=17,cursor="hand2").grid(row=4,column=3)
        
        
        
        #====Cart frame =================
        cart_Frame=Frame(Cal_cart_Frame,bd=3,relief=RIDGE,bg="white")
        cart_Frame.place(x=280,y=8,width=245,height=342)
        self.cartTitle=Label(cart_Frame,text="Cart: \t Total Produits [0]",font=("goudy old style",15),bg="lightgray")
        self.cartTitle.pack(side=TOP,fill=X)

        scrolly=Scrollbar(cart_Frame,orient=VERTICAL)
        scrollx=Scrollbar(cart_Frame,orient=HORIZONTAL)

        self.CartTable=ttk.Treeview(cart_Frame,columns=("id","nom","prix","Quantite"),yscrollcommand=scrolly.set,xscrollcommand=scrollx.set)
        scrollx.pack(side=BOTTOM,fill=X)
        scrolly.pack(side=RIGHT,fill=Y)
        scrollx.config(command=self.CartTable.xview)
        scrolly.config(command=self.CartTable.yview)

        self.CartTable.heading("id",text="id")
        self.CartTable.heading("nom",text="Nom")
        self.CartTable.heading("prix",text="prix")
        self.CartTable.heading("Quantite",text="Quantite")
        self.CartTable["show"]="headings"

        self.CartTable.column("id",width=40)
        self.CartTable.column("nom",width=90)
        self.CartTable.column("prix",width=90)
        self.CartTable.column("Quantite",width=40)
        self.CartTable.pack(fill=BOTH,expand=1)
       
        self.CartTable.bind("<ButtonRelease-1>",self.get_data_cart)

        #====Add Cart widgets Frame=================
        self.var_id=StringVar()
        self.var_Name=StringVar()
        self.var_Prix=StringVar()
        self.var_Quantite=StringVar()
        self.var_stock=StringVar()
        
        Add_CartWidgetsFrame=Frame(self.root,bd=2,relief=RIDGE,bg="white")
        Add_CartWidgetsFrame.place(x=420,y=550,width=530,height=110)

        lbl_p_Name=Label(Add_CartWidgetsFrame,text="Nom produit",font=("times new roman",15),bg="white").place(x=5,y=5)
        txt_p_Name=Entry(Add_CartWidgetsFrame,textvariable=self.var_Name,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=5,y=35,width=190,height=22)

        lbl_p_Prix=Label(Add_CartWidgetsFrame,text="Prix produit",font=("times new roman",15),bg="white").place(x=230,y=5)
        txt_p_Prix=Entry(Add_CartWidgetsFrame,textvariable=self.var_Prix,font=("times new roman",15),bg="lightyellow",state='readonly').place(x=230,y=35,width=150,height=22)

        lbl_p_Quantite=Label(Add_CartWidgetsFrame,text="Quantite",font=("times new roman",15),bg="white").place(x=390,y=5)
        txt_p_Quantite=Entry(Add_CartWidgetsFrame,textvariable=self.var_Quantite,font=("times new roman",15),bg="lightyellow").place(x=390,y=35,width=120,height=22)

        self.lbl_instock=Label(Add_CartWidgetsFrame,text="En Stock",font=("times new roman",15),bg="white")
        self.lbl_instock.place(x=5,y=70)

        btn_clear_cart=Button(Add_CartWidgetsFrame,text="Effacer",command=self.clear_cart,font=("times new roman",15,"bold"),bg="lightgray",cursor="hand2").place(x=180,y=70,width=150,height=30)
        btn_add_cart=Button(Add_CartWidgetsFrame,text="Ajouter | Modifier",command=self.add_update_cart,font=("times new roman",15,"bold"),bg="orange",cursor="hand2").place(x=340,y=70,width=180,height=30)


    #=========billig area======
        billFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billFrame.place(x=953,y=110,width=410,height=410)

        bTitle=Label(billFrame,text="Payment Client",font=("goudy old style",20,"bold"),bg="#f44336",fg="white").pack(side=TOP,fill=X)
        scrolly=Scrollbar(billFrame,orient=VERTICAL)
        scrolly.pack(side=RIGHT,fill=Y)
        
        self.txt_bill_area=Text(billFrame,yscrollcommand=scrolly.set)
        self.txt_bill_area.pack(fill=BOTH,expand=1)
        scrolly.config(command=self.txt_bill_area.yview)

    #===========BILLING BUTTONS==============

        billMenuFrame=Frame(self.root,bd=2,relief=RIDGE,bg='white')
        billMenuFrame.place(x=953,y=520,width=410,height=140)

        self.lbl_amnt=Label(billMenuFrame,text='Montant \n [0]',font=("goudy old style",15,"bold"),bg="#3f5Ab5",fg="white")
        self.lbl_amnt.place(x=2,y=5,width=120,height=70)

        self.lbl_discount=Label(billMenuFrame,text='Remise de\n [5%]',font=("goudy old style",15,"bold"),bg="#8bc34a",fg="white")
        self.lbl_discount.place(x=124,y=5,width=120,height=70)

        self.lbl_net_pay=Label(billMenuFrame,text='Montant Net\n [0]',font=("goudy old style",15,"bold"),bg="#607d8b",fg="white")
        self.lbl_net_pay.place(x=246,y=5,width=120,height=70)

        btn_print=Button(billMenuFrame,cursor='hand2',text='Imprimer',command=self.print_bill,font=("goudy old style",15,"bold"),bg="lightgreen",fg="white")
        btn_print.place(x=2,y=80,width=120,height=50)

        btn_clear_all=Button(billMenuFrame,cursor='hand2',text='Effacer Tous ',command=self.clear_all,font=("goudy old style",15,"bold"),bg="gray",fg="white")
        btn_clear_all.place(x=124,y=80,width=120,height=50)

        btn_generate=Button(billMenuFrame,cursor='hand2',text='gener| Sauver',command=self.generate_bill,font=("goudy old style",15,"bold"),bg="#009688",fg="white")
        btn_generate.place(x=246,y=80,width=160,height=50)
        
        
        #========Footer==========
        footer=Label(self.root,text="Gestion Stock | DEVLOPPER PAR NAJALI BAKAROU ABENAY DOUIBI \n Contacter nous:+212 6-66-24-78-99",font=("times new roman",11),bg="#4d636d",fg="white").pack(side=BOTTOM,fill=X)

        self.afficher()
        # self.bill_top()
        self.update_date_time()


#========Alll Functions =====
    def get_input(self,num):
       xnum=self.var_cal_input.get()+str(num)
       self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')
    
    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))




#========Alll Functions =====
    def get_input(self,num):
       xnum=self.var_cal_input.get()+str(num)
       self.var_cal_input.set(xnum)

    def clear_cal(self):
        self.var_cal_input.set('')
    
    def perform_cal(self):
        result=self.var_cal_input.get()
        self.var_cal_input.set(eval(result))



    def afficher(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            cur.execute("SELECT id,Name,Prix,Quantite,status FROM produits where  status='Active'")
            rows=cur.fetchall()
            self.product_Table.delete(*self.product_Table.get_children())
            for row in rows:
                self.product_Table.insert('',END,values=row)
                
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}",parent=self.root)    

    def rechercher(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            if self.var_search.get()=="":
                messagebox.showerror("Error","Veuillez saisir la valeur que vous voulez rechercher!",parent=self.root)
            else:
                cur.execute("SELECT id,Name,Prix,Quantite,status FROM produits WHERE Name LIKE '%"+self.var_search.get()+"%' and status='Active'")
                rows=cur.fetchall()
                if len(rows)!=0:
                    self.product_Table.delete(*self.product_Table.get_children())
                    for row in rows:
                        self.product_Table.insert('',END,values=row)
                else:
                    messagebox.showerror("Error","Aucun résultat trouvé!",parent=self.root )
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}")


    def get_data(self,ev):
        f=self.product_Table.focus()
        content=(self.product_Table.item(f))
        row=content['values']  
        self.var_id.set(row[0])
        self.var_Name.set(row[1])
        self.var_Prix.set(row[2])
        self.lbl_instock.config(text=f"En Stock [{str(row[3])}]")
        self.var_stock.set(row[3])
        self.var_Quantite.set('1')

    
    def get_data_cart(self,ev):
        f=self.CartTable.focus()
        content=(self.CartTable.item(f))
        row=content['values']
        #id,Name,Prix,Quantite,stock  
        self.var_id.set(row[0])
        self.var_Name.set(row[1])
        self.var_Prix.set(row[2])
        self.var_Quantite.set(row[3])
        self.lbl_instock.config(text=f"En Stock [{str(row[4])}]")
        self.var_stock.set(row[4])
        

    def add_update_cart(self):
        if self.var_id.get()=='':
            messagebox.showerror('Error',"Sélectionner un produit de la liste!",parent=self.root)
        elif self.var_Quantite.get()=='':
            messagebox.showerror('Error',"Entrez la quantite !",parent=self.root)
        elif int(self.var_Quantite.get())>int(self.var_stock.get()):
            messagebox.showerror('Error',"Invalid  quantite !",parent=self.root)
        else:
            #price_cal=(int(self.var_Quantite.get())*float(self.var_Prix.get()))
            #price_cal=float(price_cal)
            #print(price_cal)
            price_cal=self.var_Prix.get()
            #id,Name,Prix,Quantite,stock
            cart_data=[self.var_id.get(),self.var_Name.get(),price_cal,self.var_Quantite.get(),self.var_stock.get()]
            #---update_cart---
            present='no'
            index_=0
            for row in self.cart_list:
                if self.var_id.get()==row[0]:
                    print(self.var_id)
                    present='yes'
                    break
                index_+=1
            if present=='yes':
                op=messagebox.askyesno('Confirm',"Ce produit existe déja voulez-vous modifier ou supprimer de la carte ? ",parent=self.root)
                if op==True:
                    if self.var_Quantite.get()=="0":
                        self.cart_list.pop(index_)
                    else:
                        #id,Name,Prix,Quantite,status
                        #self.cart_list[index_][2]=price_cal  #prix
                        self.cart_list[index_][3]=self.var_Quantite.get()  #Quantite
                       
            else:
                self.cart_list.append(cart_data)
            self.show_cart()
            self.bill_updates()

    def bill_updates(self):
        self.bill_amnt=0
        self.net_pay=0
        self.discount=0
        for row in self.cart_list:
            #id,Name,Prix,Quantite,stock
            self.bill_amnt=self.bill_amnt+(float(row[2])*int(row[3]))
            

        self.discount=(self.bill_amnt*5)/100
        self.net_pay=self.bill_amnt-self.discount
        self.lbl_amnt.config(text=f'Montant \n{str(self.bill_amnt)}')
        self.lbl_net_pay.config(text=f'Montant Net \n{str(self.net_pay)}')
        self.cartTitle.config(text=f"Cart: \t Total Produits : [{str(len(self.cart_list))}]")
    
    def show_cart(self):
        
        try:
            self.CartTable.delete(*self.CartTable.get_children())
            for row in self.cart_list:
                self.CartTable.insert('',END,values=row)
                
        except Exception as ex:
            messagebox.showerror("Error",f"Erreur : {str(ex)}",parent=self.root) 

    def generate_bill(self):
        if self.var_cName.get()=='' or self.var_contact.get()=='':
            messagebox.showerror("Error",f"Les information du Client sont necessaire ",parent=self.root)
        elif len(self.cart_list)==0:
            messagebox.showerror("Error",f"Veuillez ajoute le produit ou panier ! ",parent=self.root)
        else:
            #=======BILL TOp====
            self.bill_top()
            #=====bill middle====
            self.bill_middle()
            #====bill bottom====
            self.bill_bottom()

            fp=open(f'bill/{str(self.invoice)}.txt','w')
            fp.write(self.txt_bill_area.get('1.0',END))
            fp.close()
            messagebox.showinfo('Saved',"Facture enregistrer .",parent=self.root)
            self.chk_print=1


    def bill_top(self):
        self.invoice=int(time.strftime("%H%M%S"))+int(time.strftime("%d%m%Y"))
        bill_top_temp=f'''
\t\tFacture
\t Num Tel. 98725***** , Marrakech-40000
{str("="*47)}
Client Name: {self.var_cName.get()}
Num Tel :{self.var_contact.get()}
Nr Facture : {str(self.invoice)}\t\t\tDate: {str(time.strftime("%d/%m/%Y"))}
{str("="*47)}
 Nom Produit\t\t\tQuantite\tPrix
 {str("="*47)}
        '''
        self.txt_bill_area.delete('1.0',END)
        self.txt_bill_area.insert('1.0',bill_top_temp)

    def bill_bottom(self):
        bill_bottom_temp=f'''
{str("="*47)}
Montant Facture\t\t\t\tDH.{self.bill_amnt}
Remise\t\t\t\tDH.{self.discount}
Montant net\t\t\t\tDH.{self.net_pay}
{str("="*47)}\n
        '''
        self.txt_bill_area.insert(END,bill_bottom_temp)



    def bill_middle(self):
        con=sqlite3.connect(database=r'ims.db')
        cur=con.cursor()
        try:
            for row in self.cart_list:
                #id,Name,Prix,Quantite,stock
                id=row[0]
                name=row[1]
                Quantite=int(row[4])-int(row[3])
                if int(row[3])==int(row[4]):
                    status='Inactive'
                if int(row[3])!=int(row[4]):
                    status='Active'

                Prix=float(row[2])*int(row[3])
                Prix=str(Prix)
                self.txt_bill_area.insert(END,"\n "+name+"\t\t\t"+row[3]+"\tDH."+Prix)
                #==========update quantite in product table==========
                cur.execute('Update produits set Quantite=?,status=? WHERE id=?',(
                    Quantite,
                    status,
                    id       
                ))
                con.commit()
            con.close()
            self.afficher()
        except Exception as ex:
                messagebox.showerror("Error",f"Erreur : {str(ex)}",parent=self.root) 

    def clear_cart(self):
        self.var_id.set('')
        self.var_Name.set('')
        self.var_Prix.set('')
        self.var_Quantite.set('')
        self.lbl_instock.config(text=f"En Stock")
        self.var_stock.set('')
    
    def clear_all(self):
        del self.cart_list[:]
        self.var_cName.set('')
        self.var_contact.set('')
        self.txt_bill_area.delete('1.0',END)
        self.cartTitle.config(text=f"Cart: \t Total Produits : [0]")
        self.var_search.set('')
        self.clear_cart()
        self.afficher()
        self.show_cart()
        self.chk_print=0

        
    def update_date_time(self):
        time_=time.strftime("%I:%M:%S")
        date_=time.strftime("%d-%m-%Y")
        self.label_clock.config(text=f"Bienvenue dans le Gestionnaire de Stock\t\t Date: {str(date_)}\t\t Time: {str(time_)}")
        self.label_clock.after(200,self.update_date_time)
    
    def print_bill(self):
        if self.chk_print==1:
           messagebox.showinfo('Imprimer',"Veuillez attendre",parent=self.root)
           new_file=tempfile.mktemp('.txt')
           open(new_file,'w').write(self.txt_bill_area.get('1.0',END))
           os.startfile(new_file,'Imprimer')
        else:
            messagebox.showerror('Imprimer',"Veuillez creer la facture",parent=self.root)


if __name__=="__main__":
    root=Tk()
    obj=BillClass(root)
    root.mainloop()
