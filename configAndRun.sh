apt-get update
apt-get install git-lfs

git clone https://github.com/faaizazizpf/commerce-rag-intelligent-agent.git
mv commerce-rag-intelligent-agent GLM-4
cd GLM-4

pip install -r basic_demo/requirements.txt

git lfs install
git clone https://huggingface.co/THUDM/glm-4-9b-chat

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
ngrok config add-authtoken [your token]
pip uninstall -y transformers; pip install transformers==4.44.2
pip install fuzzywuzzy python-Levenshtein
pip install openpyxl

pip freeze > project_requirements.txt
python3 requirement_check.py
xargs -a to_uninstall_requirements.txt pip uninstall -y
pip install -r unmatched_requirements.txt


rm -rf /workspace/hf_cache/
mkdir -p /workspace/hf_cache
export HF_HOME=/workspace/hf_cache

pip install selenium
pip install webdriver_manager
apt update
apt upgrade -y
apt install python3 python3-pip -y
pip install --user selenium webdriver-manager
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
dpkg -i google-chrome-stable_current_amd64.deb
apt --fix-broken install
google-chrome --version
clear & python3 dev_app.py
