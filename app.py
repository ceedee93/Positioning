import streamlit as st
import datetime

st.set_page_config(page_title="Positioning Service Übersetzer", page_icon="🎯", layout="centered")
st.title("🎯 Query-Generator für das Positioning Panel")
st.write("Wähle deine Filter auf Deutsch aus. Unten erhältst du den fertigen Code, den du direkt in das Feld 'Filterausdruck' im Positioning Query Panel kopieren kannst.")

st.markdown("---")

# --- 1. Eingaben (Business-Logik) ---
st.subheader("1. Was möchtest du filtern?")

col1, col2 = st.columns(2)
with col1:
    rohstoff = st.selectbox("Rohstoff (Commodity)", ["Alle", "Strom (Power)", "Gas", "Emissionen"])
    richtung = st.selectbox("Richtung (Direction)", ["Alle", "Kauf (Buy)", "Verkauf (Sell)"])

with col2:
    # Wir nutzen Text-Inputs für die unscharfe Suche (~)
    partner = st.text_input("Handelspartner (OtherParty)", placeholder="z.B. aachen (auch Teilworte ok)")
    portfolio = st.text_input("Portfolio", placeholder="z.B. Eigenhandel")

st.markdown("---")
st.subheader("2. Erweiterte Filter (Optional)")
vertragsart = st.selectbox("Vertragsart (ContractType)", ["Alle", "Standard", "Non-Standard", "Bilateral"])
intern_extern = st.radio("Interne oder Externe Deals?", ["Alle", "Nur Intern (Internal = true)", "Nur Extern (Internal = false)"])

st.markdown("---")

# --- 2. Logik-Generierung für das Positioning Query Panel ---
st.subheader("📋 Dein fertiger Filterausdruck")
st.write("Kopiere diesen Text und füge ihn im Positioning Query Panel unten links bei 'Filterausdruck' ein:")

logik_teile = []

# Rohstoff
if rohstoff == "Strom (Power)":
    logik_teile.append("Commodity ~ 'power'") # Wir nutzen ~ für unscharfe Suche, das ist sicherer
elif rohstoff == "Gas":
    logik_teile.append("Commodity ~ 'gas'")
elif rohstoff == "Emissionen":
    logik_teile.append("Commodity ~ 'emission'")

# Richtung
if richtung == "Kauf (Buy)":
    logik_teile.append("Direction = 'BUY'")
elif richtung == "Verkauf (Sell)":
    logik_teile.append("Direction = 'SELL'")

# Textfelder (Wir nutzen den ~ Operator, wie im Handbuch empfohlen!)
if partner:
    # Entfernt führende/nachfolgende Leerzeichen und macht es klein (sicherer bei ~)
    partner_clean = partner.strip().lower() 
    logik_teile.append(f"OtherParty ~ '{partner_clean}'")

if portfolio:
    logik_teile.append(f"Portfolio ~ '{portfolio.strip()}'")

# Erweiterte Filter
if vertragsart != "Alle":
    logik_teile.append(f"ContractType ~ '{vertragsart}'")

if intern_extern == "Nur Intern (Internal = true)":
    logik_teile.append("Internal = true") # Booleans brauchen oft keine Anführungszeichen, abhängig vom System. Ggf. 'true'
elif intern_extern == "Nur Extern (Internal = false)":
    logik_teile.append("Internal = false")

# --- 3. Ausgabe ---
if not logik_teile:
    st.info("Du hast noch keine Filter gesetzt. Das Panel zeigt dir aktuell ALLE Daten an.")
    ausgabe_text = ""
else:
    # Wir verbinden alle Teile mit " AND "
    ausgabe_text = " AND \n".join(logik_teile)
    
    # Ausgabe in einem schönen Code-Block, bereit zum Kopieren
    st.code(ausgabe_text, language="sql")

st.markdown("---")
st.write("**Tipp zum Zeitbereich:** Den Zeitraum musst du direkt oben im Panel (über dem Filterausdruck) einstellen. Denke daran, zwischen 'Kalendertagen' (Strom) und 'Gastagen' (Gas) zu unterscheiden, falls das für euch relevant ist!")
