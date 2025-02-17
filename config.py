import yaml
import os
from pathlib import Path

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".nostr_client"
        self.config_file = self.config_dir / "config.yaml"
        self._ensure_config_exists()

    def _ensure_config_exists(self):
        self.config_dir.mkdir(exist_ok=True)
        
        if not self.config_file.exists():
            default_config = {
                'relays': [
                    'wss://nos.lol',
                    'wss://relay.damus.io'
                ],
                'logging': {
                    'level': 'INFO',
                    'max_size': 1048576  # 1MB
                }
            }
            self.save_config(default_config)

    def get_config(self):
        with open(self.config_file, 'r') as f:
            return yaml.safe_load(f)

    def save_config(self, config):
        with open(self.config_file, 'w') as f:
            yaml.safe_dump(config, f)