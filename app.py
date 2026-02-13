import streamlit as st

# --- Design & Setup ---
st.set_page_config(page_title="Positioning Service Übersetzer", page_icon="🎯", layout="centered")
st.title("🎯 Query-Generator für das Positioning Panel")
st.write("Wähle deine Filter auf Deutsch aus. Unten erhältst du den fertigen Code für das Feld 'Filterausdruck' im Positioning Query Panel.")

st.markdown("---")

logik_teile = [] # Hier sammeln wir alle Bedingungen

# --- 1. Häufigste Filter (Immer sichtbar) ---
st.subheader("1. Wichtigste Filter (Standard)")
col1, col2 = st.columns(2)

with col1:
    rohstoff = st.selectbox("Rohstoff (Commodity)", ["Alle", "Power", "Gas", "Emission", "Coal", "Oil"])
    richtung = st.selectbox("Richtung (Direction)", ["Alle", "Kauf (BUY)", "Verkauf (SELL)"])

with col2:
    partner = st.text_input("Handelspartner (OtherParty)", placeholder="z.B. aachen (Teilworte ok)")
    portfolio = st.text_input("Portfolio", placeholder="z.B. Eigenhandel")

# Logik für Hauptfilter
if rohstoff != "Alle":
    logik_teile.append(f"Commodity ~ '(?i){rohstoff}'") # (?i) macht es komplett unabhängig von Groß-/Kleinschreibung
if richtung != "Alle":
    tech_richtung = "BUY" if "Kauf" in richtung else "SELL"
    logik_teile.append(f"Direction = '{tech_richtung}'")
if partner:
    logik_teile.append(f"OtherParty ~ '{partner.strip()}'")
if portfolio:
    logik_teile.append(f"Portfolio ~ '{portfolio.strip()}'")

# --- 2. Erweiterte Filter (Ausklappbar) ---
st.subheader("2. Erweiterte Filter (Klicken zum Ausklappen)")

# Kategorie: Vertrag & Produkt
with st.expander("📝 Vertrag & Produkt (Contract, Product...)"):
    c_ver1, c_ver2 = st.columns(2)
    with c_ver1:
        vertragstyp = st.selectbox("Vertragsart (ContractType)", ["Alle", "Standard", "Non-Standard", "Bilateral", "Broker", "Exchange"])
        produkt = st.text_input("Produkt (Product)", placeholder="z.B. Base, Peak, Q1-25")
    with c_ver2:
        preistyp = st.selectbox("Preistyp (PriceType)", ["Alle", "Fixed", "Float", "Indexed"])
        volumentyp = st.selectbox("Volumentyp (VolumeType)", ["Alle", "Fixed", "Profile", "Option"])
    
    if vertragstyp != "Alle": logik_teile.append(f"ContractType ~ '(?i){vertragstyp}'")
    if produkt: logik_teile.append(f"Product ~ '{produkt.strip()}'")
    if preistyp != "Alle": logik_teile.append(f"PriceType = '{preistyp}'")
    if volumentyp != "Alle": logik_teile.append(f"VolumeType = '{volumentyp}'")

# Kategorie: Markt & Lieferung
with st.expander("🌍 Markt & Lieferung (Market, Delivery...)"):
    c_markt1, c_markt2 = st.columns(2)
    with c_markt1:
        markt = st.text_input("Markt / Börse (Market / Exchange)", placeholder="z.B. EEX, OTC")
        marktgebiet = st.text_input("Marktgebiet (MarketArea)", placeholder="z.B. THE, NCG, Gaspool")
    with c_markt2:
        regelzone = st.text_input("Regelzone (ControlArea)", placeholder="z.B. Amprion, TenneT")
        lieferschema = st.text_input("Lieferschema (DeliveryScheme)", placeholder="z.B. Base, Peak")
    
    if markt: 
        logik_teile.append(f"(Market ~ '{markt.strip()}' OR Exchange ~ '{markt.strip()}')")
    if marktgebiet: logik_teile.append(f"MarketArea ~ '{marktgebiet.strip()}'")
    if regelzone: logik_teile.append(f"ControlArea ~ '{regelzone.strip()}'")
    if lieferschema: logik_teile.append(f"DeliveryScheme ~ '{lieferschema.strip()}'")

# Kategorie: Bilanzierung & Clearing
with st.expander("⚖️ Bilanzierung & Clearing (Balancing, Clearing...)"):
    c_clear1, c_clear2 = st.columns(2)
    with c_clear1:
        own_bkv = st.text_input("Eigener Bilanzkreis (OwnBalancingGroup)")
        other_bkv = st.text_input("Fremder Bilanzkreis (OtherBalancingGroup)")
    with c_clear2:
        clearing_house = st.text_input("Clearing House", placeholder="z.B. ECC")
        intern_extern = st.selectbox("Interne/Externe Deals", ["Alle", "Nur Intern", "Nur Extern"])
    
    if own_bkv: logik_teile.append(f"OwnBalancingGroup ~ '{own_bkv.strip()}'")
    if other_bkv: logik_teile.append(f"OtherBalancingGroup ~ '{other_bkv.strip()}'")
    if clearing_house: logik_teile.append(f"ClearingHouse ~ '{clearing_house.strip()}'")
    if intern_extern == "Nur Intern": logik_teile.append("Internal = true")
    if intern_extern == "Nur Extern": logik_teile.append("Internal = false")

# Kategorie: System & IDs
with st.expander("💻 System & IDs (DealId, CaptureSystem...)"):
    c_sys1, c_sys2 = st.columns(2)
    with c_sys1:
        deal_id = st.text_input("Deal-ID (DealId)", placeholder="Exakte ID oder Teil davon")
        system = st.text_input("Erfassungssystem (CaptureSystem)", placeholder="z.B. Trayport, Enmacc")
    with c_sys2:
        mandant = st.text_input("Mandant (Tenant)", placeholder="z.B. Trianel")
        ursprung = st.text_input("Ursprung (Origin)", placeholder="z.B. Import, Manual")

    if deal_id: logik_teile.append(f"DealId ~ '{deal_id.strip()}'")
    if system: logik_teile.append(f"CaptureSystem ~ '{system.strip()}'")
    if mandant: logik_teile.append(f"Tenant ~ '{mandant.strip()}'")
    if ursprung: logik_teile.append(f"Origin ~ '{ursprung.strip()}'")

# Kategorie: Numerische Werte
with st.expander("🔢 Mengen & Preise (Numerisch)"):
    st.write("Lass die Felder leer, wenn du nicht nach bestimmten Werten filtern willst.")
    c_num1, c_num2 = st.columns(2)
    with c_num1:
        min_preis = st.text_input("Mindestpreis (Price >=)", placeholder="z.B. 50.5")
        max_preis = st.text_input("Maximalpreis (Price <=)", placeholder="z.B. 120.0")
    with c_num2:
        min_menge = st.text_input("Mindestmenge MWh (TotalEnergyMWh >=)", placeholder="z.B. 100")
        max_menge = st.text_input("Maximalmenge MWh (TotalEnergyMWh <=)", placeholder="z.B. 5000")

    # Wir prüfen, ob die Eingabe nicht leer ist. Zahlen brauchen im System oft keine Anführungszeichen.
    if min_preis: logik_teile.append(f"Price >= {min_preis.replace(',', '.')}")
    if max_preis: logik_teile.append(f"Price <= {max_preis.replace(',', '.')}")
    if min_menge: logik_teile.append(f"TotalEnergyMWh >= {min_menge.replace(',', '.')}")
    if max_menge: logik_teile.append(f"TotalEnergyMWh <= {max_menge.replace(',', '.')}")


st.markdown("---")

# --- 3. Ausgabe ---
st.subheader("📋 Dein fertiger Filterausdruck")
st.write("Kopiere diesen Text und füge ihn im Positioning Query Panel bei 'Filterausdruck' ein:")

if not logik_teile:
    st.info("Du hast noch keine Filter gesetzt. Das Panel zeigt dir aktuell ALLE Daten an.")
    ausgabe_text = ""
else:
    # Wir verbinden alle Teile mit " AND " und machen Zeilenumbrüche für die Lesbarkeit
    ausgabe_text = " AND \n".join(logik_teile)
    
    # Ausgabe im Code-Block
    st.code(ausgabe_text, language="sql")

st.markdown("---")
st.caption("💡 **Tipp zur Suche:** Die Textsuche (wie Partner oder Markt) verzeiht Schreibfehler in der Groß-/Kleinschreibung. Wir nutzen im Hintergrund den Operator `~`, den das Handbuch empfiehlt.")
