# Projet Flashcards Interactives

## Auteur : Saikou

---

## 1. Introduction & Objectif

Ce projet vise à créer une application interactive de flashcards permettant de réviser différents concepts en data science, machine learning, statistiques, et bien d'autres domaines. L'application est développée avec **Streamlit** et utilise **SQLite** pour stocker les flashcards et les statistiques d'apprentissage.

### Objectifs principaux :

- Créer, stocker et gérer des flashcards de manière interactive.
- Implémenter un système de révision basé sur les probabilités d'apparition des cartes.
- Suivre les statistiques d'apprentissage des utilisateurs.
- Permettre l'ajout et la gestion de thèmes pour organiser les cartes.

---

## 2. Contenu du Projet

### Fonctionnalités principales :

- **Révision des flashcards** : Affichage des questions et réponses avec un suivi des bonnes/mauvaises réponses.
- **Ajout de nouvelles cartes** : Interface permettant d'ajouter des cartes avec une probabilité initiale.
- **Gestion des thèmes** : Possibilité d'ajouter/supprimer des thèmes pour organiser les cartes.
- **Mise à jour dynamique des probabilités** : Pondération des cartes en fonction des performances de l'utilisateur.
- **Affichage des statistiques** : Consultation des performances passées.
- **Débogage des cartes** : Vérification des probabilités associées aux cartes.

---

## 3. Installation & Prérequis

### Environnement

Ce projet fonctionne avec **Python 3.10** et est recommandé pour une utilisation dans un environnement virtuel Conda.

### Installation

1. **Cloner le projet** :
   ```bash
   git clone https://github.com/ton-profil/Projet_Flashcards.git
   cd Projet_Flashcards
   ```

2. **Créer l'environnement Conda** :
   ```bash
   conda env create -f environment.yml
   conda activate flashcards_env
   ```

3. **Ou, installer les dépendances avec pip** :
   ```bash
   pip install -r requirements.txt
   ```

4. **Lancer l'application Streamlit** :
   ```bash
   streamlit run app.py
   ```

---

## 4. Base de Données

L'application utilise **SQLite** pour stocker les flashcards et suivre les statistiques d'apprentissage.

Les principales tables sont :

- **Themes** : Stocke les différents thèmes de cartes.
- **Cards** : Contient les questions, réponses et probabilités associées.
- **Stats** : Enregistre le nombre de bonnes et mauvaises réponses par date.

---

## 5. Structure du Projet

```
Projet_Flashcards/
│── app.py                 # Application principale Streamlit
│── database.py            # Fonctions de gestion de la base SQLite
│── utils.py               # Fonctions utilitaires
│── requirements.txt       # Liste des dépendances pip
│── environment.yml        # Fichier Conda pour recréer l'environnement
│── README.md              # Documentation du projet
└── flashcards.db          # Base de données SQLite (créée automatiquement)
```

---

## 6. Difficultés & Défis

- **Gestion des probabilités** : Ajuster dynamiquement la probabilité d'apparition des cartes pour favoriser l'apprentissage.
- **Suivi des performances** : Implémenter un suivi efficace des statistiques d'apprentissage.
- **Expérience utilisateur** : Rendre l'interface intuitive et facile à utiliser.

---

## 7. Comment Contribuer ?

Vous pouvez contribuer en :
- Ajoutant de nouveaux thèmes ou cartes.
- Optimisant la gestion des probabilités.
- Intégrant de nouvelles fonctionnalités pour améliorer l'expérience utilisateur.
- Proposant des corrections ou améliorations via des **pull requests**.

---

## 8. Contact

Pour toute question ou suggestion, n'hésitez pas à me contacter sur GitHub ou LinkedIn ou via mon site  saikou-bah.github.io/mon_site_public