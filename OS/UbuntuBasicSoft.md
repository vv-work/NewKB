sudo apt install tmux fish curl make p7zip-full unzip gh ffmpeg make -y


sudo apt install python3-full python3-pip python3-pynvim pipx -y


pip install matplotlib tensorflow openai --break-system-packages
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu --break-system-packages

sudo pipx ensurepath
sudo pipx install open-interpreter
sudo pipx install yt-dlp
sudo pipx install ipython




sudo apt install nginx nodejs npm -y

npm install -g neovim


sudo curl -LO https://github.com/neovim/neovim/releases/latest/download/nvim.appimage
chmod u+x nvim.appimage

./nvim.appimage --appimage-extract
./squashfs-root/AppRun --version

# Optional: exposing nvim globally.
sudo mv squashfs-root /
sudo ln -s /squashfs-root/AppRun /usr/bin/nvim

sudo apt install ripgrep

git clone https://github.com/NvChad/NvChad ~/.config/nvim --depth 1 && nvim


sudo apt-get install speedtest-cli

