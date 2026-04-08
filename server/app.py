from environment import FinanceEnv
from flask import Flask, request, jsonify

app = Flask(__name__)
env = FinanceEnv(seed=42)

@app.route("/")
def home():
    return """
    <h1>AI Finance Coach</h1>
    <button onclick="resetEnv()">Reset</button>
    <button onclick="stepEnv()">Step</button>
    <pre id="output"></pre>

    <script>
    async function resetEnv() {
        let res = await fetch('/reset', {method: 'POST'});
        let data = await res.json();
        document.getElementById('output').innerText = JSON.stringify(data, null, 2);
    }

    async function stepEnv() {
        let res = await fetch('/step', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({action: 1})
        });
        let data = await res.json();
        document.getElementById('output').innerText = JSON.stringify(data, null, 2);
    }
    </script>
    """

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

def main():
    app.run(host="0.0.0.0", port=7860)

if __name__ == "__main__":
    main()
