# LLM-LADE: Large Language Model-based Log Anomaly Detection with Explanation

This repository contains the data process code, seed data, and LoRA adapter weights for **LLM-LADE**, a framework that formulates log anomaly detection as a multi-task generation problem. It jointly predicts anomaly labels and natural language explanations using a fine-tuned LLaMA3-8B model.

> 📄 For more details, please refer to our paper:  
> **LLM-LADE: Large Language Model-based Log Anomaly Detection with Explanation**  

---

## 🔧 Dataset Preparation

1. **Download original log datasets** from [LogHub](https://github.com/logpai/loghub):
   - HDFS
   - BGL
   - Thunderbird

2. **Parse logs using the Drain log parser**. Our LoRA weights are trained on data parsed by [Drain](https://github.com/logpai/logparser).

   - Clone the repository and install its dependencies (from the `logparser` root):
     ```bash
     git clone https://github.com/logpai/logparser.git
     cd logparser
     pip install -r requirements.txt
     ```

   - Run Drain from the `logparser` directory so relative imports work. Replace the paths below with your dataset locations. On
     Windows PowerShell, wrap arguments with quotes if the path contains spaces. The `-log_format` strings below match the
     example lines you provided:
     ```bash
     # HDFS
     python Drain.py \
       -log_file "F:\\Projects\\LLM-LADE-Furthermore\\dataset\\HDFS_v1\\HDFS.log" \
       -log_format "<Date> <Time> <Pid> <Level> <Component>: <Content>" \
       -out_file  "F:\\Projects\\LLM-LADE-Furthermore\\dataset\\HDFS_v1\\HDFS.log_structured.csv"

     # Example raw line: 081109 203518 143 INFO dfs.DataNode$DataXceiver: Receiving block blk_-1608999687919862906 ...

     # BGL
     python Drain.py \
       -log_file "F:\\Projects\\LLM-LADE-Furthermore\\dataset\\BGL\\BGL.log" \
       -log_format "<Label> <Timestamp> <Date> <Node> <Time> <Node2> <Content>" \
       -out_file  "F:\\Projects\\LLM-LADE-Furthermore\\dataset\\BGL\\BGL.log_structured.csv"

     # Example raw line: - 1117838570 2005.06.03 R02-M1-N0-C:J12-U11 2005-06-03-15.42.50.675872 R02-M1-N0-C:J12-U11 RAS KERNEL
     # INFO instruction cache parity error corrected

     # Thunderbird
     python Drain.py \
       -log_file "F:\\Projects\\LLM-LADE-Furthermore\\dataset\\Thunderbird\\Thunderbird.log" \
       -log_format "<Label> <Timestamp> <Date> <Node> <Content>" \
       -out_file  "F:\\Projects\\LLM-LADE-Furthermore\\dataset\\Thunderbird\\Thunderbird.log_structured.csv"

     # Example raw line: - 1131524107 2005.11.09 tbird-admin1 Nov 10 00:15:07 local@tbird-admin1 postfix/postdrop[10913]: warning:
     # unable to look up public/pickup: No such file or directory
     ```

   - The script does not print progress by default. Check that the `*.log_structured.csv` file is created/updated; if not, verify
     the `-log_format` matches your raw log lines and that you are inside the `logparser` folder when running `python Drain.py`.

3. **Run preprocessing** using our provided scripts:
   ```bash
   python data_process/hdfs_process.py         # For HDFS dataset
   python data_process/bgl_tbird_process.py    # For BGL and Thunderbird datasets

## 📦 LoRA Adapter Weights

We provide LoRA weights trained on three datasets:

- `model_weights/hdfs_lora/`
- `model_weights/bgl_lora/`
- `model_weights/thunderbird_lora/`

Each folder contains:

- `adapter_model.safetensors` – LoRA adapter weights
- `adapter_config.json` – LoRA configuration

These weights are trained on top of **LLaMA3-8B-Instruct**, and can be used for fine-tuning or inference via PEFT or LLaMA-Factory.

------

## 🧠 Base Model Requirement

Please download the official [Meta-LLaMA3-8B-Instruct model](https://huggingface.co/meta-llama/Meta-Llama-3-8B-Instruct/tree/main) from Hugging Face and agree to its license. The LoRA weights assume this model as the base.

------

## 🚀 Inference with LLaMA-Factory

You can use [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) to load and evaluate the model. specifying the version as 0.7.1.dev0.
