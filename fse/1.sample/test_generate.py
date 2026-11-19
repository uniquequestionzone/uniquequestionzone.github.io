import json
import html

# Test basic generation logic
with open('solutions_dict.json', 'r', encoding='utf-8') as f:
    sols = json.load(f)
print(f"Loaded solutions for {len(sols)} questions.")
