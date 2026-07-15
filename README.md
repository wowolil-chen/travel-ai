# ✈️ Travel AI

An intelligent travel planner powered by **FastAPI**, **React**, **LangChain**, and **PostgreSQL**.

Travel AI helps users generate personalized travel itineraries through natural language conversations with an AI assistant.

---

## ✨ Features

- 🤖 AI-powered travel planning
- 💬 Streaming chat responses
- 🔐 User authentication (JWT)
- 📚 Conversation history
- 🗂️ Multi-conversation management
- ⚡ FastAPI backend
- ⚛️ React + Ant Design frontend
- 🐘 PostgreSQL database
- 🐳 Docker Compose deployment

---

## 🏗️ Tech Stack

### Frontend

- React
- Vite
- Ant Design
- Axios

### Backend

- FastAPI
- SQLAlchemy
- LangChain
- JWT Authentication
- Uvicorn

### Database

- PostgreSQL

### Deployment

- Docker
- Docker Compose
- Nginx

---

## 📂 Project Structure

```text
travel-ai
├── backend
│   ├── app
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend
│   ├── src
│   ├── Dockerfile
│   └── package.json
│
├── docker-compose.yml
├── init.sql
└── README.md
```

---

## 🚀 Getting Started

### Clone the repository

```bash
git clone https://github.com/wowoli-chen/travel-ai.git
cd travel-ai
```

### Start with Docker

```bash
docker-compose up -d --build
```

Services:

| Service | Port |
|----------|------|
| Frontend | 8300 |
| Backend | 8301 |
| PostgreSQL | 8302 |

---

## 📸 Screenshots

### Login

> Add your screenshot here

### Chat

> Add your screenshot here

---

## 🔑 Environment

Backend requires the following environment variables:

```env
DATABASE_HOST=postgres
DATABASE_PORT=5432
DATABASE_NAME=travel_ai
DATABASE_USER=your_username
DATABASE_PASSWORD=your_password

SECRET_KEY=your_secret_key
```

---

## 📌 Roadmap

- [x] User authentication
- [x] Conversation management
- [x] Streaming AI responses
- [x] Docker deployment
- [ ] Markdown rendering
- [ ] RAG knowledge base
- [ ] MCP integration
- [ ] Agent workflow
- [ ] Travel map visualization
- [ ] Voice interaction

---

## 🤝 Contributing

Pull requests are welcome.

For major changes, please open an issue first to discuss what you would like to change.

---

## 📄 License

This project is licensed under the MIT License.

---

## 👨‍💻 Author

**Chen Guangquan**

GitHub:

https://github.com/wowoli-chen
