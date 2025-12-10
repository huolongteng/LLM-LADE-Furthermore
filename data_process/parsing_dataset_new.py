from logparser.Drain import LogParser


def main():
    input_dir = r"F:\Projects\LLM-LADE-Furthermore\dataset\BGL"
    output_dir = r"F:\Projects\LLM-LADE-Furthermore\dataset\BGL"
    log_file = "BGL.log"

    log_format = '<Date> <Time> <Level>:<Content>'  # Define log format to split message fields
    # Regular expression list for optional preprocessing (default: [])
    regex = [
        r'(/|)([0-9]+\.){3}[0-9]+(:[0-9]+|)(:|)'  # IP
    ]

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

    parser.parse(log_file)


if __name__ == "__main__":
    main()
