import tiktoken

# Base Pricing Dictionary (Cost per 1,000,000 Tokens in USD)
PRICING_DATA = {
    "gpt-4o": {
        "input": 2.50,
        "output": 10.00
    },
    "claude-3.5-sonnet": {
        "input": 3.00,
        "output": 15.00
    },
    "gemini-1.5-pro": {
        "input": 1.25,
        "output": 5.00
    }
}

def count_tokens(text: str, model_id: str = "gpt-4o") -> int:
    """Calculates the exact or proxy token count of a given string."""
    try:
        if model_id == "gpt-4o":
            encoding = tiktoken.get_encoding("o200k_base")
        else:
            encoding = tiktoken.get_encoding("cl100k_base")
            
        return len(encoding.encode(text))
    except Exception as e:
        print(f"Tokenization error: {e}")
        return 0

def calculate_costs(input_tokens: int, output_tokens: int, model_id: str) -> dict:
    """
    Calculates asymmetrical costs, dynamically applying scale multipliers 
    for context window thresholds (e.g., Gemini >128k token scaling).
    """
    if model_id not in PRICING_DATA:
        raise ValueError(f"Model ID '{model_id}' not found.")
    
    # Extract base rates
    input_rate = PRICING_DATA[model_id]["input"]
    output_rate = PRICING_DATA[model_id]["output"]
    is_scaled_tier = False
    
    # Implement the 128k context tier trap for Gemini
    if model_id == "gemini-1.5-pro" and input_tokens > 128000:
        input_rate *= 2   # Scaled to $2.50
        output_rate *= 2  # Scaled to $10.00
        is_scaled_tier = True
    
    # Asymmetrical Math Engine Calculation
    input_cost = (input_tokens / 1_000_000) * input_rate
    output_cost = (output_tokens / 1_000_000) * output_rate
    
    total_cost_1_run = input_cost + output_cost
    total_cost_1000_runs = total_cost_1_run * 1000
    
    return {
        "model_selected": model_id,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "input_rate_per_1m": input_rate,
        "output_rate_per_1m": output_rate,
        "cost_1_run_usd": float(f"{total_cost_1_run:.6f}"),
        "cost_1000_runs_usd": float(f"{total_cost_1000_runs:.4f}"),
        "is_scaled_tier": is_scaled_tier
    }