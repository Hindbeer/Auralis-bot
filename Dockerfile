FROM python:3.14-slim

RUN apt-get update && apt-get install -y ffmpeg && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install uv

COPY pyproject.toml uv.lock ./

RUN uv pip install --system -r pyproject.toml

COPY . .

CMD ["uv", "run", "main.py"]
