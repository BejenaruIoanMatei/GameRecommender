# GameRecommender

## Project Description:

GameRecommender is a FastAPI-based backend API that provides game recommendations based on a given title.

It supports two different recommendation algorithms: Nearest Neighbors and Cosine Similarity, trained on game metadata.

The API returns a structured JSON response and handles errors gracefully when the requested title is not found.

Comes with: Spring Boot-based frontend client: [Game Recommender Client](https://github.com/BejenaruIoanMatei/GameRecommenderClient)

## Features

- Fast and lightweight API built with FastAPI
- Two recommendation strategies: Nearest Neighbors and Cosine Similarity
- JSON response structure suitable for frontend consumption
- Easily extendable with new recommendation logic

## Architecture & Deployment

The full stack is containerised using **Docker Compose**, orchestrating two independent services:

- **Backend** – FastAPI REST API served via Uvicorn
- **Frontend** – Spring Boot / Thymeleaf client

Services communicate over an internal Docker network. The frontend waits for the backend to pass a health check before starting.

### Run locally with Docker

```
git clone --recurse-submodules https://github.com/BejenaruIoanMatei/GameRecommenderSubmods
cd GameRecommenderSubmods
docker-compose up --build
```

OBS:

-  It won't run unless you have the .pkl files from running the notebooks

## Extras
- Contains a Jupyter notebook showcasing the data analysis process on the Steam games dataset.
- Useful for understanding the development flow and the reasoning behind the final API implementation.
- Spring Boot-based frontend client: [Game Recommender Client](https://github.com/BejenaruIoanMatei/GameRecommenderClient)
- Docker Compose setup: [Docker Composer Submods](https://github.com/BejenaruIoanMatei/GameRecommenderSubmods)

## Demo video:
- Watch it here: [Game Recommender Demo](https://drive.google.com/file/d/1jvwo-_ilcqu_GGUpUPCf7o2Ma6GJd1AI/view?usp=sharing)
