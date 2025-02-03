from cases import * 
from fewshots import *
from pathlib import Path
from typing import Annotated, Union
import typer
from peft import PeftModelForCausalLM
from transformers import (
    AutoModel,
    AutoTokenizer,
)
from PIL import Image
import torch

app = typer.Typer(pretty_exceptions_show_locals=False)


def load_model_and_tokenizer(
        model_dir: Union[str, Path], trust_remote_code: bool = True
):
    model_dir = Path(model_dir).expanduser().resolve()
    if (model_dir / 'adapter_config.json').exists():
        import json
        with open(model_dir / 'adapter_config.json', 'r', encoding='utf-8') as file:
            config = json.load(file)
        model = AutoModel.from_pretrained(
            config.get('base_model_name_or_path'),
            trust_remote_code=trust_remote_code,
            device_map='auto',
            torch_dtype=torch.bfloat16
        )
        model = PeftModelForCausalLM.from_pretrained(
            model=model,
            model_id=model_dir,
            trust_remote_code=trust_remote_code,
        )
        tokenizer_dir = model.peft_config['default'].base_model_name_or_path
    else:
        model = AutoModel.from_pretrained(model_dir, trust_remote_code=trust_remote_code, device_map='auto', torch_dtype=torch.bfloat16)
        tokenizer_dir = model_dir
    tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir,
        trust_remote_code=trust_remote_code,
        encode_special_tokens=True,
        use_fast=False
    )
    return model, tokenizer


@app.command()
def main(
        model_dir: Annotated[str, typer.Argument(help='')],
):
    # For GLM-4 Finetune Without Tools
    
    model, tokenizer = load_model_and_tokenizer(model_dir)


    test_cases=fatima_sqa
    history=fewshots_history
    # while True:
    #     query = input()
        # if query.lower=="exit":
        #     break
    for query in test_cases: 
        if (len(history)-len(fewshots_history)>10):
            history1=history
            history=[]
            history = fewshots_history+history1[-10:]
            
        history.append(            {
                "role": "user", "content": query,
            })
        inputs = tokenizer.apply_chat_template(
            history,
            add_generation_prompt=True,
            tokenize=True,
            return_tensors="pt",
            return_dict=True
        ).to(model.device)

        generate_kwargs = {
            "max_new_tokens": 1024,
            "do_sample": True,
            "top_p": 0.8,
            "temperature": 0.8,
            "repetition_penalty": 1.2,
            "eos_token_id": model.config.eos_token_id,
        }
          
        
        outputs = model.generate(**inputs, **generate_kwargs)
        response = tokenizer.decode(outputs[0][len(inputs['input_ids'][0]):], skip_special_tokens=True).strip()
        print("=========")
        print("query: ",query)
        print("response: ",response)
        history.append({"role":"assistant","content":response})

if __name__ == '__main__':
    app()
