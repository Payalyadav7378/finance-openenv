from environment import FinanceEnv
from flask import Flask, request, jsonify

app = Flask(__name__)
env = FinanceEnv(seed=42)

def suggest_action():
    if env.state_data["debt"] > 3000:
        return "💳 Pay Debt"
    elif env.state_data["balance"] > 3000:
        return "📈 Invest"
    else:
        return "💵 Save"

@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>AI Finance Coach</title>
        <style>
            body { font-family: Arial; background: #f0f2f5; text-align: center; }
            .card { background: white; padding: 20px; margin: 15px; border-radius: 12px; display: inline-block; width: 200px; }
            button { padding: 10px 15px; margin: 5px; font-size: 15px; border-radius: 8px; }
            h1 { margin-top: 20px; }
        </style>
    </head>
    <body>
        <h1>💰 AI Finance Coach Dashboard</h1>

        <div>
            <button onclick="resetEnv()">🔄 Reset</button>
            <button onclick="stepEnv(1)">💵 Save</button>
            <button onclick="stepEnv(2)">📈 Invest</button>
            <button onclick="stepEnv(3)">💳 Pay Debt</button>
            <button onclick="stepEnv(4)">🛍 Spend</button>
        </div>

        <h2>🤖 Suggested Action: <span id="suggestion">-</span></h2>

        <div id="dashboard"></div>

        <script>
        function render(state, reward, done, suggestion) {
            let labels = ["Balance", "Income", "Expenses", "Savings", "Debt", "Month"];

            let html = "";
            for (let i = 0; i < state.length; i++) {
                html += `<div class="card"><h3>${labels[i]}</h3><p>${state[i]}</p></div>`;
            }

            html += `<div class="card"><h3>Reward</h3><p>${reward}</p></div>`;
            html += `<div class="card"><h3>Done</h3><p>${done}</p></div>`;

            document.getElementById("dashboard").innerHTML = html;
            document.getElementById("suggestion").innerText = suggestion;
        }

        async function resetEnv() {
            let res = await fetch('/reset', {method: 'POST'});
            let data = await res.json();
            updateUI();
        }

        async function stepEnv(action) {
            await fetch('/step', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({action: action})
            });
            updateUI();
        }

        async function updateUI() {
            let stateRes = await fetch('/state');
            let stateData = await stateRes.json();

            let sugRes = await fetch('/suggest');
            let sugData = await sugRes.json();

            render(stateData.state, "-", "-", sugData.suggestion);
        }

        updateUI();
        </script>
    </body>
    </html>
    """"

@app.route("/reset", methods=["POST"])
def reset():
    state = env.reset()
    return jsonify({"state": state.tolist()})

@app.route("/step", methods=["POST"])
def step():
    action = request.json.get("action", 0)
    state, reward, done, _ = env.step(action)
    return jsonify({
        "state": state.tolist(),
        "reward": reward,
        "done": done
    })

@app.route("/state", methods=["GET"])
def state():
    return jsonify({"state": env.state().tolist()})

@app.route("/suggest", methods=["GET"])
def suggest():
    return jsonify({"suggestion": suggest_action()})

def main():
    app.run(host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
