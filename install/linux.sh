#!/bin/bash

echo -e "\e[94;1mChecking for Python 3.7 or Python 3.8\e[0m"
{
    {
        version=$(python3 -V | tail -c +8)
        python3 -V
    } || {
        version="0.0.0"
    }
    if [[ $version == *"3.8"* ]]; then {
        echo -e "\e[93;1m> Python 3.8.X installed\e[0m"
    } elif [[ $version == *"3.7"* ]]; then {
        echo -e "\e[93;1m> Python 3.7.X installed\e[0m"
    } else {
        echo -e "\e[91;1m> You need to install/update python\e[0m"
        echo -e "\e[94;1mPlease enter your password to automatically install/update Python\e[0m"
        {
            sudo echo "Thanks!"
        } || {
            echo "The installation cannot continue."
            exit
        }
        {
            echo -e "\e[95;1mTrying APT\e[0m"
            sudo apt install python3 python3-dev python3-vlc python3-pip
            sudo apt upgrade python3 python3-dev python3-vlc python3-pip
        } || {
            echo -e "\e[95;1mTrying DNF\e[0m"

        } || {
            echo -e "\e[95;1mTrying YUM\e[0m"

        } || {
            echo -e "\e[95;1mTrying PACMAN\e[0m"
            pacman -S vlc
        } || {
            echo -e "\e[91;1mCannot install python3, python3-dev, python3-vlc, python3-pip."
            echo -e "Please install them with your package manager\e[0m"
            echo "The installation cannot continue."
            exit
        }
    }
} || {
    echo -e "\e[91;1mPython 3 not installed"
}
