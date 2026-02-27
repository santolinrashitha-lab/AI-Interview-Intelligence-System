import pandas as pd
import os
from datetime import datetime

FILE_PATH = "data/interview_history.csv"

def save_result(role, experience, round_type, score):
    new_data = {
        "timestamp": datetime.now(),
        "role": role,
        "experience": experience,
        "round": round_type,
        "score": score
    }

    if os.path.exists(FILE_PATH):
        df = pd.read_csv(FILE_PATH)
        df = pd.concat([df, pd.DataFrame([new_data])], ignore_index=True)
    else:
        df = pd.DataFrame([new_data])

    df.to_csv(FILE_PATH, index=False)

def load_history():
    if os.path.exists(FILE_PATH):
        return pd.read_csv(FILE_PATH)
    else:
        return pd.DataFrame()
