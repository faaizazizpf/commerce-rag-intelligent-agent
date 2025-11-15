# commerce-rag-intelligent-agent

A small repository for running a finetune / demo stack for an e-commerce retrieval-augmented-generation (RAG) intelligent agent. The repo contains scripts to prepare an environment, download model weights, and run a demo web app. My contributions are limited to the files under `finetune_demo/scripts` (I run the commands contained in `configAndRun.sh` to provision and prepare a GPU instance and download the necessary model artifacts).

WARNING: The supplied scripts install many system packages, clone large model checkpoints and repositories, and remember to setup your own ngrok (for example an ngrok authtoken is to be replaced with yours). Review and remove any secrets before running on a shared or public machine.

## Repository layout (relevant)
- finetune_demo/
  - scripts/  ← My contributions; contains automation,finetuning, implementing RAG, data preparation for training, testing and validation, and provisioning commands (e.g. `configAndRun.sh`)
  - basic_demo/, finetune_demo/, etc. (model and demo code)
- configAndRun.sh — script that provisions environment, installs dependencies, downloads models and runs the demo app (provided content shown below).

## What this repo does
- Sets up a Linux environment (installs packages, Python, Chrome + webdriver) and Python dependencies.
- Installs git-lfs and pulls large model files from Hugging Face and other public repos.
- Configures Hugging Face cache location (HF_HOME) to a workspace cache folder.
- Installs and pins a number of Python libraries used by the finetuning/demo stack.
- Starts the demo app (`dev_app.py`) at the end of the script (runs a Flask/pyngrok or local server).

The script is designed to run on a freshly created GPU VM so it can download and host model checkpoints locally.

## Quickstart (one-shot script)
The repository includes a bootstrap script (contents excerpted from `configAndRun.sh`). It performs many destructive/privileged operations (apt installs, dpkg, cloning big repos, etc.). Only run this on a clean VM you control.

Example (on a fresh Ubuntu GPU VM):
1. Clone this repository:
   git clone https://github.com/faaizazizpf/commerce-rag-intelligent-agent.git
   
2. Review `configAndRun.sh` and remove any dummy secrets (eg. ngrok auth token) or replace with your own. 
a. Run `configAndRun.sh` should run project root folder

3. Make it executable and run:
   chmod +x configAndRun.sh
   ./configAndRun.sh

Notes:
- The script will:
  - apt-get update, install system packages (python3, pip, chrome, etc.)
  - install git-lfs then clone large model repo(s)
  - set HF_HOME to `/workspace/hf_cache` and recreate that directory
  - pip install a long list of packages (some pinned); uninstall/install sequences may happen
  - download THUDM/glm-4-9b-chat and Finetuned_ecommerce_chatbot_public (renamed to GLM-4)
  - attempt to start the demo app (`python3 dev_app.py`) at the end
- Expect long run time and tens to hundreds of GBs of disk used when downloading model checkpoints.

## Recommended environment
- Ubuntu 20.04/22.04 (or other Debian-based)
- GPU with sufficient VRAM for the model(s) you plan to run (9B parameter model requires a substantial amount of memory or model parallel/deepspeed config).
- At least 100–500 GB disk depending on which model checkpoints you download.
- A user account with sudo privileges.
- Internet access to clone GitHub and Hugging Face repos.

## Important security & cost considerations
- Remove or rotate any tokens hard-coded in scripts (ngrok authtoken shown in the example is sensitive).
- Cloning large models and running them locally may be expensive—be mindful of cloud costs.
- The script runs apt and dpkg commands and installs packages globally; consider using a disposable VM or container (Docker) instead.

## How I contributed
- My only contributions in this repo are in `finetune_demo/scripts` — I run the commands in the `configAndRun.sh` file on the GPU instance to set up the environment and download models. I did not author model code; I automate environment provisioning and downloads.

## Troubleshooting
- If apt/dpkg fails during Chrome installation, run:
  sudo apt --fix-broken install -y
  sudo dpkg -i google-chrome-stable_current_amd64.deb
- If pip dependency conflicts occur, create a fresh virtual environment:
  python3 -m venv .venv
  source .venv/bin/activate
  pip install --upgrade pip
  pip install -r project_requirements.txt
- If Hugging Face downloads fail, ensure HF_HOME or cache path has enough free disk space and you have network access.
- If a model is too large for your GPU, consider:
  - Using model sharding / sharded checkpoints
  - Using CPU inference (very slow) or smaller models
  - Using a managed inference endpoint or multi-GPU instance

## Suggested improvements
- Move sensitive tokens into environment variables or a secrets manager; do not commit them to scripts.
- Convert installation and provisioning to a Dockerfile + docker-compose or Terraform to standardize environments and ease reproducibility.
- Add a requirements file with pinned, minimal dependencies and a dedicated virtualenv or conda environment step.
- Provide an optional interactive setup script that asks for tokens and desired model downloads rather than embedding values.

## License
This repository contains multiple third-party model artifacts and code. Check each subproject (e.g., THUDM GLM-4, Finetuned_ecommerce_chatbot_public) for their license terms and comply when using or redistributing.

## Contact / Author
- Repository owner: @faaizazizpf
- My contributions are limited to `finetune_demo/scripts` where I run `configAndRun.sh` to provision the GPU instance and download models.

