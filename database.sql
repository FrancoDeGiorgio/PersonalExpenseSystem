-- =============================================================================
-- SCRIPT SQL PER IL SISTEMA DI GESTIONE SPESE PERSONALI E BUDGET
-- =============================================================================
-- Ho creato questo script per definire la struttura del database e inserire
-- alcuni dati di esempio per testare il funzionamento del sistema.
-- =============================================================================

-- Elimino le tabelle se esistono (per poter ricreare il database da zero)
DROP TABLE IF EXISTS spese CASCADE;
DROP TABLE IF EXISTS budget CASCADE;
DROP TABLE IF EXISTS categorie CASCADE;

-- =============================================================================
-- TABELLA CATEGORIE
-- =============================================================================
-- Questa tabella memorizza le categorie di spesa (es. Alimentari, Trasporti)
-- Ho definito i seguenti vincoli:
-- - PRIMARY KEY su id_categoria (identificatore univoco auto-incrementante)
-- - UNIQUE su nome (non possono esistere due categorie con lo stesso nome)
-- - NOT NULL su nome (il nome della categoria è obbligatorio)

CREATE TABLE categorie (
    id_categoria SERIAL PRIMARY KEY,
    nome VARCHAR(100) NOT NULL UNIQUE
);

-- =============================================================================
-- TABELLA SPESE
-- =============================================================================
-- Questa tabella memorizza tutte le spese registrate dall'utente
-- Ho definito i seguenti vincoli:
-- - PRIMARY KEY su id_spesa (identificatore univoco auto-incrementante)
-- - NOT NULL su data e importo (campi obbligatori)
-- - CHECK su importo (deve essere maggiore di zero)
-- - FOREIGN KEY su id_categoria (riferimento alla tabella categorie)

CREATE TABLE spese (
    id_spesa SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    importo DECIMAL(10, 2) NOT NULL CHECK (importo > 0),
    id_categoria INTEGER NOT NULL,
    descrizione VARCHAR(255),
    FOREIGN KEY (id_categoria) REFERENCES categorie(id_categoria)
);

-- =============================================================================
-- TABELLA BUDGET
-- =============================================================================
-- Questa tabella memorizza i limiti di spesa mensili per ogni categoria
-- Ho definito i seguenti vincoli:
-- - PRIMARY KEY su id_budget (identificatore univoco auto-incrementante)
-- - NOT NULL su mese, id_categoria e importo (campi obbligatori)
-- - CHECK su importo (deve essere maggiore di zero)
-- - FOREIGN KEY su id_categoria (riferimento alla tabella categorie)
-- - UNIQUE sulla combinazione (mese, id_categoria) per evitare duplicati

CREATE TABLE budget (
    id_budget SERIAL PRIMARY KEY,
    mese VARCHAR(7) NOT NULL,
    id_categoria INTEGER NOT NULL,
    importo DECIMAL(10, 2) NOT NULL CHECK (importo > 0),
    FOREIGN KEY (id_categoria) REFERENCES categorie(id_categoria),
    UNIQUE (mese, id_categoria)
);

-- =============================================================================
-- INSERIMENTO DATI DI ESEMPIO
-- =============================================================================
-- Inserisco alcune categorie, spese e budget di esempio per dimostrare
-- il funzionamento del sistema

-- Inserimento categorie di esempio
INSERT INTO categorie (nome) VALUES ('Alimentari');
INSERT INTO categorie (nome) VALUES ('Trasporti');
INSERT INTO categorie (nome) VALUES ('Intrattenimento');
INSERT INTO categorie (nome) VALUES ('Bollette');
INSERT INTO categorie (nome) VALUES ('Salute');

-- Inserimento spese di esempio per gennaio 2025
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES 
    ('2025-01-05', 45.50, 1, 'Spesa settimanale supermercato');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES 
    ('2025-01-10', 25.00, 1, 'Pranzo al ristorante');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES 
    ('2025-01-12', 35.00, 2, 'Abbonamento mensile autobus');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES 
    ('2025-01-15', 60.00, 1, 'Spesa settimanale supermercato');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES 
    ('2025-01-18', 15.00, 3, 'Cinema');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES 
    ('2025-01-20', 120.00, 4, 'Bolletta elettricità');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES 
    ('2025-01-22', 50.00, 1, 'Spesa settimanale supermercato');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES 
    ('2025-01-25', 30.00, 5, 'Farmacia');

-- Inserimento spese di esempio per febbraio 2025
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES 
    ('2025-02-03', 55.00, 1, 'Spesa settimanale supermercato');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES 
    ('2025-02-08', 20.00, 2, 'Taxi');
INSERT INTO spese (data, importo, id_categoria, descrizione) VALUES 
    ('2025-02-14', 40.00, 3, 'Cena di San Valentino');

-- Inserimento budget mensili di esempio
INSERT INTO budget (mese, id_categoria, importo) VALUES ('2025-01', 1, 200.00);
INSERT INTO budget (mese, id_categoria, importo) VALUES ('2025-01', 2, 50.00);
INSERT INTO budget (mese, id_categoria, importo) VALUES ('2025-01', 3, 100.00);
INSERT INTO budget (mese, id_categoria, importo) VALUES ('2025-01', 4, 150.00);
INSERT INTO budget (mese, id_categoria, importo) VALUES ('2025-02', 1, 200.00);
INSERT INTO budget (mese, id_categoria, importo) VALUES ('2025-02', 2, 50.00);

-- =============================================================================
-- FINE SCRIPT
-- =============================================================================
