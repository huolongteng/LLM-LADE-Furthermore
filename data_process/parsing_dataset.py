from logparser.Drain import LogParser
import os
import csv
import pandas as pd

# These defaults follow the original Drain paper and reference
# implementation, and they are widely used as a starting point for
# general log parsing tasks.
DEFAULT_ST = 0.5
DEFAULT_DEPTH = 4

CONFIGS = {
    "HDFS": {
        "log_file": "HDFS.log",  # 按你的真实文件名改
        # 按模板头部顺序：Date, Time, Pid, Level, Component, Content
        "log_format": "<Date> <Time> <Pid> <Level> <Component>: <Content>",
        # 常用的动态字段预处理（块ID、IP/端口）
        "regex": [
            r"blk_-?\d+",
            r"(/|)(\d+\.){3}\d+(:\d+)?",
        ],
    },
    "BGL": {
        "log_file": "BGL.log",
        # 模板列：Label, Timestamp, Date, Node, Time, NodeRepeat, Type, Component, Level, Content
        "log_format": "<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>",
        "regex": [
            r"\d+\.\d+\.\d+\.\d+",  # 以防日志中有IP
        ],
    },
    "Thunderbird": {
        "log_file": "Thunderbird.log",
        # 模板列：Label, Timestamp, Date, User, Month, Day, Time, Location, Component, PID, Content
        # Thunderbird 日志中有的行带有 [PID]，有的只有组件名，使用冒号作为统一分隔
        # 例如：
        # - 1147034081 2006.05.07 dn642 May 7 13:34:41 dn642/dn642 ntpd[2266]: synchronized to 10.100.26.250, stratum 3
        # - 1136887631 2006.01.10 bn971 Jan 10 02:07:11 bn971/bn971 kernel: <...>
        # 因此将组件字段调整为简单的“<Component>:”，以兼容带/不带 PID 的情况。
        "log_format": "<Label> <Timestamp> <Date> <User> <Month> <Day> <Time> <Location> <Component>: <Content>",
        "regex": [
            r"(/|)(\d+\.){3}\d+(:\d+)?",  # 有些行可能含IP
        ],
    },
}

# Some log lines include double quotes, and certain versions of pandas
# require an explicit escape character when CSV quoting is disabled
# (e.g., when quoting=csv.QUOTE_NONE). We patch DataFrame.to_csv to ensure
# an escape character is always provided in that scenario to avoid
# "need to escape, but no escapechar set" errors during parsing.
_orig_to_csv = pd.DataFrame.to_csv


def _safe_to_csv(self, *args, **kwargs):
    if kwargs.get("quoting") == csv.QUOTE_NONE and "escapechar" not in kwargs:
        kwargs["escapechar"] = "\\"
    return _orig_to_csv(self, *args, **kwargs)


pd.DataFrame.to_csv = _safe_to_csv


def run_one(dataset: str, input_dir: str, output_dir: str):
    cfg = CONFIGS[dataset]
    os.makedirs(output_dir, exist_ok=True)

    parser = LogParser(
        cfg["log_format"],
        indir=input_dir,
        outdir=output_dir,
        depth=DEFAULT_DEPTH,
        st=DEFAULT_ST,
        rex=cfg.get("regex", []),
    )
    parser.parse(cfg["log_file"])


if __name__ == "__main__":
    # 按你的真实路径改
    # BGL和HDFS都OK
    run_one(
        "BGL",
        "F:\\Projects\\LLM-LADE-Furthermore\\dataset\\BGL",
        "F:\\Projects\\LLM-LADE-Furthermore\\dataset\\BGL"
    )
    run_one(
        "HDFS",
        "F:\\Projects\\LLM-LADE-Furthermore\\dataset\\HDFS_v1",
        "F:\\Projects\\LLM-LADE-Furthermore\\dataset\\HDFS_v1"
    )
    run_one(
        "Thunderbird",
        "F:\\Projects\\LLM-LADE-Furthermore\\dataset\\Thunderbird",
        "F:\\Projects\\LLM-LADE-Furthermore\\dataset\\Thunderbird",
    )
