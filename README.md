# PFA-BIBLIOTHEQUE
Le projet consiste en une application de gestion de bibliothèque comprenant deux vues: une vue administrateur et une vue adhérent. La vue administrateur permet de gérer les réservations, les emprunts, les livres et les adhérents. La vue adhérent permet de parcourir les livres, de les réserver et de voir l'état de ses emprunts. L'interface graphique de l'application est réalisée en utilisant la bibliothèque Tkinter de Python, tandis que la base de données est gérée par SQLite.

### Tkinter et SQLite, pourquoi? 
Tkinter est une bibliothèque standard de Python pour créer des interfaces graphiques (GUI). Elle est simple à utiliser et offre de nombreuses fonctionnalités pour créer des applications de bureau avec des interfaces graphiques interactives. Elle est également compatible avec la plupart des systèmes d'exploitation et des plates-formes, ce qui la rend très flexible et facile à déployer.

SQLite est une base de données relationnelle légère qui est souvent utilisée pour des applications de bureau. Elle est facile à utiliser et ne nécessite pas de configuration de serveur, ce qui la rend très pratique pour des projets de petite envergure. SQLite est également très rapide et peut gérer de grandes quantités de données. Elle est compatible avec la plupart des langages de programmation, y compris Python.

C'est pourquoi, pour le projet de gestion de bibliothèque, nous avons choisi d'utiliser Tkinter pour la création de l'interface utilisateur et SQLite pour stocker les données de la bibliothèque.

## Sommaire :
- Partie Conception
- Installation
- Fonctionalités et usage
- Contributeurs
- Contact

## Partie Conception

## Fonctionalités et usage :
L'application de gestion de bibliothèque comporte les fonctionnalités suivantes :

### Authentfication et enregistrement:
- S'authetifier : Se connecter à son compte à travers ses identifiants uniques
![login](login.png)
- Créer un compte : Les adhérents de la bibliothèque peuvent se créer des comptes
- Personaliser ses informations : 
### Vue administrateur :

- Gérer les livres : Ajouter, supprimer, modifier, rechercher et parcourir les livres de la bibliothèque
- Gérer les adhérents : Ajouter, supprimer, modifier et parcourir les informations des adhérents
Gérer les emprunts : Enregistrer un nouvel emprunt, retourner un livre emprunté

### Vue adhérent :

- Parcourir les livres disponibles : Rechercher un livre par titre, auteur, année, etc.
- Réserver un livre : Vérifier la disponibilité d'un livre et le réserver en ligne
- Consulter l'état de ses emprunts : Voir les livres empruntés et vérifier si on est en retard ou pas

L'application de gestion de bibliothèque est conçue pour offrir une expérience utilisateur facile et intuitive, avec une interface utilisateur claire et conviviale. Les fonctionnalités sont conçues pour répondre aux besoins à la fois des administrateurs de bibliothèques et des adhérents.




