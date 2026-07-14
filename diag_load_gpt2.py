from transformers import AutoModelForCausalLM, AutoTokenizer
import transformers, torch
print('transformers version:', transformers.__version__)
print('torch version:', torch.__version__)

try:
    tokenizer = AutoTokenizer.from_pretrained('gpt2')
    model = AutoModelForCausalLM.from_pretrained('gpt2')
    inputs = tokenizer('Create a Jatti hello program', return_tensors='pt')
    outputs = model.generate(**inputs, max_new_tokens=30)
    print('\n=== GENERATED ===')
    print(tokenizer.decode(outputs[0], skip_special_tokens=True))
except Exception as e:
    import traceback
    traceback.print_exc()
    print('ERROR:', e)
