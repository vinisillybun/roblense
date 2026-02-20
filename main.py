from flask import Flask, request, jsonify
import requests
import uuid

app = Flask(__name__)

# Store user sessions: uid -> { token, toys }
sessions = {}

LOVENSE_API = "https://api.lovense.com/api/lan/v2/command"
DEV_TOKEN = "f_dedqE0FLDS_Fg3FYcNlvw2MfWWQxLq0zGTWHqeocaVja0PXV56OH1aLA80ZFjm0FYEnsYygmW1oDeEi8MsIg"

@app.route("/")
def index():
    return jsonify({"status": "roblense server running"})

# Step 1: Generate a link for user to connect their toy
@app.route("/link", methods=["GET"])
@app.route("/link", methods=["GET"])
def link():
    uid = request.args.get("uid")
    if not uid:
        return jsonify({"error": "missing uid"}), 400

    r = requests.post("https://api.lovense.com/api/lan/getQrCode", json={
        "token": DEV_TOKEN,
        "uid": uid,
        "uname": uid,
        "utoken": str(uuid.uuid4()),
        "v": 2
    })

    data = r.json()
    print(f"[roblense] Lovense response: {data}")  # add this
    return jsonify(data)  # return the whole thing so we can see it

    return jsonify({
        "qr": data.get("message"),
        "uid": uid
    })

# Step 2: Lovense calls this when user connects
@app.route("/callback", methods=["POST"])
def callback():
    uid = request.args.get("uid")
    data = request.json
    if uid and data:
        sessions[uid] = {
            "token": data.get("utoken"),
            "toys": data.get("toys", {})
        }
        print(f"[roblense] User {uid} connected with toys: {list(sessions[uid]['toys'].keys())}")
    return "ok", 200

# Step 3: Roblox calls this to send commands
@app.route("/command", methods=["GET"])
def command():
    uid = request.args.get("uid")
    action = request.args.get("action")
    speed = request.args.get("v", "10")
    duration = request.args.get("sec", "5")

    if not uid or not action:
        return jsonify({"error": "missing uid or action"}), 400

    session = sessions.get(uid)
    if not session:
        return jsonify({"error": "user not connected, scan the link first"}), 404

    action_map = {
        "vibrate": "Vibrate",
        "rotate": "Rotate",
        "pump": "Pump",
        "thrust": "Thrust",
        "vibrate2": "Vibrate2",
        "stop": "Stop"
    }

    lovense_action = action_map.get(action.lower())
    if not lovense_action:
        return jsonify({"error": "unknown action"}), 400

    if lovense_action == "Stop":
        payload = {
            "token": DEV_TOKEN,
            "uid": uid,
            "command": "Function",
            "action": "Stop",
            "timeSec": 0,
            "apiVer": 1
        }
    else:
        payload = {
            "token": DEV_TOKEN,
            "uid": uid,
            "command": "Function",
            "action": f"{lovense_action}:{speed}",
            "timeSec": int(duration),
            "apiVer": 1
        }

    r = requests.post(LOVENSE_API, json=payload)
    return jsonify(r.json())

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
