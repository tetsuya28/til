# Init
sudo yum update -y && sudo yum install -y git vim zsh wget zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel xz xz-devel libffi-devel findutils util-linux-user

# Install for Python
sudo yum install -y gcc openssl-devel bzip2-devel libffi-devel

# Install my zsh
wget -O ~/.zshrc https://gist.githubusercontent.com/yakult1995/a03eb69b2297a2a7c74a3f8e5f4ccfe6/raw/bed4b44db0452bebdf4c2c962a1e97cfdf9b5d9e/.zshrc
mkdir ~/.zsh.d
wget -O ~/.zsh.d/languages.zsh https://gist.githubusercontent.com/yakult1995/d136560dc027d14e6a473747b46ce3c1/raw/4ce71c5eece8c9c7f02ef1a4ef9aaea6e4b0c673/languages.zsh
wget -O ~/.zsh.d/alias.zsh https://gist.githubusercontent.com/yakult1995/9913e4c9df68e27e62e464881a1837ad/raw/0f1df6b36f92097a6a9056d3d56907eabd7ee9f7/alias.zsh
sudo sh -c "echo `which zsh` > /etc/shells"
sudo chsh -s `which zsh` `whoami`

# Install envs
git clone https://github.com/riywo/anyenv ~/.anyenv
export PATH="$HOME/.anyenv/bin:$PATH"
eval "$(anyenv init -)"
echo y | anyenv install --init
anyenv install pyenv
source ~/.zshrc > /dev/null 2>&1
pyenv install 3.6.0
pyenv global 3.6.0
source ~/.zshrc > /dev/null 2>&1


# Install power-shell
pip install --user powerline-shell
wget -O ~/.zsh.d/power-shell.zsh https://gist.githubusercontent.com/yakult1995/3fdc0a71cac5a3e3aa5b2075cacce932/raw/980ae285add9798186adf80560526f9f93dd39b5/power-shell.zsh

# Install git-foresta
mkdir ~/bin
curl -L https://github.com/takaaki-kasai/git-foresta/raw/master/git-foresta -o ~/bin/git-foresta && chmod +x ~/bin/git-foresta
source ~/.zshrc > /dev/null 2>&1

# Download .vimrc
wget -O ~/.vimrc https://gist.githubusercontent.com/yakult1995/c7b76de04148532297a4f938316a0d55/raw/5995af99156abfe91a7ec8d9eda8c63b72736ff9/vimrc

# Others
## Timezone
sudo timedatectl set-timezone Asia/Tokyo

