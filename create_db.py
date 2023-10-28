import sqlite3
def create_db():
    con=sqlite3.connect(database=r'ims.db')
    cur=con.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS employee(id INTEGER PRIMARY KEY AUTOINCREMENT,nom text,email text,genre text,contact text,dob text,doj text,pwd text,utype text,adresse text,salaire text)")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS fournisseur(invoice INTEGER PRIMARY KEY AUTOINCREMENT,nom text,contact text,descriptionf text)")
    con.commit()
    
    cur.execute("CREATE TABLE IF NOT EXISTS categorie(cid INTEGER PRIMARY KEY AUTOINCREMENT,nom text )")
    con.commit()

    cur.execute("CREATE TABLE IF NOT EXISTS produits(id INTEGER PRIMARY KEY AUTOINCREMENT,categories text,fournisseurs text,Name text,Prix text,Quantite text,status text)")
    con.commit()
create_db()