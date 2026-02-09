# =============================================================================
# SISTEMA DI GESTIONE DELLE SPESE PERSONALI E DEL BUDGET
# =============================================================================
# Ho sviluppato questo programma per gestire le mie spese personali.
# Il sistema permette di registrare spese, organizzarle per categoria,
# definire budget mensili e visualizzare report riepilogativi.
# =============================================================================

import psycopg2
from psycopg2 import sql

# =============================================================================
# CONFIGURAZIONE DATABASE
# =============================================================================
# Qui definisco i parametri di connessione al database PostgreSQL.
# Modifico questi valori in base alla mia configurazione locale.

DB_CONFIG = {
    'host': 'localhost',
    'database': 'spese_personali',
    'user': 'postgres',
    'password': 'postgres',
    'port': '5432'
}

# =============================================================================
# FUNZIONE DI CONNESSIONE AL DATABASE
# =============================================================================
# Questa funzione stabilisce la connessione al database PostgreSQL.
# Restituisce l'oggetto connessione se la connessione ha successo,
# altrimenti stampa un messaggio di errore e restituisce None.

def connetti_database():
    """Stabilisco la connessione al database PostgreSQL."""
    try:
        connessione = psycopg2.connect(**DB_CONFIG)
        return connessione
    except psycopg2.Error as errore:
        print(f"Errore di connessione al database: {errore}")
        return None

# =============================================================================
# FUNZIONE PER VISUALIZZARE IL MENU PRINCIPALE
# =============================================================================
# Questa funzione visualizza il menu principale del sistema.

def mostra_menu_principale():
    """Visualizzo il menu principale del sistema."""
    print("\n" + "=" * 35)
    print("   SISTEMA SPESE PERSONALI")
    print("=" * 35)
    print("1. Gestione Categorie")
    print("2. Inserisci Spesa")
    print("3. Definisci Budget Mensile")
    print("4. Visualizza Report")
    print("5. Esci")
    print("=" * 35)

# =============================================================================
# MODULO 1 - GESTIONE CATEGORIE
# =============================================================================
# Questo modulo permette di inserire nuove categorie di spesa.
# Verifico che il nome non sia vuoto e che la categoria non esista già.

def gestione_categorie(connessione):
    """Gestisco l'inserimento di nuove categorie di spesa."""
    print("\n--- GESTIONE CATEGORIE ---")
    
    # Acquisisco il nome della categoria dall'utente
    nome_categoria = input("Inserisci il nome della categoria: ").strip()
    
    # Verifico che il nome non sia vuoto
    if not nome_categoria:
        print("Errore: il nome della categoria non può essere vuoto.")
        return
    
    try:
        cursore = connessione.cursor()
        
        # Verifico se la categoria esiste già nel database
        cursore.execute(
            "SELECT id_categoria FROM categorie WHERE LOWER(nome) = LOWER(%s)",
            (nome_categoria,)
        )
        
        if cursore.fetchone():
            print("La categoria esiste già.")
        else:
            # Inserisco la nuova categoria nel database
            cursore.execute(
                "INSERT INTO categorie (nome) VALUES (%s)",
                (nome_categoria,)
            )
            connessione.commit()
            print("Categoria inserita correttamente.")
        
        cursore.close()
        
    except psycopg2.Error as errore:
        print(f"Errore durante l'operazione: {errore}")
        connessione.rollback()

# =============================================================================
# MODULO 2 - INSERIMENTO SPESA
# =============================================================================
# Questo modulo permette di registrare una nuova spesa.
# Acquisisco data, importo, categoria e descrizione opzionale.

def inserisci_spesa(connessione):
    """Registro una nuova spesa nel sistema."""
    print("\n--- INSERIMENTO SPESA ---")
    
    # Acquisisco la data della spesa
    data = input("Inserisci la data (YYYY-MM-DD): ").strip()
    
    # Acquisisco l'importo della spesa
    try:
        importo = float(input("Inserisci l'importo: ").strip())
    except ValueError:
        print("Errore: l'importo deve essere un numero valido.")
        return
    
    # Verifico che l'importo sia maggiore di zero
    if importo <= 0:
        print("Errore: l'importo deve essere maggiore di zero.")
        return
    
    # Acquisisco il nome della categoria
    nome_categoria = input("Inserisci il nome della categoria: ").strip()
    
    # Acquisisco la descrizione (opzionale)
    descrizione = input("Inserisci una descrizione (opzionale): ").strip()
    if not descrizione:
        descrizione = None
    
    try:
        cursore = connessione.cursor()
        
        # Verifico che la categoria esista
        cursore.execute(
            "SELECT id_categoria FROM categorie WHERE LOWER(nome) = LOWER(%s)",
            (nome_categoria,)
        )
        risultato = cursore.fetchone()
        
        if not risultato:
            print("Errore: la categoria non esiste.")
            cursore.close()
            return
        
        id_categoria = risultato[0]
        
        # Inserisco la spesa nel database
        cursore.execute(
            "INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES (%s, %s, %s, %s)",
            (data, importo, id_categoria, descrizione)
        )
        connessione.commit()
        print("Spesa inserita correttamente.")
        
        cursore.close()
        
    except psycopg2.Error as errore:
        print(f"Errore durante l'operazione: {errore}")
        connessione.rollback()

# =============================================================================
# MODULO 3 - DEFINIZIONE BUDGET MENSILE
# =============================================================================
# Questo modulo permette di impostare un limite di spesa per una categoria
# in un determinato mese.

def definisci_budget(connessione):
    """Definisco un budget mensile per una categoria."""
    print("\n--- DEFINIZIONE BUDGET MENSILE ---")
    
    # Acquisisco il mese
    mese = input("Inserisci il mese (YYYY-MM): ").strip()
    
    # Acquisisco il nome della categoria
    nome_categoria = input("Inserisci il nome della categoria: ").strip()
    
    # Acquisisco l'importo del budget
    try:
        importo = float(input("Inserisci l'importo del budget: ").strip())
    except ValueError:
        print("Errore: l'importo deve essere un numero valido.")
        return
    
    # Verifico che l'importo sia maggiore di zero
    if importo <= 0:
        print("Errore: l'importo deve essere maggiore di zero.")
        return
    
    try:
        cursore = connessione.cursor()
        
        # Verifico che la categoria esista
        cursore.execute(
            "SELECT id_categoria FROM categorie WHERE LOWER(nome) = LOWER(%s)",
            (nome_categoria,)
        )
        risultato = cursore.fetchone()
        
        if not risultato:
            print("Errore: la categoria non esiste.")
            cursore.close()
            return
        
        id_categoria = risultato[0]
        
        # Inserisco o aggiorno il budget (uso INSERT ... ON CONFLICT UPDATE)
        cursore.execute("""
            INSERT INTO budget (mese, id_categoria, importo) 
            VALUES (%s, %s, %s)
            ON CONFLICT (mese, id_categoria) 
            DO UPDATE SET importo = EXCLUDED.importo
        """, (mese, id_categoria, importo))
        
        connessione.commit()
        print("Budget mensile salvato correttamente.")
        
        cursore.close()
        
    except psycopg2.Error as errore:
        print(f"Errore durante l'operazione: {errore}")
        connessione.rollback()

# =============================================================================
# MODULO 4 - VISUALIZZAZIONE REPORT
# =============================================================================
# Questo modulo visualizza un sottomenu per la scelta del tipo di report.

def mostra_menu_report():
    """Visualizzo il menu dei report disponibili."""
    print("\n" + "-" * 35)
    print("   MENU REPORT")
    print("-" * 35)
    print("1. Totale spese per categoria")
    print("2. Spese mensili vs budget")
    print("3. Elenco completo delle spese")
    print("4. Ritorna al menu principale")
    print("-" * 35)

def report_totale_per_categoria(connessione):
    """Visualizzo il totale delle spese raggruppate per categoria."""
    print("\n--- TOTALE SPESE PER CATEGORIA ---")
    
    try:
        cursore = connessione.cursor()
        
        # Eseguo la query per ottenere il totale per categoria
        cursore.execute("""
            SELECT c.nome, COALESCE(SUM(s.importo), 0) as totale
            FROM categorie c
            LEFT JOIN spese s ON c.id_categoria = s.id_categoria
            GROUP BY c.nome
            ORDER BY totale DESC
        """)
        
        risultati = cursore.fetchall()
        
        # Visualizzo i risultati in formato tabellare
        print("\n{:<20} {:>15}".format("Categoria", "Totale Speso"))
        print("-" * 35)
        
        for riga in risultati:
            categoria = riga[0]
            totale = riga[1]
            print("{:<20} {:>15.2f}".format(categoria, totale))
        
        cursore.close()
        
    except psycopg2.Error as errore:
        print(f"Errore durante l'operazione: {errore}")

def report_spese_vs_budget(connessione):
    """Confronto le spese mensili con il budget definito."""
    print("\n--- SPESE MENSILI VS BUDGET ---")
    
    try:
        cursore = connessione.cursor()
        
        # Ottengo tutti i budget definiti con le relative spese
        cursore.execute("""
            SELECT 
                b.mese,
                c.nome as categoria,
                b.importo as budget,
                COALESCE(SUM(s.importo), 0) as speso
            FROM budget b
            JOIN categorie c ON b.id_categoria = c.id_categoria
            LEFT JOIN spese s ON s.id_categoria = b.id_categoria 
                AND TO_CHAR(s.data, 'YYYY-MM') = b.mese
            GROUP BY b.mese, c.nome, b.importo
            ORDER BY b.mese, c.nome
        """)
        
        risultati = cursore.fetchall()
        
        if not risultati:
            print("Nessun budget definito.")
            cursore.close()
            return
        
        # Visualizzo i risultati con lo stato del budget
        for riga in risultati:
            mese = riga[0]
            categoria = riga[1]
            budget = riga[2]
            speso = riga[3]
            
            # Determino lo stato confrontando speso e budget
            if speso > budget:
                stato = "SUPERAMENTO BUDGET"
            elif speso == budget:
                stato = "BUDGET RAGGIUNTO"
            else:
                stato = "NEI LIMITI"
            
            print(f"\nMese: {mese}")
            print(f"Categoria: {categoria}")
            print(f"Budget: {budget:.2f}")
            print(f"Speso: {speso:.2f}")
            print(f"Stato: {stato}")
            print("-" * 30)
        
        cursore.close()
        
    except psycopg2.Error as errore:
        print(f"Errore durante l'operazione: {errore}")

def report_elenco_spese(connessione):
    """Visualizzo l'elenco completo delle spese ordinate per data."""
    print("\n--- ELENCO COMPLETO DELLE SPESE ---")
    
    try:
        cursore = connessione.cursor()
        
        # Ottengo tutte le spese ordinate per data
        cursore.execute("""
            SELECT s.data, c.nome, s.importo, COALESCE(s.descrizione, '-')
            FROM spese s
            JOIN categorie c ON s.id_categoria = c.id_categoria
            ORDER BY s.data
        """)
        
        risultati = cursore.fetchall()
        
        if not risultati:
            print("Nessuna spesa registrata.")
            cursore.close()
            return
        
        # Visualizzo i risultati in formato tabellare
        print("\n{:<12} {:<15} {:>10} {:<25}".format(
            "Data", "Categoria", "Importo", "Descrizione"))
        print("-" * 65)
        
        for riga in risultati:
            data = str(riga[0])
            categoria = riga[1]
            importo = riga[2]
            descrizione = riga[3]
            print("{:<12} {:<15} {:>10.2f} {:<25}".format(
                data, categoria, importo, descrizione))
        
        cursore.close()
        
    except psycopg2.Error as errore:
        print(f"Errore durante l'operazione: {errore}")

def visualizza_report(connessione):
    """Gestisco il sottomenu dei report."""
    while True:
        mostra_menu_report()
        scelta = input("Inserisci la tua scelta: ").strip()
        
        # Utilizzo una struttura simile allo switch per gestire la scelta
        if scelta == "1":
            report_totale_per_categoria(connessione)
        elif scelta == "2":
            report_spese_vs_budget(connessione)
        elif scelta == "3":
            report_elenco_spese(connessione)
        elif scelta == "4":
            # Ritorno al menu principale
            break
        else:
            print("Scelta non valida. Riprovare.")

# =============================================================================
# FUNZIONE PRINCIPALE
# =============================================================================
# Questa è la funzione principale che avvia il sistema.
# Gestisco il ciclo del menu principale fino a quando l'utente sceglie di uscire.

def main():
    """Funzione principale che avvia il sistema di gestione spese."""
    
    # Visualizzo il messaggio di benvenuto
    print("\n" + "=" * 50)
    print("   BENVENUTO NEL SISTEMA DI GESTIONE SPESE")
    print("=" * 50)
    
    # Stabilisco la connessione al database
    connessione = connetti_database()
    
    if not connessione:
        print("Impossibile avviare il sistema senza connessione al database.")
        return
    
    print("Connessione al database stabilita con successo.")
    
    # Ciclo principale del menu
    while True:
        mostra_menu_principale()
        scelta = input("Inserisci la tua scelta: ").strip()
        
        # Utilizzo una struttura simile allo switch per gestire la scelta
        if scelta == "1":
            gestione_categorie(connessione)
        elif scelta == "2":
            inserisci_spesa(connessione)
        elif scelta == "3":
            definisci_budget(connessione)
        elif scelta == "4":
            visualizza_report(connessione)
        elif scelta == "5":
            # Chiudo la connessione ed esco dal programma
            print("\nChiusura del sistema in corso...")
            connessione.close()
            print("Arrivederci!")
            break
        else:
            print("Scelta non valida. Riprovare.")

# =============================================================================
# PUNTO DI INGRESSO DEL PROGRAMMA
# =============================================================================
# Avvio il programma solo se questo file viene eseguito direttamente.

if __name__ == "__main__":
    main()
