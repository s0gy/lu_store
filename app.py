from pathlib import Path

from flask import Flask, make_response, render_template, url_for


app = Flask(__name__)
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0


def asset_url(filename: str) -> str:
    static_file = Path(app.static_folder) / filename
    version = int(static_file.stat().st_mtime) if static_file.exists() else 0
    return url_for("static", filename=filename, v=version)


app.jinja_env.globals["asset_url"] = asset_url


@app.route("/")
def home():
    response = make_response(render_template("index.html"))
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)
