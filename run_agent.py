import time
from adb_utils import setup_device
import logging
import os
from agent_wrapper import MiniCPMWrapper
import numpy as np
from PIL import Image

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s: %(message)s")


def run_task(query):
    device = setup_device()
    minicpm = MiniCPMWrapper(model_name='AgentCPM-GUI', temperature=1, use_history=True, history_size=2)
    
    is_finish = False
    while not is_finish:
        text_prompt = query
        screenshot = device.screenshot(1120)
        response = minicpm.predict_mm(text_prompt, [np.array(screenshot)])
        action = response[3]
        print(action)
        is_finish = device.step(action)
        time.sleep(2.5)
    return is_finish

if __name__ == "__main__":
    run_task("去哔哩哔哩看李子柒的最新视频，并且点赞。")

