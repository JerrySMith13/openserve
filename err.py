import os
from enum import Enum
import time
ERR_LOG_PATH = os.getenv("ERR_LOG_PATH")

class ErrLevel(Enum):
    Severe = "Severe",
    High = "High",
    Medium = "Medium",
    Low = "Low",

def panic(sig: int, msg: str):
    writeerr(msg, ErrLevel.Severe)
    print(f"Error: {msg}")
    exit(sig)

def writeerr(msg: str, level: ErrLevel):
    if ERR_LOG_PATH == None:
        print("Error: ERR_LOG_PATH not set")
        return
    file = open(ERR_LOG_PATH, "a")
    file.write(f"\n{str(ErrLevel.value)},{time.time()},{msg}")
    file.close()

