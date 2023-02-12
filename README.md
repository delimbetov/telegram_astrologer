# Overview
Telegram bot that uses open ai API to do astrological predictions.

# How to build docker image
## Build image
docker build -t delimbetov/telegram_astrologer:git_sha_xxxxxx .

## Login - password will be prompted
docker login --username DOCKER_HUB_USERNAME

## Push to repo
docker push delimbetov/telegram_astrologer:git_sha_xxxxxx

# How to run existing image on Ubuntu
## Prepare docker deps
### remove old stuff
sudo apt-get remove docker docker-engine docker.io containerd runc

### setup repo
sudo apt-get update
sudo apt-get install \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

### add docker official gpg key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

### setup stable repo
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

### install docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

## Login - you have to do that ONLY if repo is private. Password will be prompted
docker login --username DOCKER_HUB_USERNAME

## Get docker image
docker pull delimbetov/telegram_astrologer:git_sha_xxxxxx

## Run it
docker run -d delimbetov/telegram_astrologer:git_sha_xxxxxx OPENAI_API_TOKEN API_ID API_HASH TOKEN DAILY_LIMIT