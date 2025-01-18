import yaml

# Load the YAML configuration
def load_yaml(file_path):
    with open(file_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

# Example usage
if __name__ == "__main__":
    yaml_file = ".env"
    config = load_yaml(yaml_file)

    # Access the DB configuration
    db_config = config.get("db", {})
    host = db_config.get("host")
    port = db_config.get("port")
    user = db_config.get("user")
    password = db_config.get("password")

    print(f"Host: {host}")
    print(f"Port: {port}")
    print(f"User: {user}")
    print(f"Password: {password}")
