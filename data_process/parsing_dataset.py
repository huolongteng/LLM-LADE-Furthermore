from logparser.Drain import LogParser
import os

DEFAULT_ST = 0.5
DEFAULT_DEPTH = 4

CONFIGS = {
    "HDFS": {
        "log_file": "HDFS.log",  # 按你的真实文件名改
        # 基于你给的样例行推断的最常见 HDFS 头格式
        "log_format": "<Date> <Time> <Pid> <Level> <Component>: <Content>",
        # 常用的动态字段预处理（块ID、IP/端口）
        "regex": [
            r"blk_-?\d+",
            r"(/|)(\d+\.){3}\d+(:\d+)?"
        ],
    },
    "BGL": {
        "log_file": "BGL.log",
        # 基于样例的一个合理拆分（每个占位符对应一个“按空格分隔”的token）
        # 你可以把字段名当作列名用；关键是最后要有 <Content>
        "log_format": "<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>",
        "regex": [
            r"\d+\.\d+\.\d+\.\d+",   # 以防日志中有IP
        ],
    },
    "Thunderbird": {
        "log_file": "Thunderbird.log",
        # 你的例子里有 syslog 风格的 "Nov 10 00:15:07"
        # 用 <Month> <Day> <Time> 三个占位符拆开最稳
        "log_format": "<Label> <Timestamp> <Date> <Host> <Month> <Day> <Time> <Location> <Component>: <Content>",
        "regex": [
            r"(/|)(\d+\.){3}\d+(:\d+)?",  # 有些行可能含IP
        ],
    },
}

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
    run_one("BGL", "F:\Projects\LLM-LADE-Furthermore\dataset\BGL", "F:\Projects\LLM-LADE-Furthermore\dataset\BGL")
    run_one("HDFS", "F:\Projects\LLM-LADE-Furthermore\dataset\HDFS_v1", "F:\Projects\LLM-LADE-Furthermore\dataset\HDFS_v1")
    run_one("Thunderbird", "F:\Projects\LLM-LADE-Furthermore\dataset\Thunderbird", "F:\Projects\LLM-LADE-Furthermore\dataset\Thunderbird")