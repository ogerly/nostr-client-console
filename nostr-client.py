import os
import json
import time
import asyncio
import hashlib
import websockets
from ecdsa import SigningKey, SECP256k1

# ANSI Farbcodes
COLOR_HEADER = "\033[95m"
COLOR_USER = "\033[94m"
COLOR_KEY = "\033[93m"
COLOR_RESET = "\033[0m"

DEFAULT_RELAYS = [
    "wss://pareto.space",
    "wss://pareto.nostr1.com",
    "wss://damus.io",
    "wss://nos.lol",
    "wss://offchain.pub",
    "wss://nostr.wine"
]

class KeyManager:
    def __init__(self):
        self.keys = {}
        self.profiles = {}

    def generate_keys(self, username):
        private_key = SigningKey.generate(curve=SECP256k1)
        public_key = private_key.get_verifying_key()
        
        self.keys[username] = {
            "private_key": private_key.to_string().hex(),
            "public_key": public_key.to_string("compressed").hex()
        }
        
        self.profiles[username] = {
            "display_name": username,
            "bio": "",
            "created": int(time.time())
        }
        return self.keys[username]

    def save_keys(self, username, path="."):
        if username not in self.keys:
            return False

        data = {
            "keys": self.keys[username],
            "profile": self.profiles[username]
        }

        os.makedirs(path, exist_ok=True)
        filename = os.path.join(path, f"{username}_nostr_keys.json")
        
        with open(filename, "w") as f:
            json.dump(data, f)
        return True

    def load_keys(self, username, path="."):
        filename = os.path.join(path, f"{username}_nostr_keys.json")
        
        try:
            with open(filename, "r") as f:
                data = json.load(f)
            
            self.keys[username] = data["keys"]
            self.profiles[username] = data["profile"]
            return True
        except Exception as e:
            print(f"Fehler beim Laden: {str(e)}")
            return False

    def update_profile(self, username, **kwargs):
        if username in self.profiles:
            self.profiles[username].update(kwargs)
            return True
        return False

class SettingsManager:
    def __init__(self):
        self.settings = {
            "relays": DEFAULT_RELAYS,
            "channels": [],
            "followers": [],
            "groups": {}
        }

    def add_follower(self, pubkey):
        if pubkey not in self.settings["followers"]:
            self.settings["followers"].append(pubkey)
            return True
        return False

    def join_group(self, group_id):
        if group_id not in self.settings["groups"]:
            self.settings["groups"][group_id] = {
                "joined": int(time.time()),
                "role": "member"
            }
            return True
        return False

class NostrClient:
    def __init__(self):
        self.key_manager = KeyManager()
        self.settings = SettingsManager()
        self.current_user = None
        self.messages = []

    def show_welcome(self):
        if self.current_user:
            pubkey = self.key_manager.keys[self.current_user]["public_key"]
            print(f"\n{COLOR_USER}★ Eingeloggt als {self.current_user} {COLOR_RESET}")
            print(f"{COLOR_KEY}Public Key: {pubkey}{COLOR_RESET}\n")

    def display_relays(self):
        print("\nRelay-Server Liste:")
        for i, relay in enumerate(self.settings.settings["relays"], 1):
            print(f"{i}. {relay}")

    def display_groups(self):
        print("\nGruppen:")
        for group_id, details in self.settings.settings["groups"].items():
            print(f"- {group_id} (Beigetreten: {time.ctime(details['joined'])})")

    def display_followers(self):
        print("\nFollower:")
        for follower in self.settings.settings["followers"]:
            print(f"- {follower[:12]}...{follower[-6:]}")

    async def profile_settings(self):
        if not self.current_user:
            return

        profile = self.key_manager.profiles[self.current_user]
        print("\nProfil Einstellungen:")
        print(f"1. Anzeigename: {profile['display_name']}")
        print(f"2. Bio: {profile['bio']}")
        print("3. Zurück")

        choice = input("Auswahl: ")
        if choice == "1":
            new_name = input("Neuer Anzeigename: ")
            self.key_manager.update_profile(self.current_user, display_name=new_name)
        elif choice == "2":
            new_bio = input("Neue Bio: ")
            self.key_manager.update_profile(self.current_user, bio=new_bio)

    async def send_public_message(self):
        if not self.current_user:
            print("Kein Benutzer ausgewählt!")
            return

        content = input("Gib deine Nachricht ein: ")
        if not content:
            print("Nachricht darf nicht leer sein!")
            return

        # Event erstellen
        event = {
            "pubkey": self.key_manager.keys[self.current_user]["public_key"],
            "created_at": int(time.time()),
            "kind": 1,
            "tags": [],
            "content": content
        }

        # Event signieren
        private_key = SigningKey.from_string(
            bytes.fromhex(self.key_manager.keys[self.current_user]["private_key"]),
            curve=SECP256k1
        )
        event_serialized = json.dumps([
            0,
            event["pubkey"],
            event["created_at"],
            event["kind"],
            event["tags"],
            event["content"]
        ], separators=(',', ':'), ensure_ascii=False)
        
        event_id = hashlib.sha256(event_serialized.encode()).hexdigest()
        signature = private_key.sign_digest(bytes.fromhex(event_id)).hex()

        event.update({
            "id": event_id,
            "sig": signature
        })

        # Sende an alle Relays
        for relay in self.settings.settings["relays"]:
            try:
                async with websockets.connect(relay) as ws:
                    await ws.send(json.dumps(["EVENT", event]))
                    try:
                        response = await asyncio.wait_for(ws.recv(), timeout=10)
                        print(f"Antwort von {relay}: {response}")
                    except asyncio.TimeoutError:
                        print(f"Timeout bei {relay}")
            except Exception as e:
                print(f"Fehler mit {relay}: {str(e)}")

        # Lokal speichern
        self.messages.append({
            "id": event_id,
            "content": content,
            "timestamp": event["created_at"],
            "relays": self.settings.settings["relays"]
        })
        self.save_messages()

    def save_messages(self):
        if self.current_user:
            filename = f"{self.current_user}_messages.json"
            with open(filename, "w") as f:
                json.dump(self.messages, f)

    def load_messages(self):
        if self.current_user:
            filename = f"{self.current_user}_messages.json"
            try:
                with open(filename, "r") as f:
                    self.messages = json.load(f)
            except FileNotFoundError:
                self.messages = []

    def display_messages(self):
        print("\nMeine Nachrichten:")
        for idx, msg in enumerate(self.messages, 1):
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(msg["timestamp"]))
            print(f"{idx}. [{timestamp}] {msg['content']}")
            print(f"   ID: {msg['id']}")
            print(f"   Relays: {', '.join(msg['relays'])}")
            print("-" * 50)

async def main_async():
    client = NostrClient()
    while True:
        print(f"\n{COLOR_HEADER}=== NOSTR CLIENT ==={COLOR_RESET}")
        
        # Login-Status Anzeige
        if client.current_user:
            pubkey_short = client.key_manager.keys[client.current_user]["public_key"][:6]+"..."+client.key_manager.keys[client.current_user]["public_key"][-4:]
            print(f"{COLOR_USER}Eingeloggt als: {client.key_manager.profiles[client.current_user]['display_name']}")
            print(f"Public Key: {pubkey_short}{COLOR_RESET}\n")
        else:
            print(f"{COLOR_KEY}Kein Benutzer eingeloggt{COLOR_RESET}\n")

        # Menüoptionen
        print(f"{COLOR_HEADER}Hauptmenü:{COLOR_RESET}")
        print("1. Schlüssel verwalten")
        print("2. Relay Liste anzeigen")
        
        if client.current_user:
            print("3. Nachricht senden")
            print("4. Meine Nachrichten")
            print("5. Profil verwalten")
            print("6. Gruppen anzeigen")
            print("7. Follower verwalten")
            print("8. Abmelden")
        else:
            print("3. Zum Einloggen bitte Schlüssel laden")
        
        print("0. Beenden")
        
        choice = input("\nAuswahl: ").strip()

        if choice == "1":
            await key_management_menu(client)
        elif choice == "2":
            client.display_relays()
        elif client.current_user:
            if choice == "3":
                await client.send_public_message()
            elif choice == "4":
                client.display_messages()
            elif choice == "5":
                await client.profile_settings()
            elif choice == "6":
                client.display_groups()
            elif choice == "7":
                print("Follower-Verwaltung noch nicht implementiert")
            elif choice == "8":
                client.current_user = None
                client.messages = []
                print("Erfolgreich abgemeldet!")
            elif choice == "0":
                print("Auf Wiedersehen!")
                break
            else:
                print("Ungültige Auswahl!")
        else:
            if choice == "3":
                print("\nBitte erst Schlüssel generieren oder laden (Menüpunkt 1)")
            elif choice == "0":
                print("Auf Wiedersehen!")
                break
            else:
                print("Ungültige Auswahl!")

async def key_management_menu(client):
    while True:
        print(f"\n{COLOR_HEADER}Schlüsselverwaltung:{COLOR_RESET}")
        print("1. Neue Schlüssel generieren")
        print("2. Schlüssel speichern")
        print("3. Schlüssel laden")
        print("4. Zurück zum Hauptmenü")
        
        choice = input("\nAuswahl: ").strip()

        if choice == "1":
            username = input("Gewünschten Benutzernamen eingeben: ").strip()
            if not username:
                print("Benutzername darf nicht leer sein!")
                continue
            if username in client.key_manager.keys:
                print("Benutzername bereits vergeben!")
                continue
                
            client.key_manager.generate_keys(username)
            client.current_user = username
            client.load_messages()
            print(f"\n{COLOR_USER}Neuer Account '{username}' wurde erstellt!{COLOR_RESET}")
            return
            
        elif choice == "2":
            if not client.current_user:
                print("Bitte erst einloggen!")
                continue
                
            path = input("Speicherpfad (leer für aktuelles Verzeichnis): ").strip() or "."
            client.key_manager.save_keys(client.current_user, path)
            print(f"\n{COLOR_KEY}Schlüssel gespeichert in:{COLOR_RESET}")
            print(f"{os.path.join(path, f'{client.current_user}_nostr_keys.json')}")
            
        elif choice == "3":
            username = input("Benutzername: ").strip()
            path = input("Pfad (leer für aktuelles Verzeichnis): ").strip() or "."
            
            if client.key_manager.load_keys(username, path):
                client.current_user = username
                client.load_messages()
                print(f"\n{COLOR_USER}Erfolgreich eingeloggt als {username}{COLOR_RESET}")
            else:
                print("\n⚠️  Fehler beim Laden der Schlüssel!")
                
        elif choice == "4":
            return
        else:
            print("Ungültige Auswahl!")

if __name__ == "__main__":
    asyncio.run(main_async())