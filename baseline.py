from environment import FinanceEnv
from tasks import easy_task, medium_task, hard_task

env = FinanceEnv(seed=42)

print({
    "easy": easy_task(env),
    "medium": medium_task(env),
    "hard": hard_task(env)
})
