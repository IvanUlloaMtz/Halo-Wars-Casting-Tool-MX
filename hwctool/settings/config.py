import json
import os
import logging

logger = logging.getLogger('root')

class ConfigManager:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.default_config = {
            "websocket_port": 7305,
            "http_port": 8000,
            "language": "es",
            "hotkeys": {
                "show_intro_p1": "F5",
                "show_intro_p2": "F6",
                "toggle_score": "F7",
                "reset_all": "F8"
            },
            "assets_path": "casting_html/src/assets",
            "obs_browser_source_paths": {
                "intro": "casting_html/intro.html",
                "score": "casting_html/score.html"
            }
        }
        self.config = self.load_config()

    def load_config(self):
        if not os.path.exists(self.config_file):
            logger.info("Archivo de configuracion no encontrado. Creando uno nuevo con valores por defecto.")
            self.save_config(self.default_config)
            return self.default_config
        
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # Merge with defaults to ensure all keys exist
                for key, value in self.default_config.items():
                    if key not in config:
                        config[key] = value
                return config
        except Exception as e:
            logger.error(f"Error cargando configuracion: {e}")
            return self.default_config

    def save_config(self, config=None):
        if config:
            self.config = config
        
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4)
            logger.info("Configuracion guardada correctamente.")
        except Exception as e:
            logger.error(f"Error guardando configuracion: {e}")

    def get(self, key, default=None):
        return self.config.get(key, default)

    def set(self, key, value):
        self.config[key] = value
        self.save_config()
