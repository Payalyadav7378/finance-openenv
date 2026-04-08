import random
import numpy as np

class FinanceEnv:
    def __init__(self, seed=42):
        random.seed(seed)
        np.random.seed(seed)
        self.reset()

    def reset(self):
        self.state_data = {
            "balance": 5000.0,
            "monthly_income": random.uniform(2000, 5000),
            "expenses": random.uniform(1500, 3000),
            "savings": 2000.0,
            "debt": random.uniform(1000, 5000),
            "month": 0
        }
        self.done = False
        return self.state()

    def state(self):
        return np.array(list(self.state_data.values()), dtype=np.float32)

    def step(self, action):
        reward = 0

        income = self.state_data["monthly_income"]
        expenses = self.state_data["expenses"]

        self.state_data["balance"] += income - expenses

        if random.random() < 0.2:
            emergency = random.uniform(500, 2000)
            self.state_data["balance"] -= emergency
            reward -= emergency * 0.5

        if action == 1:
            amt = self.state_data["balance"] * 0.2
            self.state_data["savings"] += amt
            self.state_data["balance"] -= amt
            reward += amt * 0.3

        elif action == 2:
            amt = self.state_data["balance"] * 0.3
            gain = amt * random.uniform(-0.1, 0.2)
            self.state_data["balance"] += gain
            reward += gain

        elif action == 3:
            pay = min(self.state_data["balance"], self.state_data["debt"] * 0.3)
            self.state_data["debt"] -= pay
            self.state_data["balance"] -= pay
            reward += pay * 0.5

        elif action == 4:
            spend = random.uniform(200, 1000)
            self.state_data["balance"] -= spend
            reward -= spend

        if self.state_data["balance"] < 0:
            reward -= 1000

        net_worth = self.state_data["balance"] + self.state_data["savings"] - self.state_data["debt"]
        reward += net_worth * 0.01

        self.state_data["month"] += 1
        if self.state_data["month"] >= 12:
            self.done = True

        return self.state(), reward, self.done, {}
