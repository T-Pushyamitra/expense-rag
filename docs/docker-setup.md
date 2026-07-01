### DOCKER SETUP

- Start docker

    `docker-compose up -d`

- Download embedding model into Ollama

    `docker exec -it ollama ollama pull nomic-embed-text`

    check:

    `docker exec -it ollama ollama list` 

    Result 

    `nomic-embed-text`

