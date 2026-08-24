# Receipt Scanner da Webcam con Azure AI

## Descrizione

Il programma apre uno stream video dalla webcam con un riquadro guida a schermo per posizionare correttamente lo scontrino. Con un tasto lo scatta e lo ritaglia, poi invia l'immagine al modello preaddestrato `prebuilt-receipt` di Azure Document Intelligence, che riconosce ed estrae la lista dei prodotti acquistati, stampandoli a schermo.

## Funzionalità

-  Acquisizione live da webcam con riquadro guida per l'inquadratura
-  Ritaglio automatico dell'area dello scontrino al momento dello scatto
-  Salvataggio dell'immagine scattata su disco
-  Riconoscimento automatico dei prodotti tramite Azure AI Document Intelligence (modello `prebuilt-receipt`)
-  Stampa a schermo dei prodotti trovati

## Struttura del progetto

```
.
├── receipt_scanner.py    # Script principale: webcam + analisi scontrino
└── requirements.txt
```

## Requisiti

- Python 3.9+
- Una risorsa **Azure AI Document Intelligence** (ex Form Recognizer)

## Installazione

```bash
git clone https://github.com/<tuo-username>/<nome-repo>.git
cd <nome-repo>
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Configurazione

Crea un file `.env` nella root del progetto con le seguenti variabili:

```env
AZ_ENDPOINT=https://<il-tuo-endpoint>.cognitiveservices.azure.com
AZ_KEY=la-tua-chiave
```

## Utilizzo

```bash
python receipt_scanner.py
```

Inquadra lo scontrino all'interno del riquadro mostrato a schermo, poi:

- premi **S** per salvare lo scatto e avviare l'analisi
- premi **Q** per uscire senza scattare

I prodotti riconosciuti verranno stampati direttamente nel terminale.
