from pathlib import Path

from pythonblog import create_app

config_file = Path(__file__).resolve().parent / "pythonblog/config.py"

app = create_app(config_file)

if __name__ == "__main__":
    app.run(debug=False)
