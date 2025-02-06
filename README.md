<a href="https://www.buymeacoffee.com/aadarshlalchandani"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=☕&slug=aadarshlalchandani&button_colour=5F7FFF&font_colour=ffffff&font_family=Cookie&outline_colour=000000&coffee_colour=FFDD00" /></a>&nbsp;&nbsp;&nbsp;<a href="https://www.producthunt.com/posts/aasetpy?embed=true&utm_source=badge-featured&utm_medium=badge&utm_souce=badge-aasetpy" target="_blank"><img src="https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=851410&theme=light&t=1738843824699" alt="aasetpy - Python&#0032;Project&#0032;Kickstarter&#0032;Template | Product Hunt" style="width: 250px; height: 54px;" width="250" height="54" /></a>

# `aasetpy`

![aasetpy release (latest by date)](https://img.shields.io/github/v/release/aadarshlalchandani/aasetpy?style=flat-square&color=blue&label=Release)
![aasetpy downloads](https://img.shields.io/github/downloads/aadarshlalchandani/aasetpy/total?color=success&label=Downloads)
![License](https://img.shields.io/badge/License-GNU%20GPL%203.0-orange.svg)

## `aasetpy` will create:
- Virtual Environment (`env/`)
- `.env` file to store environment variables
- Directory to store Execution Logs (`logs/`)
- Python Project Skeleton (`src/`)
- `utils/` module in `src/`
  > The `utils` module has annotations and environment variables ready to use
- `requirements.txt` with basic lightweight contents
  - ```txt
    coverage
    pytest
    pylint
    requests
    psutil
    pydantic
    pydantic-settings
    ```
- `.gitignore` with necessary contents
  - ```ini
    env/
    venv/
    *.log
    *.out
    __pycache__/
    .env
    .venv
    .vscode
    test.py
    ```
- `Dockerfile` as basic containerization of the project
- `docker.compose.yml` to build and run the docker project
- `README.md` with the base instructions
- `main.py` with basic implementation and usage of the src modules
- `run.sh` to run your files in the parent directory
  > `run.sh`will activate the virtual environment and run the program, storing the execution logs to the specified path
- If used with the `api` flag, it will create the following files:
  - `rest_api` module
  - `limits` module for rate limiting
  - `api.py` file in parent directory to run the uvicorn server
  - api security file
  - api logging file
  - update the `.env` file as per API variables
- If used with the `caching` flag, it will create the following files:
  - `server_cache` module
  - `redis` module
  - `src/rest_api/api.py` gets updated with caching on endpoints as an example
  - update the `.env` file as per Caching variables
- Lastly, it removes nested `__pycache__` directories from the project.
- [This script](https://gist.github.com/aadarshlalchandani/b737e77a480a70a4755267dd81f82a68#file-setup-sh) is run into your project directory upon running `aasetpy`
- You can take a look  the files to be created [here](https://github.com/aadarshlalchandani/aasetpy/tree/main/aasetpy-template-files)

## Single command setup in Ubuntu

> This setup requires to be run with `sudo` as it makes changes to the `/etc/bash.bashrc` file.

```bash
wget https://github.com/aadarshlalchandani/aasetpy/releases/download/v0.1.3/aasetpy.deb  >/dev/null 2>&1 && sudo apt install ./aasetpy.deb && rm aasetpy.deb
```

<details>

<summary>
<h2 style="display: inline;">
Manual Setup
</h2>
</summary>

### Open bashrc file to add command alias

```bash
sudo nano /etc/bash.bashrc
```

### Add these lines to the end of file

```bash
## credits: aadarshlalchandani/aasetpy
alias aasetpy='rm -rf ~/.wget-hsts && wget -q -O - https://gist.github.com/aadarshlalchandani/b737e77a480a70a4755267dd81f82a68/raw | bash -s --'
alias aaresetpy='rm -rf ~/.wget-hsts && wget -q -O - https://gist.github.com/aadarshlalchandani/b737e77a480a70a4755267dd81f82a68/raw | bash -s -- reset'
```

### Reopen the terminal
Your commands are now ready to be used!

</details>

# Usage

#### Setup (install/re-install dependencies) your Python Project

```bash
aasetpy
```

#### Project Template with FastAPI

```bash
aasetpy api
aasetpy api caching
```

#### Reset your Python Project

```bash
aaresetpy
aaresetpy api
aaresetpy api caching
```

OR

```bash
aasetpy reset
aasetpy reset api
aasetpy reset api caching
```
> `caching` flag, during initial setup (in presence of `reset` flag), will only work in presence of `api` flag for obvious reasons.  
> You can call `aasetpy caching` without `api` once you have `rest_api` module in `src/`

# Remove `aasetpy` from ubuntu

```bash
sudo apt remove aasetpy -y
```

[Reference](https://askubuntu.com/a/986053)
