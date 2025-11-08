import yaml

class ConfigLoader:
    @staticmethod
    def load_yaml(path: str):
        with open(path, "r") as file:
            return yaml.safe_load(file)

    @staticmethod
    def load_app_config():
        return ConfigLoader.load_yaml("config/app_config.yaml")

    @staticmethod
    def load_rules():
        app_config = ConfigLoader.load_app_config()
        rules_path = app_config["app"]["rules_file"]
        return ConfigLoader.load_yaml(rules_path)
