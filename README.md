Medichat
========

An application built to answer medical questions based on the uploaded context.

How to run
==========

- Clone the project
  ```
  git clone https://github.com/ajk0x00/medichat.git
  ```
- Create a virtual environment using virtualenv and activate the env
  ```
  virtualenv .venv
  source ./.venv/bin/activate
  ```
- Install required packages
  ```
  pip3 install -r pytorch-cpu.txt
  pip3 install -r requirements.txt
  ```
- Install supervisor
  ```
  sudo apt install supervisor
  ```
- Export Groq api key
  ```
  export GROQ_API_KEY="<TOKEN>"
  ```
- Run the application
  ```
  supervisord -c supervisord.conf
  ```