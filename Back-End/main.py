from fastapi import FastAPI
from typing import Optional
import mysql.connector
import json
from pydantic import BaseModel
from starlette.middleware.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:4200",
    "http://localhost",
    "http://localhost:8000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Employe (BaseModel):
    cin: int
    nom: str
    prenom: str
    date_de_naissance: int
    sexe: str


@app.get("/employe/")
def fetch_employes():
    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="mydb1")
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM employe")
    return mycursor.fetchall()


@app.get("/employe/{empId}")
def fetch_employe(empId: str):
    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="mydb1")
    mycursor = mydb.cursor()
    mycursor.execute(f"SELECT * FROM employe where cin={empId}")
    return mycursor.fetchone()


@app.post("/employe/add")
def add_employe(new_employe: Employe):
    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="mydb1")
    mycursor = mydb.cursor()
    mycursor.execute(
        f"INSERT INTO employe (cin, nom, prenom, date_de_naissance, sexe) VALUES ({new_employe.cin}, '{new_employe.nom}', '{new_employe.prenom}',{new_employe.date_de_naissance}, '{new_employe.sexe}')")
    mydb.commit()
    return "employe Added"


@app.delete("/employe/delete/{empId}")
def delete_employe(empId: str):
    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="mydb1")
    mycursor = mydb.cursor()
    mycursor.execute(f"delete from employe where cin = {empId}")
    mydb.commit()
    return "employe deleted"


@app.put("/employe/update/{empId}")
def update_employe(empId: int, new_employe: Employe):
    mydb = mysql.connector.connect(host="localhost", user="root", password="", database="mydb1")
    mycursor = mydb.cursor()
    mycursor.execute(
        f"update employe set cin={new_employe.cin}, nom='{new_employe.nom}', prenom='{new_employe.prenom}', date_de_naissance={new_employe.date_de_naissance},sexe= '{new_employe.sexe}'  where cin = {empId}")
    mydb.commit()
    return "employe updated"
