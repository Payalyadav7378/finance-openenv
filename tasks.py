from environment import FinanceEnv

def easy_task(env):
    env.reset()
    for _ in range(12):
        env.step(1)
    nw = env.state_data["balance"] + env.state_data["savings"] - env.state_data["debt"]
    return min(max(nw / 20000, 0), 1)

def medium_task(env):
    env.reset()
    for _ in range(12):
        if env.state_data["debt"] > 2000:
            action = 3
        else:
            action = 1
        env.step(action)
    nw = env.state_data["balance"] + env.state_data["savings"] - env.state_data["debt"]
    return min(max(nw / 20000, 0), 1)

def hard_task(env):
    env.reset()
    for _ in range(12):
        if env.state_data["debt"] > 3000:
            action = 3
        elif env.state_data["balance"] > 3000:
            action = 2
        else:
            action = 1
        env.step(action)
    nw = env.state_data["balance"] + env.state_data["savings"] - env.state_data["debt"]
    return min(max(nw / 25000, 0), 1)
