# Sistema di Gestione delle Spese Personali e del Budget

Un'applicazione console in Python per gestire le spese personali, organizzarle per categoria, definire budget mensili e visualizzare report riepilogativi.

## Requisiti per l'Esecuzione

### Software Necessario

- **Python 3.x** (testato con Python 3.8+)
- **PostgreSQL** (versione 12 o superiore)
- **pip** (gestore pacchetti Python)

### Librerie Python

- `psycopg2` - Connettore PostgreSQL per Python

## Installazione

### 1. Installazione delle Dipendenze Python

Aprire il terminale nella cartella del progetto ed eseguire:

```bash
pip install -r requirements.txt
```

In alternativa, installare manualmente:

```bash
pip install psycopg2-binary
```

### 2. Configurazione del Database PostgreSQL

#### 2.1 Creare il Database

Accedere a PostgreSQL tramite terminale o pgAdmin e creare un nuovo database:

```sql
CREATE DATABASE spese_personali;
```

#### 2.2 Eseguire lo Script SQL

Connettersi al database appena creato ed eseguire lo script `database.sql`:

**Da terminale:**

```bash
psql -U postgres -d spese_personali -f database.sql
```

**Oppure da pgAdmin:**
1. Aprire pgAdmin
2. Connettersi al server PostgreSQL
3. Selezionare il database `spese_personali`
4. Aprire Query Tool
5. Caricare ed eseguire il file `database.sql`

### 3. Configurazione della Connessione

Aprire il file `main.py` e modificare i parametri di connessione nella sezione `DB_CONFIG` se necessario:

```python
DB_CONFIG = {
    'host': 'localhost',
    'database': 'spese_personali',
    'user': 'postgres',
    'password': 'postgres',  # Modificare con la propria password
    'port': '5432'
}
```

## Avvio del Programma

Aprire il terminale nella cartella del progetto ed eseguire:

```bash
python main.py
```

## Utilizzo

All'avvio, il programma presenta un menu principale con le seguenti opzioni:

1. **Gestione Categorie** - Inserire nuove categorie di spesa
2. **Inserisci Spesa** - Registrare una nuova spesa
3. **Definisci Budget Mensile** - Impostare un limite di spesa per categoria/mese
4. **Visualizza Report** - Accedere al sottomenu dei report
5. **Esci** - Chiudere il programma

### Formato dei Dati in Input

- **Data**: formato `YYYY-MM-DD` (es. `2025-01-15`)
- **Mese**: formato `YYYY-MM` (es. `2025-01`)
- **Importo**: numero decimale (es. `45.50`)

## Struttura del Progetto

```
Esame/
├── main.py              # Applicazione principale Python
├── database.sql         # Script SQL per creare le tabelle
├── requirements.txt     # Dipendenze Python
├── DOCUMENTAZIONE.md    # Documentazione del progetto (per PDF)
└── README.md            # Questo file
```

## Struttura del Database

Il sistema utilizza tre tabelle:

- **categorie** - Memorizza le categorie di spesa
- **spese** - Memorizza le singole spese registrate
- **budget** - Memorizza i limiti di spesa mensili per categoria

## Note

- Il database deve essere avviato prima di eseguire il programma
- I dati di esempio vengono inseriti automaticamente eseguendo `database.sql`
- Per un database vuoto, commentare le istruzioni INSERT nello script SQL
