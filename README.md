# LLM Token & Cost Shock Analyzer

A lightweight, strictly modular Flask API and web interface designed to calculate the exact financial cost of executing large system prompts across multiple LLMs. 

## The Problem
Standard token calculators only measure input length. In reality, LLM APIs charge asymmetrical rates, where Output Tokens cost 3x to 5x more than Input Tokens. Furthermore, certain models dynamically scale their base rates depending on the context window size. Failing to calculate these variables results in severe "cost shock" at scale.

## The Solution
This analyzer evaluates a single prompt against multiple models simultaneously, factoring in asymmetrical input/output rates and edge-case context thresholds (e.g., Gemini's >128k token rate doubling) to provide a mathematically rigorous cost projection.

## Core Features
* **Multi-Model Execution:** Compares GPT-4o, Claude 3.5 Sonnet, and Gemini 1.5 Pro instantly.
* **Asymmetrical Math Engine:** Calculates total transaction cost based on expected generation length, not just input size.
* **Context-Aware Tiering:** Automatically detects if a prompt breaches the 128,000 token threshold for Gemini and doubles the rate dynamically according to Google's official API pricing matrix.
* **Strict Modularity:** The tokenization and mathematical logic (`core_logic.py`) is entirely decoupled from the Flask routing (`app.py`), allowing for easy command-line testing or future database integration.

## Architecture
* **Backend:** Python 3, Flask
* **Tokenization:** `tiktoken` (uses `o200k_base` and `cl100k_base` proxy encodings)
* **Frontend:** Vanilla HTML/JS (No bloated frameworks, zero dependencies)

## Local Installation & Execution

1. **Clone the repository and navigate to the directory:**
   ```bash
   cd LLM_Token_Cost_Analyzer