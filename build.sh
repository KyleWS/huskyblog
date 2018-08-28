#!/bin/bash

pip freeze --exclude-editable > remove_local_modules.txt
pip freeze > requirements.txt
echo "Docker login can fail"
docker login
docker build -t kylews/huskyblog .
docker push kylews/huskyblog
