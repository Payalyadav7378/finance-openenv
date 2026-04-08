from environment import FinanceEnv
from flask import Flask, request, jsonify

app = Flask(__name__)
env = FinanceEnv(seed=42)

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

# ✅ REQUIRED main function
def main():
    app.run(host="0.0.0.0", port=7860)

# ✅ REQUIRED entrypoint
if __name__ == "__main__":
    main()
