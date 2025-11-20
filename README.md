# Ask F1

![Ask F1 Logo](assets/logo.jpg)


To run both the frontend and the backend:
```
docker-compose up --build
```

Run just the OpenWebUI frontend:
```
docker run -d \
    -p 3000:8080 \
    -v .open-webui:/app/backend/data \
    -e OPENAI_API_BASE_URL=http://host.docker.internal:8080/v1 \
    -e OPENAI_API_KEY=no-key-needed \
    --name open-webui \
    --restart always \
    ghcr.io/open-webui/open-webui:main
```