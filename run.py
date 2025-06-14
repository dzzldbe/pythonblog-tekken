from pathlib import Path

from pythonblog import create_app

config_file = Path.cwd() / "pythonblog/config.py"

app = create_app(config_file)

if __name__ == "__main__":
    app.run(debug=False)
