# python
import random
import glob
import os
import sys

# --- 在这里手动修改参数（在 PyCharm 中直接编辑） ---
INPUT_PATH = "F:\Projects\LLM-LADE-Furthermore\dataset\Thunderbird\Thunderbird.log"      # 输入文件路径，若为 None 则使用当前目录第一个 .log 文件
NUM = 1000             # 要抽取的行数
SEED = 7838276            # 随机种子，设为 None 则不固定随机序列
# --------------------------------------------------------

def reservoir_sample(path, k, seed=None):
    if seed is not None:
        random.seed(seed)
    reservoir = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        for i, line in enumerate(f, start=1):
            if i <= k:
                reservoir.append(line)
            else:
                j = random.randrange(i)
                if j < k:
                    reservoir[j] = line
    return reservoir

def choose_default_log():
    logs = sorted(glob.glob("*.log"))
    return logs[0] if logs else None

def run(input_path=None, num=1000, seed=None):
    input_path = input_path or choose_default_log()
    if not input_path:
        raise FileNotFoundError("未找到 .log 文件，且未指定输入文件。")
    if not os.path.isfile(input_path):
        raise FileNotFoundError(f"输入文件不存在: {input_path}")

    sampled = reservoir_sample(input_path, num, seed)
    base = os.path.splitext(os.path.basename(input_path))[0]
    out_name = f"{base}_sampled_{len(sampled)}.log"
    out_path = os.path.join(os.getcwd(), out_name)
    with open(out_path, "w", encoding="utf-8") as out_f:
        out_f.writelines(sampled)
    print(f"已从 `{input_path}` 抽取 {len(sampled)} 行，保存为 `{out_path}`")
    return out_path

if __name__ == "__main__":
    run(INPUT_PATH, NUM, SEED)