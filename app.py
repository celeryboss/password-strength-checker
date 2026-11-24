from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

def check_password(password):
    score = 0

    if len(password) >= 8:
        score += 1

    if len(password) >= 12:
        score += 1

    if any(char.isupper() for char in password):
        score += 1

    if any(char.islower() for char in password):
        score += 1

    if any(char.isdigit() for char in password):
        score += 1

    if any(not char.isalnum() for char in password):
        score += 1

    if score < 3:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"

    char_space = 0
    if any(char.islower() for char in password):
        char_space += 26
    if any(char.isupper() for char in password):
        char_space += 26
    if any(char.isdigit() for char in password):
        char_space += 10
    if any(not char.isalnum() for char in password):
        char_space += 32

    combinations = char_space ** len(password) if char_space else 1
    guesses_per_second = 10_000_000_000
    seconds = combinations / 2 / guesses_per_second

    if seconds < 1:
        crack_time = "less than a second"
    elif seconds < 60:
        crack_time = f"{round(seconds)} seconds"
    elif seconds < 3600:
        crack_time = f"{round(seconds / 60)} minutes"
    elif seconds < 86400:
        crack_time = f"{round(seconds / 3600)} hours"
    elif seconds < 31536000:
        crack_time = f"{round(seconds / 86400)} days"
    elif seconds < 31536000 * 100:
        crack_time = f"{round(seconds / 31536000)} years"
    else:
        crack_time = "centuries"

    return {
        "score": score,
        "strength": strength,
        "crack_time": crack_time
    }

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check():
    data = request.get_json(silent=True) or {}
    password = data.get("password", "")
    return jsonify(check_password(password))

if __name__ == "__main__":
    app.run(debug=True)