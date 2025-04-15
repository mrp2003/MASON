# MASON — Multi-Agent System for Open No-Code Development

Welcome to the repository for **MASON**, a Multi-Agent LLM-based Framework for No-Code Software Generation. This system was developed to explore the effectiveness of multi-agent large language model (LLM) architectures in no-code environments, tested using algorithmic code generation tasks like MBPP and HumanEval.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Repository Structure](#repository-structure)
- [Installation & Setup](#installation--setup)
- [Datasets](#datasets)
- [Configuration](#configuration)
- [Running the Framework](#running-the-framework)
- [Results](#results)
- [Evaluation Summary](#evaluation-summary)
- [Agent Architecture](#agent-architecture)
- [Limitations & Future Work](#limitations--future-work)
---

## Project Overview

This project evaluates whether **multi-agent systems (MAS)** powered by large language models can outperform single-agent setups in a **no-code software development** environment.

Specifically, we introduce a custom multi-agent orchestration framework called **MASON**, built on top of [CrewAI](https://github.com/joaomdmoura/crewAI), and benchmark its performance across **Python generation benchmarks** including:

- **MBPP (Mostly Basic Python Problems)**  
- **HumanEval (from OpenAI)**

---

## Repository Structure

```plaintext
├── data/
│   ├── mbpp.jsonl            # MBPP dataset
│   └── humanEval.jsonl       # HumanEval dataset
├── src/mason_framework_sample/
│   ├── main.py               # Entry point for MASON
│   ├── crew.py               # Contains Crew/Agent definitions
│   ├── config/
│   │   ├── agents.yaml       # Defines agents (roles, goals)
│   │   └── tasks.yaml        # Defines tasks per benchmark
├── Results/
│   ├── Output/               # Raw output logs (.txt) from runs
│   └── Visualizations/       # Graphs comparing MAS vs Single LLM
├── .env                      # Environment variables
├── .gitignore
├── pyproject.toml            # Poetry dependencies
├── uv.lock                   # Dependency lock file
└── README.md                 # You're here!
```
---
## Installation & Setup

### 1. Clone the repository

```bash
git clone git@github.com:mrp2003/MASON.git
cd MASON
```
### 2. Set up Python environment

```bash
python -m venv .venv
source .venv/bin/activate
```
### 3. Install dependencies

```bash
pip install -r requirements.txt
```
### 4. Configure environment variables
Edit the `.env` file in the root folder and add:
```bash
MODEL=<your_model_name>
PROVIDER_API_KEY=<your_api_key>
```
---
## Datasets
Both datasets used in evaluation are included in the data/ folder:

- `mbpp.jsonl` (from Google Research)

- `humanEval.jsonl` (OpenAI benchmark)

Each contains task descriptions, function signatures, and unit tests. The framework automatically parses them and sends to the appropriate agent.

---
## Configuration
Agent and task settings can be customized under:

- `agents.yaml`
- `tasks.yaml`


Sample agent definition:

```yaml
researcher:
  role: >
    Senior Data Researcher
  goal: >
    Uncover cutting-edge developments in {topic}
  backstory: >
    You're a seasoned researcher with a knack for uncovering the latest developments in {topic}. Known for your ability to find the most relevant information and present it in a clear and concise manner.
```
Sample task definition:

```yaml
research_task:
  description: >
    Conduct a thorough research about {topic}
    Make sure you find any interesting and relevant information given the current year is 2025.
  expected_output: >
    A list with 10 bullet points of the most relevant information about {topic}
  agent: researcher
```

---
## Running the Framework
After configuring `tasks.yaml` and `agents.yaml`, run:

```bash
crewai run
```
---
## Results
### Output Files
Located in: `/Results/Output/`

Each `.txt` file contains:

- The task ID

- Number of Agent Interactions

- Execution time

- Pass/fail test case results


### Visualizations
Located in: `/Results/Visualizations/`

Includes:

- Pass@1 comparison bar charts

- Execution time plots

- Radar charts for strengths/weaknesses

- MAS vs Single-Agent performance graphs

---
## Evaluation Summary

We evaluated across the following metrics:

| **Metric**       | **Result Summary**                                       |
|------------------|----------------------------------------------------------|
| **Pass@1**       | MAS showed slight improvement over single LLM            |
| **Execution Time** | MAS incurs extra latency due to coordination           |
| **Accuracy Trend** | MAS better at longer, multi-line prompts               |
| **Stability**     | Open-source models underperformed vs Proprietary             |

---

## Agent Architecture

MASON operates using a **CrewAI-style sequential multi-agent system**, where each agent is assigned a specialized role in the code generation pipeline. These agents collaborate to transform natural language software requests into fully executable Python programs.

- ### Input Parsing Specialist
    Extracts actionable information from natural language prompts—such as desired functionality, required libraries, or constraints—to produce a structured, interpretable input for the next agent.

- ### Requirements Analysis Specialist
    Converts parsed input into a formalized software specification. This specification guides code generation by capturing the technical scope, logic flow, and functional expectations.

- ### Python Code Generator
    Translates the software specification into maintainable and well-structured Python code. Emphasizes clarity, modularity, and correctness in implementation.

- ### Code Validator
    Performs syntactic and runtime validation of the generated code to ensure it executes without errors. Catches exceptions, handles edge cases, and flags faulty logic.

- ### File Output Specialist
    Packages the validated Python code into a standalone .py file, ready for execution or deployment. Ensures correct formatting and proper structure for downstream use.

Each agent operates autonomously but in a predefined order, passing enriched context to the next role to ensure a cohesive and reliable workflow. This architecture allows for modularity, clarity in responsibility, and easier debugging across the generation process.

---
## Limitations & Future Work

- **Execution time** is significantly higher in MAS due to inter-agent communication.
- **Small LLMs** (e.g., DeepSeek 1.3B) struggled to maintain state across tasks.
- **Local execution** was sequential due to resource constraints (no GPUs).

### Future work includes:
- Designing lightweight MAS for small LLMs
- Exploring open-source orchestration alternatives (AutoGen, LangGraph)
- Incorporating agent learning from past tasks


