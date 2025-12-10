# parsing_dataset_new.py

import os
import csv
import pandas as pd

# ------------------------------------------------------------
# 方案 1：最省事的热修（monkey patch）
# ------------------------------------------------------------
_orig_to_csv = pd.DataFrame.to_csv

def _to_csv_with_escape(self, *args, **kwargs):
    """
    Hotfix for:
        _csv.Error: need to escape, but no escapechar set

    Some versions of logparser.Drain call pandas to_csv with
    quoting=csv.QUOTE_NONE but without escapechar.
    This patch adds a default escapechar in that specific case.
    """
    if kwargs.get("quoting") == csv.QUOTE_NONE and "escapechar" not in kwargs:
        kwargs["escapechar"] = "\\"
    return _orig_to_csv(self, *args, **kwargs)

pd.DataFrame.to_csv = _to_csv_with_escape


# ------------------------------------------------------------
# Drain parsing
# ------------------------------------------------------------
from logparser.Drain import LogParser


def main():
    input_dir = r"F:\Projects\LLM-LADE-Furthermore\dataset\BGL"
    output_dir = r"F:\Projects\LLM-LADE-Furthermore\dataset\BGL"
    log_file = "BGL.log"

    # 确保目录存在
    os.makedirs(output_dir, exist_ok=True)

    log_format = "<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>"
    regex = [r"\d+\.\d+\.\d+\.\d+"]  # IP

    st = 0.5
    depth = 4

    parser = LogParser(
        log_format,
        indir=input_dir,
        outdir=output_dir,
        depth=depth,
        st=st,
        rex=regex
    )

    # 你仍然可以保留这个设置（有的版本会用到）
    parser.csv_kwargs = {
        "quoting": csv.QUOTE_ALL,
        "doublequote": True,
        "escapechar": "\\",  # 即使没被内部使用，也无害
    }

    parser.parse(log_file)


if __name__ == "__main__":
    main()
