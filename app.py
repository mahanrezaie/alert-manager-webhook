from flask import Flask, request, jsonify
import os
import json
import telebot
from datetime import datetime
import dotenv

dotenv.load_dotenv()
app = Flask(__name__)

# BOT_TOKEN is a .env, you can set it yourself
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

def send_message(chat_id, data):
    bot.send_message(chat_id, data)

def get_timestamp():
    return datetime.now().strftime("%Y%m%d-%H:%M:%S")


@app.route("/webhook", methods=["POST"])
def webhook():
    # Validate Content-Type
    if not request.is_json:
        return jsonify({"error": "Invalid Content-Type, expecting JSON"}), 400

    time_stamp = get_timestamp()
    payload = request.get_json()
    alerts = payload.get("alerts", [])
    
    if not alerts:
        return jsonify({"message": "No alerts to process"}), 200

    for alert in alerts:
        labels = alert.get("labels", {})
        annotations = alert.get("annotations", {})
        
        # Extract required fields
        team = labels.get("team")
        severity = labels.get("severity")
        summary = annotations.get("summary")
        description = annotations.get("description")
        
        # Check if required fields are present
        if team and severity:
            # Define the file path
            directory = f"alerts/{team}"
            filename = f"{directory}/{severity}.json"
        
            # Create directory if it doesn't exist
            os.makedirs(directory, exist_ok=True)
        
            # Prepare the alert data to save
            alert_data = {
                "team": team,
                "severity": severity,
                "summary": summary,
                "description": description,
                "time_stamp": time_stamp
            }
            
            # Load existing alerts or create new list
            existing_alerts = []
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    existing_alerts = json.load(f)
            
            # Append new alert
            existing_alerts.append(alert_data)

            # Prepare message
            message = json.dumps(alert_data)
            # Send with bot
            chat_id = os.getenv("chat_id")
            send_message(chat_id, message)
            # Write to file
            with open(filename, "w") as f:
                json.dump(existing_alerts, f, indent=2)

    return jsonify({"message": "Alerts processed successfully"}), 200

if __name__ == "__main__":
    app.run(debug=True)          
