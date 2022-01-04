sudo pacman -Syyu
sudo pacman -S yay
yay -S htop
yay -S unzip
yay -S pulseaudio
yay -S neovim
yay -S neofetch
yay -S cmake
yay -S rofi
yay -S discord
yay -S google-chrome
yay -S spotify
yay -S visual-studio-code-bin
yay -S picom
yay -S gruvbox-dark-gtk
yay -S gruvbox-dark-icons-gtk
yay -S nerd-fonts-complete
yay -S flameshot
yay -S py3status
sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

cp -a . ../
cd ..
rm -rf .git
rm README.md
rm setup.sh

nitrogen

lxappearance


