from environment import FinanceEnv
from tasks import easy_task, medium_task, hard_task

def run_inference():
    env = FinanceEnv(seed=42)

    results = {
        "easy": round(easy_task(env), 3),
        "medium": round(medium_task(env), 3),
        "hard": round(hard_task(env), 3)
    }

    return results

if __name__ == "__main__":
    output = run_inference()
    print(output)
