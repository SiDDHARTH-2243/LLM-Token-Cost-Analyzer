from flask import Flask, request, jsonify, render_template
from core_logic import count_tokens, calculate_costs, PRICING_DATA

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_prompt():
    data = request.get_json()
    
    # Validation: Ensure both text and the expected output token count exist
    if not data or 'text' not in data or 'expected_output_tokens' not in data:
        return jsonify({"error": "Missing text or expected_output_tokens payload"}), 400
        
    text = data['text']
    try:
        # Cast to integer to prevent string concatenation in the math engine
        expected_output_tokens = int(data['expected_output_tokens'])
    except ValueError:
        return jsonify({"error": "Expected output tokens must be a valid integer"}), 400
        
    comparison_results = []
    
    try:
        for model_id in PRICING_DATA.keys():
            input_tokens = count_tokens(text, model_id)
            # Pass both parameters into the upgraded calculation module
            financials = calculate_costs(input_tokens, expected_output_tokens, model_id)
            comparison_results.append(financials)
            
        return jsonify({"comparisons": comparison_results}), 200
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)