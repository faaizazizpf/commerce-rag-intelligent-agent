apt-get update

cd GLM-4

pip install -r /workspace/GLM-4/basic_demo/requirements.txt
rm -rf /workspace/hf_cache/ 
mkdir -p /workspace/hf_cache
export HF_HOME=/workspace/hf_cache
cd finetune_demo
pip install datasets peft tensorboard
pip install jieba==0.42.1
pip install datasets==2.20.0
pip install peft==0.12.2
pip install deepspeed==0.14.4
pip install nltk==3.8.1
pip install rouge_chinese==1.0.3
pip install ruamel.yaml==0.18.6
cd scripts

pip install flask flask-cors gunicorn pyngrok
pip install flask pyngrok transformers
pip install peft
pip install -U sentence-transformers
pip install pandas
pip install s3fs
pip install torch
pip install numpy
pip install faiss-cpu
pip install fastapi uvicorn jinja2
ngrok config add-authtoken 2lA2iAcA98ju3TaQznxR992ISuv_46Aiyx7HU5VcRHyzobE1h
pip uninstall transformers; pip install transformers==4.44.2
pip install fuzzywuzzy python-Levenshtein

pip freeze > project_requirements.txt
python3 requirement_check.py
xargs -a requirements.txt pip uninstall -y
pip install -r unmatched_requirements.txt 


rm -rf /workspace/hf_cache/
mkdir -p /workspace/hf_cache
export HF_HOME=/workspace/hf_cache
python3 dev_app.py
