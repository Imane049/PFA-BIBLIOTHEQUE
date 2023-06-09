# APPLICATION GESTION DE BIBLIOTHEQUE
Le projet consiste en une application de gestion de bibliothèque comprenant deux vues: une vue administrateur et une vue adhérent. La vue administrateur permet de gérer les réservations, les emprunts, les livres et les adhérents. La vue adhérent permet de parcourir les livres, de les réserver et de voir l'état de ses emprunts. L'interface graphique de l'application est réalisée en utilisant la bibliothèque Tkinter de Python, tandis que la base de données est gérée par SQLite.

### Tkinter et SQLite, pourquoi? 
Tkinter est une bibliothèque standard de Python pour créer des interfaces graphiques (GUI). Elle est simple à utiliser et offre de nombreuses fonctionnalités pour créer des applications de bureau avec des interfaces graphiques interactives. Elle est également compatible avec la plupart des systèmes d'exploitation et des plates-formes, ce qui la rend très flexible et facile à déployer.

SQLite est une base de données relationnelle légère qui est souvent utilisée pour des applications de bureau. Elle est facile à utiliser et ne nécessite pas de configuration de serveur, ce qui la rend très pratique pour des projets de petite envergure. SQLite est également très rapide et peut gérer de grandes quantités de données. Elle est compatible avec la plupart des langages de programmation, y compris Python.

C'est pourquoi, pour le projet de gestion de bibliothèque, nous avons choisi d'utiliser Tkinter pour la création de l'interface utilisateur et SQLite pour stocker les données de la bibliothèque.

## Sommaire :
- Partie Conception
- Fonctionalités 
- Installation et utilisation
- Contributeurs

# Partie Conception
Le MCD est donné par:
![mcd](MCD.PNG)

d'où le MLDR suivant:
```
Bibliothecaire(ID_BIBLIOTHECAIRE, username, password)
CLIENT(ID_CLIENT, PERSONAL_NAME, FAMILY_NAME, USERNAME, PASSWORD, AGE, ADRESS, EMAIL, PHONE)
BOOK(ID_BOOK, TITLE, AUTHOR, ISBN, GENRE; ANNEE, LANGUE, CONTEMLATION_SUR_PLACE)
RENTAL(ID_BOOK, ID_CLIENT, DATE_EMPRUNT)
RESERVATION(ID_BOOK, ID_CLIENT)
```
d'où la base de données donnée par:
```
conn=sqlite3.connect("bibliotheque.db")
print("database connected successfully")


##creation des tables admin et client
conn.execute("""CREATE TABLE IF NOT EXISTS BIBLIOTHECAIRE(BIBLIOTHECAIRE_ID INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
USERNAME TEXT NOT NULL,
PASSWORD TEXT NOT NULL)""")
#La bibliotheque a un seul admin
conn.execute("""CREATE TRIGGER IF NOT EXISTS enforce_single_row
BEFORE INSERT ON BIBLIOTHECAIRE
BEGIN
  SELECT
    CASE
      WHEN (SELECT COUNT(*) FROM BIBLIOTHECAIRE) >= 1 THEN
        RAISE(ABORT, 'Only one row is allowed in this table')
    END;
END;
""")
conn.execute("""INSERT INTO BIBLIOTHECAIRE(username, password)
SELECT ? , ?
WHERE NOT EXISTS (SELECT 1 FROM BIBLIOTHECAIRE)""", ("admin", "pwd"))
print("table bibliothecaire connected successfully")
#conn.execute("""INSERT INTO BIBLIOTHECAIRE(USERNAME, PASSWORD) VALUES("admin","pwd")""")
conn.execute("""
    CREATE TABLE IF NOT EXISTS CLIENT (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        PERSONAL_NAME TEXT NOT NULL,
        FAMILY_NAME TEXT NOT NULL,
        PASSWORD TEXT NOT NULL,
        AGE INTEGER,
        ADDRESS TEXT,
        PHONE INTEGER NOT NULL,
        EMAIL TEXT NOT NULL,
        USERNAME TEXT
    )
""")



conn.execute("""CREATE TABLE IF NOT EXISTS BOOKS (ID INTEGER PRIMARY KEY AUTOINCREMENT, TITLE TEXT NOT NULL, AUTHOR TEXT NOT NULL, GENRE TEXT, LANGUAGE TEXT, year INTEGER , CONTEMPLATION_SUR_PLACE INTEGER CHECK (CONTEMPLATION_SUR_PLACE IN (0,1)), ISBN INTEGER NOT NULL, IMAGE BLOB)""")

conn.execute("""CREATE TABLE IF NOT EXISTS rentals (BOOK_ID INT NOT NULL, CLIENT_ID INT, DATE_EMPRUNT DATE, FOREIGN KEY (BOOK_ID) references BOOKS(ID), FOREIGN KEY (CLIENT_ID) REFERENCES CLIENT(ID))""")

conn.execute("""CREATE TABLE IF NOT EXISTS reservations (BOOK_ID INT NOT NULL, CLIENT_ID INT, DATE_EMPRUNT DATE, FOREIGN KEY (BOOK_ID) references BOOKS(ID), FOREIGN KEY (CLIENT_ID) REFERENCES CLIENT(ID))""")

conn.commit()

delai_emprunt = 15
delai_reservation = 7

```
+ La bibliothèque n'a qu'un seul admin d'où l'utilisation du trigger. Les identifiants par défaut de l'admin sont __(username=admin, password=pwd)__ mais qu'il peut changer à tout moment
+ Le username de chaque utilisateur est généré automatiquement à travers la concaténation de son nom personel et de son id et son mot de passe est géneré automatiquement et aléatoirement, garantissant ainsi l'unicité des identifiants de connection de chaque utilisateurs et ainsi la confidentialité de leur comptes
+ Chaque livre emprunté doit etre retourné dans un délai de 15 par defaut et chaque reservation est annulée si le livre n'est pas récupéré dans un délai de 7 jours :
```
conn.execute(" DELETE FROM reservations WHERE date( DATE_EMPRUNT + ? ) < date('now')", (delai_reservation,))

```
  * les deux délais sontmodifiables par l'admin
![settings_change](settings.PNG)
+ 
# Fonctionalités:
L'application gestion de bibliothèque offre plusieurs fonctionalités conçues pour répondre aux besoins à la fois des administrateurs de bibliothèques et des adhérents à travers une interface simple et .

### Authentfication et enregistrement:
- S'authetifier : Se connecter à son compte à travers ses identifiants uniques
![login](login.PNG) 
- Créer un compte : Les adhérents de la bibliothèque peuvent se créer des comptes
![sigunp](signup.PNG)
- Le nom d'utilisateur et le mot de passe se chaque adhérent sont générés de façon automatique. Une fiche apparait après l'enregistrement pour que l'adgérent puisse noter ses identifiants. Il a aussi la possibilité de les modifier ou de supprimer son compte
![infos](infossignup.PNG)
 
### Vue administrateur :
 
* Gérer les adhérents : Ajouter, supprimer, modifier et parcourir les informations des adhérents
 + Ajouter des adhérents :
 ![ajout_client](addclient.PNG)
 +Parcourir les adhérents :
 ![parcourir_client](browseclient.PNG)
 +Chercher des clients particuliers:
     Exemple: recherche clients avec "user" dans leur nom
     ![chercher_client](searchclient.PNG)
  +Selectionner un client particulier afin d'afficher toutes ses informations (les identifiant et mots de passe ne sont pas affichés sinon pour des raisons de confidentialité), les modifier ou supprimer son compte
  ![selection_client](selectionclient.PNG)
  
* Gérer les livres : Ajouter, supprimer, modifier, rechercher et parcourir les livres de la bibliothèque
 + Ajouter un livre:
 ![ajout_livre](addbook.PNG)
 +Parcourir les livres de la bibliothèque:
 ![parcourir_livres](browsebook.PNG)
 + Rechercher un livre en particulier. En plus de la fonction de recherche basique, il est possible d'afficher plus d'options de recherche(par auteur, année, etc...) en appyuant sur le bouton "more options"
    Exemple: recherche livre avec nom d'auteur "author2"
    ![searchbook](searchbook.PNG)
 + Selectionner un livre afin d'afficher toutes les informations le concernant, les modifier ou supprimer le livre:
 ![selectionner_livre](selectionbook.PNG)
 
* Gérer les emprunts et retours: 
  + Parcourir les emprunts et voir s'ils sont en retard ou pas
  ![browse_rental](browserental.PNG)
  + Enregistrer un nouvel emprunt à travers les ids respectifs du client et du livre concernés
  ![addrental](addrental.PNG)
  +  Retourner un livre emprunté à partir des memes ids
  ![registerreturn](return.PNG)
  
 * Accéder aux statistiques de la bibliothèque:
 ![statistiques](statistiques.PNG)
 * Modifier son identifiant et mot de passe et se déconnecter
  ![accountadmin](accountadmin.PNG)

### Vue adhérent :

- Parcourir les livres disponibles : 
   + Parcourir les livres de la bibliothèque et voir s'ils sont à emprunter ou à consulter sur place
   ![browsebooks](browsebooks.PNG)
   + Rechercher un livre par titre, auteur, année, etc...
   ![searchbooks](searchbooks.PNG)
   + Selectionner un livre en particulier pour voir ses informations et éventuellement le réserver s'il n'est pas déja reservé
   ![selectionbook](infosbook.PNG)

- Consulter l'état de ses emprunts : 
   + Voir les livres empruntés par soi et vérifier si on est en retard ou pas
   ![browserental](reservationbrowse.PNG)
   + Etre alerté de ses retards le cas échéant dés qu'on est connecté
   ![alerteretard](alerteretard.PNG)
   
 - Modifier les informations relatives à son compte, se déconnecter ou supprimer son compte
  ![manageaccount](account.PNG)

* Toutes ces fonctionalités sont offertes à l'utilisateur à travers une expérience facile et intuitive, avec une interface utilisateur claire et conviviale, 
 réalisée via le module ThemedStyle de ttkthemes qui permet d'appliquer des thèmes préconcus et personalisables à notre application de façon simple
```
import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedStyle

root= tk.Tk()
```
Il suffit de créer un objet style et de l'affecter à l'objet fenetre/widget/frame de notre choix pour qu'il s'applique à toutes ses composantes. On a choisi le thème "breeze" à cause des graphiques harmonieux et simples qu'il offre
```
style = ThemedStyle(home)
style.set_theme("breeze")

```
Attention cependant à utiliser des objets ttk et non tk puisque ces derniers ne sont pas supportés par le module ThemedStyle
```
label = ttk.Label(root, text="This is a mabel ") #not tk.Label(...
label.pack()

entry =ttk.Entry(root)
entry.pack()

button = ttk.Button(root, text="This is a button")
button.pack()
```
## Utilisation : 
 Pour utiliser l'application, veuillez mettre les fichiers .py contenus dans ce repository dans le meme emplacement et excecuter le fichier "login.py"

## Contributeurs:
Cette application a été réalisé dans le cadre du P.F.A. du groupe 5 3 I.I.R. de l'EMSI MARRAKECH, sous la supervisition de Mr. Ayoub CHAREF
 + Imane BARAKATE
 + Oussama MARIR
 + Zouhair LAFROUGUI
 
