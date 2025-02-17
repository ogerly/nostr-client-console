from core.network import RelayManager
from core.config import ConfigManager
from core.crypto import KeyManager

class NostrCLI:
    def __init__(self):
        self.config = ConfigManager()
        self.relay_mgr = RelayManager(self.config)
        self.key_mgr = KeyManager()
        
    async def start(self):
        await self.relay_mgr.connect_all()
        self.show_main_menu()

    def show_main_menu(self):
        print("Nostr Terminal Client")
        print("1. Nachricht senden")
        print("2. Relays verwalten")
        print("3. Schlüssel verwalten")
        print("4. Beenden")
        # ... Menülogik ...