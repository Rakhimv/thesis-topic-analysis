import os
from flask import Flask, render_template, request, jsonify, send_from_directory
from search import find_advisors, get_advisor, ADVISOR_NAMES

app = Flask(__name__)
TEMPLATES_DIR = os.path.join(os.path.dirname(__file__), "templates")


def search_payload(query):
    return [
        {
            "name": a["name"],
            "rating": a["rating"],
            "main_topic": a["main_topic"],
            "in_topic": a["in_topic"],
            "pct": a["pct"],
            "total": a["total"],
            "matches": a["matches"],
        }
        for a in find_advisors(query)
    ]


@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    tab = request.args.get("tab", "search")
    advisor = request.args.get("advisor", "").strip()
    return render_template(
        "app.html",
        query=query,
        tab=tab,
        advisors=ADVISOR_NAMES,
        selected_advisor=advisor,
        advisor_profile=get_advisor(advisor) if advisor else None,
        search_results=find_advisors(query) if query else [],
    )


@app.route("/search")
def search():
    query = request.args.get("q", "").strip()
    return jsonify(search_payload(query))


@app.route("/bg.png")
def bg_image():
    return send_from_directory(TEMPLATES_DIR, "bg.png")


@app.route("/advisor")
def advisor():
    name = request.args.get("name", "").strip()
    profile = get_advisor(name)
    if not profile:
        return jsonify({"error": "не найден"}), 404
    return jsonify(profile)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
