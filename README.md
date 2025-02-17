
# Nostr Console Client 🔍

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue?logo=python)](https://www.python.org/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Nostr NIPs](https://img.shields.io/badge/Nostr-NIPs-green)](https://github.com/nostr-protocol/nips)

Ein feature-reicher Terminal-Client für das Nostr-Netzwerk mit folgenden Funktionen:

✨ **Features**:
- 🗝️ Schlüsselgenerierung & -import/export
- 📨 Nachrichtenversand mit NIP-07 Signatur
- 🔍 Event-Subscriptions
- 🌐 Multi-Relay Support
- 📂 Persistente Speicherung


## 📦 Installation

### Voraussetzungen
- Python 3.10 oder höher
- pip Paketmanager

### Schritt-für-Schritt
1. Repository klonen:
```bash
git clone https://github.com/dein-username/nostr-client-console).git
cd nostr-client-console)
```

2. Virtuelle Umgebung erstellen (empfohlen):
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows
```

3. Abhängigkeiten installieren:
```bash
pip install -r requirements.txt
```

## 🛠️ Verwendung

### Starten des Clients
```bash
python src/nostr-client.py
```

### Hauptmenü-Übersicht
```
[1] Schlüssel verwalten      [5] Profil bearbeiten
[2] Relays anzeigen         [6] Gruppen verwalten
[3] Nachricht senden        [7] Follower-Liste
[4] Nachrichtenarchiv       [8] Abmelden
[0] Beenden
```

![Bildschirmfoto vom 2025-02-17 22-02-58](https://github.com/user-attachments/assets/4fc8e479-96ee-4bdd-a5db-820ff9bb39a1)
![Bildschirmfoto vom 2025-02-17 22-03-54](https://github.com/user-attachments/assets/fbfe62f2-a0c3-4b80-b93c-f4e20bff70aa)




### Schlüsselverwaltung 🔑
- **Neue Schlüssel generieren**: Erstellt neues Schlüsselpaar mit Benutzernamen
- **Schlüssel speichern**: Exportiert Schlüssel als verschlüsselte JSON-Datei
- **Schlüssel laden**: Importiert bestehende Schlüssel aus Datei

Beispiel:
```bash
# Nach dem Start:
1  # Schlüsselverwaltung auswählen
1  # Neue Schlüssel generieren
Benutzername: nostr-fan123
```

### Nachrichtenversand ✉️
- Versenden von öffentlichen Nachrichten (Kind 1 Events)
- Automatische Signierung mit ECDSA
- Multi-Relay-Unterstützung

```
Auswahl: 3
Gib deine Nachricht ein: Hallo Nostr-Community! 👋
```

## 🌟 Hauptfunktionen

### Kernfeatures
- ✅ Schlüsselgenerierung (secp256k1 ECDSA)
- 📨 Nachrichtenversand mit automatischer Signatur
- 🌐 Multi-Relay-Unterstützung
- 🔐 Lokale Schlüsselspeicherung (AES-256 verschlüsselt)
- 🎨 Farbige Terminaloberfläche

### Erweiterte Features
- 📂 Persistente Speicherung von:
  - Schlüsselpaaren
  - Nachrichtenverlauf
  - Relay-Konfiguration
- 👥 Follower-Verwaltung
- 📝 Profilbearbeitung (NIP-05 kompatibel)
- ⏱️ Automatisches Nachrichten-Archiv

## 🔧 Technische Details

### Unterstützte Relays
Standardmäßig konfigurierte Relays:
- `wss://nos.lol`
- `wss://damus.io`
- `wss://relay.damus.io`
- `wss://offchain.pub`

### Dateistruktur
```bash
nostr-client-console)/
├── src/
│   ├── nostr-client.py      # Hauptanwendung
│   └── requirements.txt     # Abhängigkeiten
├── docs/                    # Dokumentation & Screenshots
├── .gitignore               # Ignorierte Dateien
├── LICENSE                  MIT-Lizenz
└── README.md                Diese Datei
```

### Sicherheitshinweise 🔒
- Schlüssel werden **niemals unverschlüsselt** gespeichert
- AES-256 Verschlüsselung für lokale Speicherung
- Private Keys verbleiben immer lokal

## 🤝 Mitwirken

Wir freuen uns über Beiträge! So geht's:

1. Repository forken
2. Feature-Branch erstellen:
```bash
git checkout -b feature/mein-tolles-feature
```
3. Änderungen committen
4. Push zum Branch:
```bash
git push origin feature/mein-tolles-feature
```
5. Pull Request öffnen

### Anerkannte Beiträge
- [ ] Gruppen-Chat-Funktion (NIP-28)
- [ ] Direktnachrichten-Verschlüsselung (NIP-04)
- [ ] Relay-Benchmarking

## 📜 Lizenz

Dieses Projekt steht unter der MIT-Lizenz

---

**Hinweis**: Dies ist ein Entwicklungsprojekt und sollte nicht für sensible Daten verwendet werden.


