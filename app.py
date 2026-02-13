import streamlit as st
import datetime

# --- Design & Setup ---
st.set_page_config(page_title="Abfrage-Übersetzer", page_icon="⚡", layout="centered")
st.title("⚡ Energie-Trading Abfrage-Übersetzer")
st.write("Klicke einfach an, was du wissen möchtest. Das Tool übersetzt deine Wünsche automatisch in die richtigen Datenbank-Felder für die IT.")

st.markdown("---")

# --- 1. Nutzereingaben (Business-Sicht) ---
st.subheader("1. Wen oder was suchst du?")
col1, col2 = st.columns(2)

with col1:
    rohstoff = st.selectbox("Welcher Rohstoff?", ["Alle", "Strom", "Gas", "Emissionen"])
    richtung = st.selectbox("Handelsrichtung?", ["Alle", "Kauf (Buy)", "Verkauf (Sell)"])

with col2:
    partner = st.text_input("Bestimmter Handelspartner? (Optional)", placeholder="z.B. Stadtwerke XYZ")
    portfolio = st.text_input("Bestimmtes Portfolio? (Optional)", placeholder="z.B. Base_Load_2026")

st.subheader("2. Welcher Zeitraum?")
zeitraum_typ = st.radio("Auf welches Datum bezieht sich die Abfrage?",
                        ["Lieferzeitraum (Wann fließt die Energie?)",
                         "Handelszeitpunkt (Wann wurde der Deal gemacht?)"])

start_datum = st.date_input("Startdatum", datetime.date.today())
end_datum = st.date_input("Enddatum", datetime.date.today() + datetime.timedelta(days=30))

st.subheader("3. Welche Informationen möchtest du im Ergebnis sehen?")
# Hier ordnen wir die deutschen Begriffe den technischen Feldern zu
auswahl_felder = {
    "Deal-Nummer": "DealId",
    "Partner-Name": "OtherParty / OtherPartyName",
    "Preis & Währung": "Price, Currency",
    "Gesamtmenge (MWh)": "TotalEnergyMWh",
    "Gesamtumsatz": "TotalTurnover",
    "Marktplatz / Börse": "Market / Exchange"
}

gewuenschte_spalten = st.multiselect(
    "Wähle die gewünschten Spalten für deine Tabelle:",
    options=list(auswahl_felder.keys()),
    default=["Deal-Nummer", "Preis & Währung", "Gesamtmenge (MWh)"]
)

st.markdown("---")

# --- 2. Übersetzung in IT-Logik (Das Herzstück) ---
st.subheader("🤖 Deine übersetzte IT-Abfrage")
st.write("Kopiere diese Logik für deine Datenbank-Abfrage oder gib sie an die IT weiter:")

# Logik-Baukasten
abfrage_logik = []

if rohstoff != "Alle":
    abfrage_logik.append(f"Commodity = '{rohstoff}'")

if richtung != "Alle":
    tech_richtung = "Buy" if "Kauf" in richtung else "Sell"
    abfrage_logik.append(f"Direction = '{tech_richtung}'")

if partner:
    abfrage_logik.append(f"OtherParty LIKE '%{partner}%'")

if portfolio:
    abfrage_logik.append(f"Portfolio LIKE '%{portfolio}%'")

# Datumslogik übersetzen
if "Lieferzeitraum" in zeitraum_typ:
    abfrage_logik.append(f"DeliveryStart >= '{start_datum}'")
    abfrage_logik.append(f"DeliveryEnd <= '{end_datum}'")
else:
    abfrage_logik.append(f"TransactionTime BETWEEN '{start_datum}' AND '{end_datum}'")

# Ausgabespalten übersetzen
technische_spalten = [auswahl_felder[spalte] for spalte in gewuenschte_spalten]

# Ausgabe schön formatieren
st.code(f"""
-- BENÖTIGTE SPALTEN (SELECT):
{', '.join(technische_spalten) if technische_spalten else '*'}

-- FILTER-KRITERIEN (WHERE):
{' AND '.join(abfrage_logik)}
""", language="sql")

st.success("Tipp: Du kannst diese Parameter jetzt direkt nutzen, um deine Daten im System zu filtern!")