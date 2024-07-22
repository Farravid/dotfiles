import subprocess
import inquirer
import os
from enum import Enum
from pathlib import Path

Purple = '\033[0;35m'
NC = '\033[0m'

class PackageAction(Enum):
    install=" -S --noconfirm "
    remove=" -Rcns "

def is_pckg_installed(package_name) -> bool:
    result = subprocess.run("yay -Qi " + package_name, shell=True, capture_output=True, text=True)
    return not result.returncode

def is_pckg_update_or_install_needed(package_name) -> bool:
    if not is_pckg_installed(package_name): return True

    result = subprocess.run("yay -Qu " + package_name, shell=True, capture_output=True, text=True)
    return not result.returncode

def perform_required_pckg_action(action : PackageAction, names : [str]):
    for name in names:
        command= "yay" + str(action.value) + name
        subprocess.run(command, shell=True)

def perform_optional_pckg_actions(action : PackageAction, names : [str]):
    for name in names:
        
        if action == PackageAction.remove and not is_pckg_installed(name): continue
        if action == PackageAction.install and not is_pckg_update_or_install_needed(name): continue

        print("\n")
        message = 'Do you want to ' + action.name + ' ' + Purple + name + NC + ' ?'
        question = [
            inquirer.List(
                "choice", message,["Yes", "No"],
            ),
        ]

        answer = inquirer.prompt(question)

        if answer["choice"] == "Yes":
            perform_required_pckg_action(action, [name])
            

def create_sym_links(symlink_files : [str]):
    for slf in symlink_files:
        print("Symlinking " + Purple + slf + NC + " file")

        system_file_path = Path(os.path.expanduser('~/' + slf))
        dotfiles_file_path = Path(os.path.expanduser('~/.dotfiles/' + slf))

        assert dotfiles_file_path.is_file() or dotfiles_file_path.is_dir(), "Trying to symlink an invalid dotfiles file/folder!"

        if system_file_path.is_file():
            os.remove(system_file_path)
        else:
            path_parent_folder = system_file_path.parent
            if not path_parent_folder.is_dir(): os.mkdir(path_parent_folder)

        os.symlink(dotfiles_file_path, system_file_path)


def main():
    print(r"""
    ██████╗  ██████╗ ████████╗███████╗██╗██╗     ███████╗███████╗
    ██╔══██╗██╔═══██╗╚══██╔══╝██╔════╝██║██║     ██╔════╝██╔════╝
    ██║  ██║██║   ██║   ██║   █████╗  ██║██║     █████╗  ███████╗
    ██║  ██║██║   ██║   ██║   ██╔══╝  ██║██║     ██╔══╝  ╚════██║
    ██████╔╝╚██████╔╝   ██║   ██║     ██║███████╗███████╗███████║
    ╚═════╝  ╚═════╝    ╚═╝   ╚═╝     ╚═╝╚══════╝╚══════╝╚══════╝                                                                                                                           
    """)

    print(Purple + "=== Removing not used software from Manjaro i3 😎 ===" + NC)
    perform_optional_pckg_actions(PackageAction.remove, ["palemoon, volumeicon", "nitrogen"])

    print(Purple + "=== Installing necessary software for this dotfiles ===" + NC)
    # perform_required_pckg_action(PackageAction.install,
    # [   
    #     "kitty", "ulauncher", "flameshot", "polybar",
    #     "neofetch", "blueman", "neovim", "github-cli"
    #     "git-lfs", "github-desktop", "discord", "obsidian"
    #     "google-chrome", "neofetch", "feh", "waypaper",
    #     "pulseaudio", "spotify", "pavucontrol", "playerctl",
    #     "python-pywal", "colorz, visual-studio-code-bin"
    # ])

    print(Purple + "=== Installing optional software for this dotfiles ===" + NC)
    # perform_optional_pckg_actions(PackageAction.install,
    # [  
    #     "fsearch", "nautilus", "hotspot", "appimagelauncher",
    #     "python2", "cava", "cmake"                                                        
    # ])

    # TODO Fix error oh my zsh stopping the execution probably

    print(Purple + "== Installing oh my zsh ===" + NC)
    subprocess.run("sh -c \"$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)\"", shell=True)
    subprocess.run("git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}/themes/powerlevel10k", shell=True)
    subprocess.run("git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting", shell=True)
    subprocess.run("git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions", shell=True)

    # TODO Code extensions

    print(Purple + "\n=== Symlinking files ===" + NC)
    create_sym_links([  ".config/kitty/kitty.conf",
                        ".config/neofetch/config.conf",
                        ".config/polybar/config.ini",
                        ".config/waypaper/config.ini",
                        ".config/picom.conf",
                        ".config/ulauncher/extensions.json",
                        ".config/ulauncher/settings.json",
                        ".config/ulauncher/shortcuts.json",
                        ".i3/config",
                        ".gitconfig", 
                        ".profile",
                        ".zshrc",
                        ".p10k.zsh"
                    ])

    #TODO Find a solution for extensions of ulauncher
    print(Purple + "\n=== Copy ulauncher extensions to .config/ulauncher folder ===" + NC)
    subprocess.run("cp -r ~/.dotfiles/.config/ulauncher/ext_preferences ~/.config/ulauncher", shell=True)

    subprocess.run("source ~/.zshrc", shell=True, capture_output=True, text=True)
    
    print(Purple + "\n=== Select a random wallpaper from dotfiles and applying pywal ===" + NC)
    subprocess.run("waypaper --random", shell=True)
    
    #TODO: zsh-theme10k


if __name__ == "__main__":
    main()
