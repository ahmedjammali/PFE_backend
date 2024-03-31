import pyodbc

def get_connection():
    conn = pyodbc.connect('DRIVER={SQL Server};SERVER=JAMMALI-AHMED1\SQLEXPRESS;DATABASE=Db_TriSQR_ProdOLD')
    return conn

