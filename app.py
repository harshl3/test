from flask import Flask, jsonify

app = Flask(__name__)

# The fixed delivery schedule: street name -> (slot, tanker)
SCHEDULE = {
    "river road": ("06:30", "T1"),
    "market square": ("07:15", "T2"),
    "hill lane": ("08:00", "T1"),
}


@app.route("/")
def home():
    return "Tanker dispatch ready"


@app.route("/slot/<street>")
def slot(street):
    name = street.strip().lower()
    slot_time, tanker = SCHEDULE.get(name, ("unassigned", "none"))
    return jsonify({"street": name, "slot": slot_time, "tanker": tanker})


if __name__ == "__main__":
    app.run()
