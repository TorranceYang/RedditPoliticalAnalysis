#!/bin/bash

apt update
apt --yes install python python-dev python3 python3-dev
easy_install pip
pip install --ignore-installed google-cloud
pip install --upgrade google-cloud-language
pip install --upgrade nltk
mkdir -p /usr/share/nltk_data
python -c "import nltk; nltk.download('vader_lexicon', download_dir='/home/nltk_data/')"