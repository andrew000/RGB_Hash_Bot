docker stop rgb_bot
docker rm rgb_bot
docker rmi rgb_bot:latest
docker build . -t rgb_bot
docker run -d --restart always --name rgb_bot rgb_bot