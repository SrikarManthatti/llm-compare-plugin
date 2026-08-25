# llm-compare-plugin

An LLM plugin that adds `llm compare` for running the same prompt against multiple models.

## Install

```bash
llm install llm-compare-plugin
```

For local development:

```bash
git clone https://github.com/SrikarManthatti/llm-compare-plugin.git
cd llm-compare-plugin
python -m venv .venv
source .venv/bin/activate
pip install -e ".[test]"
```

## Usage

```bash
llm compare -m model-a -m model-b "Explain Apache Spark"
```

Two models render side-by-side. Three or more render sequentially.

```bash
llm compare -m model-a -m model-b -m model-c "Explain Kafka"
```

JSON:

```bash
llm compare -m model-a -m model-b --json "Explain Spark"
```

System prompt:

```bash
llm compare -m model-a -m model-b -s "Answer as a senior data engineer" "Explain Spark"
```

Options:

```bash
llm compare -m model-a -m model-b -o temperature 0.2 "Explain Spark"
```