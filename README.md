# CoachingProject-serveur
OT  Sims - Backend

## Installation de l'environnement de développement

* Python
=========
Pour pouvoir utiliser le framework Django, vous devez installer python sur votre système. (Nous utiliserons python 3.4)
** Commande d'installation
**sudo apt-get install python3.4**

* virtualenv
=========
Les virtualenv permettent d'isoler différentes configurations python sur votre système Linux. (Exemple si vous développez deux projets avec un utilisant python 2 et l'autre python 3)

** Création du virtualenv
La création d'un virtualenv va entrâiner la création d'un dossier contenant les fichiers nécessaires à python pour fonctionner. En entrant dans le virtualenv, vous définissez votre configuration de base python comme étant celle présente dans ce dossier. 

** Commande de création du virtualenv
**virtualenv -p python3.4 [nom_du_dossier]**

* Django
========
Django est le framework que nous allons utiliser pour développer le backend (partie serveur) de notre projet. 
Vous pouvez trouver beaucoup d'informations sur Django sur (https://www.djangoproject.com/)

** Installation
Vous devez installer Django dans le virtualenv que vous avez précédemment créé.
Pour rentrer dans le virtualenv, allez dans le dossier du virtualenv que vous avez créé et lancer la commande d'activation de l'environnement :
**cd [chemin_vers_dossier_virtualenv]**
**source bin/activate**

Vous êtes maintenant dans l'environnement (le nom de l'environnement doit apparaître avant le prompt dans la console)
Vous devez maintenant installer Django :
**pip install django**

Puis les éléments nécessaires au projet :
**pip install djangorestframework**
**pip install markdown**
**pip install django-filter**

Vous devez ensuite créer un projet Django :
**django-admin startproject [nom_du_projet]

Puis cloner le repository dans ce dossier.

**N'oubliez pas de vous mettre à chaque fois dans votre virtualenv avant de travailler sur le projet !**


