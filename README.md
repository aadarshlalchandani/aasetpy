<a href="https://www.buymeacoffee.com/aadarshlalchandani"><img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=☕&slug=aadarshlalchandani&button_colour=5F7FFF&font_colour=ffffff&font_family=Cookie&outline_colour=000000&coffee_colour=FFDD00" /></a>

# Setting up `aasetpy` in ubuntu

## Single command setup

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
```

#### Reset your Python Project

```bash
aaresetpy
aaresetpy api
```

OR

```bash
aasetpy reset
aasetpy reset api
```

# Remove `aasetpy` from ubuntu

```bash
sudo apt remove aasetpy -y
```

[Reference](https://askubuntu.com/a/986053)
