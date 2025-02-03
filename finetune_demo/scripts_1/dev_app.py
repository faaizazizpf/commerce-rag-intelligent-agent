from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import logging
from pathlib import Path
from transformers import AutoModel, AutoTokenizer
from peft import PeftModelForCausalLM
import torch
from datetime import datetime
from pyngrok import ngrok
import asyncio
import random
import json  # Add this line to fix the error
from fewshots import *
import threading
from ragResponse import *
import uvicorn
import requests
from utils import *

# Initialize FastAPI app
app = FastAPI()

@app.middleware("http")
async def log_requests(request: Request, call_next):
    log_with_pakistan_time(f"Received request: {request.method} {request.url}")
    response = await call_next(request)
    log_with_pakistan_time(f"Response status: {response.status_code}")
    return response

# CORS setup
origins = [
    "https://chatapp.codev360.com",
    "https://localhost",
    "https://larachat.test"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global model and tokenizer for GLM4
model_dir = Path("/workspace/GLM-4/finetune_demo/checkpoint-3000-v3")  # Update with your GLM4 model path
model = None
tokenizer = None
lock = threading.Lock()  # Lock for ensuring thread safety during model inference

def load_glm4_model_and_tokenizer():
    global model, tokenizer
    model_dir_resolved = model_dir.expanduser().resolve()

    if (model_dir_resolved / 'adapter_config.json').exists():
        with open(model_dir_resolved / 'adapter_config.json', 'r', encoding='utf-8') as file:
            config = json.load(file)
        base_model = AutoModel.from_pretrained(
            config.get('base_model_name_or_path'),
            trust_remote_code=True,
            device_map='auto',
            torch_dtype=torch.bfloat16
        )
        model = PeftModelForCausalLM.from_pretrained(
            model=base_model,
            model_id=model_dir_resolved,
            trust_remote_code=True
        )
        tokenizer_dir = model.peft_config['default'].base_model_name_or_path
    else:
        model = AutoModel.from_pretrained(model_dir_resolved, trust_remote_code=True, device_map='auto',
                                          torch_dtype=torch.bfloat16)
        tokenizer_dir = model_dir_resolved

    tokenizer = AutoTokenizer.from_pretrained(tokenizer_dir, trust_remote_code=True, use_fast=False)

load_glm4_model_and_tokenizer()

class QueryModel(BaseModel):
    query: str
    request_id: str
    user_history: list[dict]

def get_timestamp():
    return datetime.now().strftime("%S:%M:%H")

def trim_history_by_tokens(history, max_tokens=600):
    current_token_count = sum([len(tokenizer.encode(turn['content'])) for turn in history])
    while current_token_count > max_tokens:
        history.pop(0)  # Remove the oldest entry
        current_token_count = sum([len(tokenizer.encode(turn['content'])) for turn in history])
    return history

def trim_history_by_length(history, max_length=10):
    if len(history)>max_length:
        max_length=-max_length
        history=history[max_length:]
    return history

# Function to sanitize and validate history
def validate_and_sanitize_history(history: list[dict[str, str]]) -> list[dict[str, str]]:
    sanitized_history = []
    for turn in history:
        if 'role' in turn and 'content' in turn and turn['role'] in ['user', 'assistant']:
            sanitized_history.append(turn)
    return sanitized_history

def check_patterns_in_string(input_string):
    patterns = [r'Series', r'\-', r'\/', r'Rs\.']
    return any(re.search(pattern, input_string) for pattern in patterns)
    
@app.post("/get_response")
async def get_response(query_model: QueryModel):
    server_receive_time = get_timestamp()
    history = query_model.user_history
                # Validate and sanitize history
    user_history = validate_and_sanitize_history(query_model.user_history)

    # Trim history by token count
    user_history = trim_history_by_length(user_history)
    # fewshots_history=getFewshotsHistory(query_model.query)
    # logging.info("%"*40)
    # logging.info("User context history after trimming (i.e user_history):")
    # i=0
    # for message in user_history:
    #     i+=1
    #     logging.info(f"Message {i}:  {message['role']}: {message['content']}")        

    # logging.info("%"*40)
    context_history=user_history
    
    fewshots_history,string_match=getFewshotsHistory(query_model.query,user_history)
    logging.info("+"*40)
    logging.info(f"Against user query: {query_model.query}")
    logging.info(f"The string match fewshots was: {string_match}")        
    logging.info("+"*40)
    user_history = fewshots_history + user_history
    messages = user_history + [{"role": "user", "content": query_model.query}]
    

    # file1 = open(f"logs/logs_{get_pakistan_time_for_file()}.txt", "a+", encoding="utf-8") # append mode
    
    
    # # Log the history being sent to the model
    # log_with_pakistan_time("Logging History")
    
    # # file1.write(f"%"*150)
    # # file1.write(f"Starting of the Server Run{get_pakistan_time()}")
    # # file1.write(f"%"*150)

    # # for i, message in enumerate(messages):
    # #     logging.info(f"Message {i}: [{get_pakistan_time()}] {message['role']}: {message['content']}")        
    # #     file1.write(f"Message {i}: [{get_pakistan_time()}] {message['role']}: {message['content']}")
    # #     file1.write("\n")

    # logging.info("End of History")
        
    # Ensure that inference is thread-safe
    with lock:
        inputs = tokenizer.apply_chat_template(
            messages,
            add_generation_prompt=True,
            tokenize=True,
            return_tensors="pt",
            return_dict=True
        ).to(model.device)
        generate_kwargs = {
            "max_new_tokens": 256,
            "do_sample": True,
            "top_p": 0.8,
            "temperature": 0.8,
            "repetition_penalty": 1.2,
            "eos_token_id": model.config.eos_token_id,
        }

        outputs = model.generate(**inputs, **generate_kwargs)
        full_response = tokenizer.decode(outputs[0][len(inputs['input_ids'][0]):], skip_special_tokens=True).strip()

    # Handle empty response
    while len(full_response) < 10:
        outputs = model.generate(**inputs, **generate_kwargs)
        full_response = tokenizer.decode(outputs[0][len(inputs['input_ids'][0]):], skip_special_tokens=True).strip()
    # if "Haier" or "Rs." in full_response:
    # Example usage
    if(check_patterns_in_string(full_response)):  # Output: True
        # logging.info("[PRODUCT INFO FOUND IN QUERY]"*5)
        full_response=query_RAG_check(full_response)
    
    process_end_time = get_timestamp()

    # Update history with the response
    history.append({"role": "user", "content": query_model.query})
    history.append({"role": "assistant", "content": full_response})
    
    # Log the response
    # logging.info("[Q]" * 100)
    # logging.info(f"Received query: {query_model.query}")
    # logging.info("[R]" * 100)
    # logging.info(f"Response generated: {full_response}")

    # # file1.write(f"Starting of the Server Run{get_pakistan_time()}")
    # file1.write("[Q]" * 50)
    # file1.write(f"\nReceived query: {query_model.query} \n")
    # file1.write("[R]" * 50)
    # file1.write(f"\nResponse generated: {full_response} \n")

    # file1.close()
    len_allowed=len(fewshots_history)
    rag_items=fewshots_history[6:8]
    messages=rag_items+history
    write_history_csv(messages, query_model.query,full_response)

    return {
        "response": full_response,
        "server_receive_time": server_receive_time,
        "process_end_time": process_end_time,
        "updated_history": history,
        "request_id": query_model.request_id
    }

# Start NGROK
async def start_ngrok():
    file2 = open("link.txt", "w") # append mode
    tunnels = ngrok.get_tunnels()
    for tunnel in tunnels:
        ngrok.disconnect(tunnel.public_url)
    url = ngrok.connect(8000)
    public_url = url.public_url
    public_url=public_url+"/get_response"
    logging.info("\n\n\n\n====================================================================================")
    logging.info("model_dir: "+ str(model_dir))
    logging.info("====================================================================================\n\n\n\n")
    
    payload = {
        "url": public_url
    }

    # Send the POST request to the target URL
    target_url = "http://161.35.105.71/change-bot-url"
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.post(target_url, data=json.dumps(payload), headers=headers)
        # Log response status
        if response.status_code == 200:
            logging.info(f"Successfully sent the URL to {target_url}")
        else:
            logging.error(f"Failed to send the URL. Status code: {response.status_code}, Response: {response.text}")
    except Exception as e:
        logging.error(f"An error occurred while sending the URL: {e}")
    
    file2.write(f"%"*150)
    file2.write("public_url "+public_url)
    file2.write("target_url "+target_url)
    file2.write("response.status_code "+ str(response.status_code))
    file2.write(f"%"*150)
    
    file2.close()

    
    
    print(f"Ngrok tunnel established: {url}")
    return url

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    ngrok_url = loop.run_until_complete(start_ngrok())
    uvicorn.run(app, host="0.0.0.0", port=8000)
