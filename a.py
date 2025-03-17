import streamlit as st
import sqlite3
from datetime import datetime
import random

DB_NAME = "flashcards.db"

def connect_db():
    return sqlite3.connect(DB_NAME)

def init_db():
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("PRAGMA foreign_keys=ON;")
        c.execute('''CREATE TABLE IF NOT EXISTS Themes (
                        ID INTEGER PRIMARY KEY,
                        Theme TEXT  
                    );''')
        c.execute('''CREATE TABLE IF NOT EXISTS Cards(
                        ID INTEGER PRIMARY KEY,
                        Question TEXT,
                        Reponse TEXT,
                        Probabilite REAL CHECK(Probabilite >= 0.1 AND Probabilite <= 1),
                        id_theme INTEGER,
                        FOREIGN KEY (id_theme) REFERENCES Themes(ID) ON DELETE RESTRICT
                    );''')
        c.execute('''CREATE TABLE IF NOT EXISTS Stats(
                        ID INTEGER PRIMARY KEY,
                        Bonnes_Reponses INTEGER,
                        Mauvaises_Reponses INTEGER,
                        Date DATE
                    );''')
        conn.commit()

def get_random_card(theme_id):
    """ Sélectionne une carte en fonction de sa probabilité mise à jour (pondérée) pour un thème donné """
    with connect_db() as conn:
        conn.execute("PRAGMA read_uncommitted = TRUE;")
        c = conn.cursor()
        c.execute("SELECT ID, Question, Reponse, Probabilite FROM Cards WHERE id_theme = ?", (theme_id,))
        cards = c.fetchall()  # Récupère toutes les cartes du thème sélectionné

    if not cards:
        return None

    # Extraction des données
    ids = [card[0] for card in cards]
    questions = [card[1] for card in cards]
    responses = [card[2] for card in cards]
    probabilities = [card[3] for card in cards]

    # Normalisation des probabilités pour garder les pondérations correctes
    total_prob = sum(probabilities)
    probabilities = [p / total_prob for p in probabilities] if total_prob > 0 else [1 / len(cards)] * len(cards)

    # Sélection aléatoire pondérée basée sur la probabilité de chaque carte
    chosen_index = random.choices(range(len(cards)), weights=probabilities, k=1)[0]

    return ids[chosen_index], questions[chosen_index], responses[chosen_index]

def update_card_probability(card_id, is_correct):
    """ Met à jour la probabilité d'apparition d'une carte en fonction de la réponse de l'utilisateur """
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT Probabilite FROM Cards WHERE ID = ?", (card_id,))
        card = c.fetchone()
        if card:
            current_prob = card[0]
            new_prob = current_prob * 0.7 if is_correct else current_prob * 1.3
            new_prob = max(0.1, min(new_prob, 1.0))  # Assurer que la probabilité reste entre 0.1 et 1
            c.execute("UPDATE Cards SET Probabilite = ? WHERE ID = ?", (new_prob, card_id))
            conn.commit()

        # 🔥 Forcer la mise à jour immédiate des probabilités
        c.execute("PRAGMA wal_checkpoint(FULL);")
        conn.commit()
        
def update_stats(is_correct):
    today = datetime.now().strftime("%Y-%m-%d")
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT * FROM Stats WHERE Date = ?", (today,))
        stats = c.fetchone()
        if stats:
            bonnes_reponses = stats[1] + 1 if is_correct else stats[1]
            mauvaises_reponses = stats[2] + 1 if not is_correct else stats[2]
            c.execute("UPDATE Stats SET Bonnes_Reponses = ?, Mauvaises_Reponses = ? WHERE Date = ?", (bonnes_reponses, mauvaises_reponses, today))
        else:
            bonnes_reponses = 1 if is_correct else 0
            mauvaises_reponses = 0 if is_correct else 1
            c.execute("INSERT INTO Stats (Bonnes_Reponses, Mauvaises_Reponses, Date) VALUES (?, ?, ?)", (bonnes_reponses, mauvaises_reponses, today))
        conn.commit()

def reset_probabilities():
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("UPDATE Cards SET Probabilite = 0.5")
        conn.commit()
        st.success("Toutes les probabilités ont été réinitialisées à 0.5.")

def show_flashcards():
    st.subheader("Réviser les Flashcards")

    with connect_db() as conn:
        themes = conn.execute("SELECT ID, Theme FROM Themes").fetchall()

    if not themes:
        st.warning("Aucun thème disponible. Ajoutez d'abord un thème.")
        return

    # Sélection du thème
    theme_choice = st.selectbox("Sélectionnez un thème :", themes, format_func=lambda x: x[1])

    if "current_card" not in st.session_state or st.session_state.get("card_changed", False):
        st.session_state.current_card = get_random_card(theme_choice[0])
        st.session_state.show_answer = False
        st.session_state.card_changed = False

    card = st.session_state.current_card

    if card:
        id_card, question, reponse = card
        st.write(f"**Question:** {question}")

        if st.button("Voir la réponse"):
            st.session_state.show_answer = True

        if st.session_state.get("show_answer", False):
            st.write(f"**Réponse:** {reponse}")

        col1, col2 = st.columns(2)
        with col1:
            if st.button("Je connais cette réponse"):
                update_card_probability(id_card, True)
                update_stats(True)
                st.session_state.card_changed = True
                st.session_state.show_answer = False
                st.rerun()

        with col2:
            if st.button("Je ne connais pas cette réponse"):
                update_card_probability(id_card, False)
                update_stats(False)
                st.session_state.card_changed = True
                st.session_state.show_answer = False
                st.rerun()
    else:
        st.warning("Aucune carte disponible pour ce thème.")




def add_flashcard():
    st.subheader("➕ Ajouter une Flashcard")
    question = st.text_input("Question")
    reponse = st.text_area("Réponse")
    with connect_db() as conn:
        themes = conn.execute("SELECT ID, Theme FROM Themes").fetchall()
    id_theme = st.selectbox("Thème", themes, format_func=lambda x: x[1])
    if st.button("Ajouter la carte"):
        if question and reponse:
            with connect_db() as conn:
                c = conn.cursor()
                c.execute("INSERT INTO Cards (Question, Reponse, Probabilite, id_theme) VALUES (?, ?, ?, ?)", (question, reponse, 0.5, id_theme[0]))
                conn.commit()
                st.success("Carte ajoutée avec succès !")
                
def show_cards_by_theme():
    st.subheader("📂 Afficher les cartes par thème")
    with connect_db() as conn:
        themes = conn.execute("SELECT ID, Theme FROM Themes").fetchall()
    if not themes:
        st.warning("Aucun thème disponible. Ajoutez d'abord un thème.")
        return
    
    id_theme = st.selectbox("Choisissez un thème", themes, format_func=lambda x: x[1])
    with connect_db() as conn:
        cards = conn.execute("SELECT Question, Reponse, Probabilite FROM Cards WHERE id_theme = ?", (id_theme[0],)).fetchall()
    
    if cards:
        for question, reponse, prob in cards:
            st.write(f"**Question :** {question}")
            st.write(f"**Réponse :** {reponse}")
            st.write(f"**Probabilité :** {prob:.2f}")
            st.markdown("---")
    else:
        st.info("Aucune carte disponible pour ce thème.")
def debug_card_probabilities():
    """ Affiche les probabilités des cartes pour vérifier leur évolution """
    st.subheader("🔍 Débogage : Probabilités des Cartes")
    with connect_db() as conn:
        c = conn.cursor()
        c.execute("SELECT ID, Question, Probabilite FROM Cards ORDER BY Probabilite DESC")
        cards = c.fetchall()
    if cards:
        for card in cards:
            st.write(f"**ID:** {card[0]}, **Question:** {card[1]}, **Probabilité:** {card[2]:.2f}")
    else:
        st.warning("Aucune carte disponible.")
        
def show_stats():
    st.subheader("📊 Statistiques d'apprentissage")
    with connect_db() as conn:
        stats = conn.execute("SELECT Date, Bonnes_Reponses, Mauvaises_Reponses FROM Stats ORDER BY Date DESC").fetchall()
    if stats:
        st.table(stats)
    else:
        st.info("Aucune statistique disponible.")
    if st.button("Réinitialiser toutes les probabilités"):
        reset_probabilities()

def add_theme():
    st.subheader("➕ Ajouter un Thème")
    new_theme = st.text_input("Nom du nouveau thème")
    if st.button("Ajouter le thème"):
        if new_theme:
            with connect_db() as conn:
                c = conn.cursor()
                c.execute("INSERT INTO Themes (Theme) VALUES (?)", (new_theme,))
                conn.commit()
                st.success("Thème ajouté avec succès !")

def delete_theme():
    st.subheader("🗑 Supprimer un Thème")
    with connect_db() as conn:
        themes = conn.execute("SELECT ID, Theme FROM Themes").fetchall()
    id_theme = st.selectbox("Thème à supprimer", themes, format_func=lambda x: x[1])
    if st.button("Supprimer"):
        with connect_db() as conn:
            c = conn.cursor()
            c.execute("DELETE FROM Themes WHERE ID = ?", (id_theme[0],))
            conn.commit()
            st.success("Thème supprimé avec succès.")

def main():
    st.title("🧠 Flashcards Interactives")
    menu = ["Réviser", "Ajouter une flashcard", "Afficher les cartes par thème", "Ajouter un thème", "Supprimer un thème", "Statistiques", "Débogage Probabilités"]
    choix = st.sidebar.radio("Menu", menu)
    if choix == "Réviser":
        show_flashcards()
    elif choix == "Ajouter une flashcard":
        add_flashcard()
    elif choix == "Afficher les cartes par thème":
        show_cards_by_theme()
    elif choix == "Ajouter un thème":
        add_theme()
    elif choix == "Supprimer un thème":
        delete_theme()
    elif choix == "Statistiques":
        show_stats()
    elif choix == "Débogage Probabilités":
        debug_card_probabilities()

if __name__ == "__main__":
    init_db()
    main()