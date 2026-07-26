# Fine-Tuning para IA: Engenharia de Software Moderna

## Visão Geral do Projeto

Este documento foi inspirado na metodologia de aprendizado estruturado da física teórica, adaptado para criar um fine-tuning especializado em engenharia de software. O objetivo é desenvolver modelos de IA que compreendam profundamente os princípios da engenharia de software, desde fundamentos até práticas avançadas de desenvolvimento.

### Contexto Filosófico
A engenharia de software é comparada a uma construção arquitetônica: fundações sólidas em algoritmos e estruturas de dados, progredindo para arquiteturas complexas e sistemas distribuídos. O desenvolvimento deve ser rigoroso, com ênfase em qualidade de código, escalabilidade e manutenibilidade.

### Metodologia de Aprendizado Recomendada
1. **Estudo Sistemático**: Seguir sequência lógica de conceitos
2. **Prática Intensiva**: Implementar projetos reais e resolver problemas
3. **Revisão de Código**: Analisar código de projetos open source
4. **Persistência**: Explorar diferentes tecnologias e frameworks
5. **Integração**: Conectar teoria com implementação prática

---

## 1. FUNDAMENTOS DE PROGRAMAÇÃO E ALGORITMOS

### 1.1 Estruturas de Dados Essenciais
```python
# Exemplo: Implementação de estruturas de dados fundamentais
class HashTable:
    """Tabela hash com resolução de colisões por encadeamento"""
    def __init__(self, size=100):
        self.size = size
        self.table = [[] for _ in range(size)]
        self.count = 0

    def _hash(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                pair[1] = value
                return
        self.table[index].append([key, value])
        self.count += 1

    def get(self, key):
        index = self._hash(key)
        for pair in self.table[index]:
            if pair[0] == key:
                return pair[1]
        raise KeyError(key)
```

**Conceitos Críticos:**
- Complexidade de algoritmos (Big O notation)
- Estruturas de dados lineares e não-lineares
- Algoritmos de ordenação e busca
- Programação dinâmica e algoritmos gulosos

### 1.2 Paradigmas de Programação
```python
# Exemplo: Padrões de design fundamentais
from abc import ABC, abstractmethod

class Strategy(ABC):
    @abstractmethod
    def execute(self, data):
        pass

class BubbleSort(Strategy):
    def execute(self, data):
        arr = data.copy()
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

class QuickSort(Strategy):
    def execute(self, data):
        arr = data.copy()
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return self.execute(left) + middle + self.execute(right)

# Uso do padrão Strategy
sorter = QuickSort()
sorted_data = sorter.execute([64, 34, 25, 12, 22, 11, 90])
```

**Tópicos Essenciais:**
- Programação orientada a objetos
- Programação funcional
- Programação reativa
- Padrões de design (GoF, GRASP)

### 1.3 Linguagens e Ecossistemas
```python
# Exemplo: Sistema de tipos avançado em TypeScript
interface User {
    id: number;
    name: string;
    email: string;
    role: 'admin' | 'user' | 'moderator';
}

interface Repository<T> {
    findById(id: number): Promise<T | null>;
    findAll(): Promise<T[]>;
    save(entity: T): Promise<T>;
    delete(id: number): Promise<boolean>;
}

class UserService implements Repository<User> {
    private users: Map<number, User> = new Map();

    async findById(id: number): Promise<User | null> {
        return this.users.get(id) || null;
    }

    async findAll(): Promise<User[]> {
        return Array.from(this.users.values());
    }

    async save(user: User): Promise<User> {
        this.users.set(user.id, user);
        return user;
    }

    async delete(id: number): Promise<boolean> {
        return this.users.delete(id);
    }
}
```

**Conceitos Fundamentais:**
- Sistemas de tipos estáticos vs dinâmicos
- Compilação vs interpretação
- Gerenciamento de memória
- Concorrência e paralelismo

---

## 2. ARQUITETURAS DE SOFTWARE E PADRÕES

### 2.1 Arquiteturas Monolíticas vs Microserviços
**Padrões Essenciais:**
- Arquitetura em camadas (Layered Architecture)
- Arquitetura hexagonal (Hexagonal Architecture)
- CQRS (Command Query Responsibility Segregation)
- Event Sourcing

```python
# Exemplo: Arquitetura hexagonal em Python
from abc import ABC, abstractmethod
from typing import List, Optional

# Domain Layer
class User:
    def __init__(self, user_id: int, name: str, email: str):
        self.user_id = user_id
        self.name = name
        self.email = email

# Application Layer
class UserService:
    def __init__(self, user_repository: 'UserRepository'):
        self.user_repository = user_repository

    def create_user(self, name: str, email: str) -> User:
        user = User(user_id=self._generate_id(), name=name, email=email)
        self.user_repository.save(user)
        return user

    def get_user(self, user_id: int) -> Optional[User]:
        return self.user_repository.find_by_id(user_id)

    def _generate_id(self) -> int:
        return hash(f"{name}{email}{time.time()}") % 1000000

# Infrastructure Layer
class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None:
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[User]:
        pass

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users: dict[int, User] = {}

    def save(self, user: User) -> None:
        self.users[user.user_id] = user

    def find_by_id(self, user_id: int) -> Optional[User]:
        return self.users.get(user_id)
```

### 2.2 Desenvolvimento Web e APIs
**Técnicas Avançadas:**
- RESTful APIs vs GraphQL
- Autenticação e autorização (JWT, OAuth)
- Rate limiting e throttling
- Documentação de APIs (OpenAPI/Swagger)

```python
# Exemplo: API REST com FastAPI
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List
import uvicorn

app = FastAPI(title="User Management API", version="1.0.0")

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

# Simulação de banco de dados
users_db = {}
user_counter = 1

@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate):
    global user_counter
    new_user = UserResponse(id=user_counter, name=user.name, email=user.email)
    users_db[user_counter] = new_user
    user_counter += 1
    return new_user

@app.get("/users", response_model=List[UserResponse])
async def get_users():
    return list(users_db.values())

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    return users_db[user_id]

@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserCreate):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    updated_user = UserResponse(id=user_id, name=user.name, email=user.email)
    users_db[user_id] = updated_user
    return updated_user

@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    if user_id not in users_db:
        raise HTTPException(status_code=404, detail="User not found")
    del users_db[user_id]
    return {"message": "User deleted successfully"}
```

### 2.3 Bancos de Dados e Persistência
```python
# Exemplo: Padrão Repository com SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from datetime import datetime
from typing import List, Optional

Base = declarative_base()

class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class UserRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> User:
        db_user = UserModel(name=user.name, email=user.email)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)

        # Converter para domínio
        return User(
            user_id=db_user.id,
            name=db_user.name,
            email=db_user.email
        )

    def find_by_id(self, user_id: int) -> Optional[User]:
        db_user = self.session.query(UserModel).filter(UserModel.id == user_id).first()
        if db_user:
            return User(
                user_id=db_user.id,
                name=db_user.name,
                email=db_user.email
            )
        return None

    def find_all(self) -> List[User]:
        db_users = self.session.query(UserModel).all()
        return [
            User(user_id=db_user.id, name=db_user.name, email=db_user.email)
            for db_user in db_users
        ]

# Configuração do banco
engine = create_engine("sqlite:///./test.db")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
```

---

## 3. HIPÓTESES E RAMIFICAÇÕES PARA DESENVOLVIMENTO

### 3.1 Arquiteturas de Microserviços

**Hipótese Principal: Escalabilidade em Sistemas Distribuídos**
- **Ramificação 1**: Padrões de comunicação assíncrona entre serviços
- **Ramificação 2**: Gerenciamento de estado distribuído e consistência
- **Ramificação 3**: Observabilidade e monitoramento em arquiteturas distribuídas

```python
# Exemplo: Comunicação assíncrona com RabbitMQ
import pika
import json
from typing import Callable

class MessageBroker:
    def __init__(self, host: str = 'localhost'):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host))
        self.channel = self.connection.channel()

    def publish(self, queue: str, message: dict):
        self.channel.queue_declare(queue=queue)
        self.channel.basic_publish(
            exchange='',
            routing_key=queue,
            body=json.dumps(message)
        )

    def subscribe(self, queue: str, callback: Callable):
        self.channel.queue_declare(queue=queue)

        def wrapper(ch, method, properties, body):
            message = json.loads(body)
            callback(message)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_consume(queue=queue, on_message_callback=wrapper)
        self.channel.start_consuming()

# Exemplo de uso
broker = MessageBroker()

# Publicar mensagem
broker.publish('user_created', {
    'user_id': 123,
    'name': 'João Silva',
    'email': 'joao@example.com'
})

# Consumir mensagem
def handle_user_created(message):
    print(f"Novo usuário criado: {message}")
    # Aqui poderia enviar email de boas-vindas, etc.

broker.subscribe('user_created', handle_user_created)
```

### 3.2 Desenvolvimento Frontend Moderno

**Hipótese Principal: Experiência do Usuário em Aplicações Web**
- **Ramificação 1**: Gerenciamento de estado complexo em SPAs
- **Ramificação 2**: Performance e otimização de aplicações React/Vue/Angular
- **Ramificação 3**: Acessibilidade e design inclusivo

```javascript
// Exemplo: Gerenciamento de estado com Redux Toolkit
import { createSlice, configureStore } from '@reduxjs/toolkit';

const userSlice = createSlice({
  name: 'user',
  initialState: {
    currentUser: null,
    loading: false,
    error: null
  },
  reducers: {
    loginStart: (state) => {
      state.loading = true;
      state.error = null;
    },
    loginSuccess: (state, action) => {
      state.loading = false;
      state.currentUser = action.payload;
    },
    loginFailure: (state, action) => {
      state.loading = false;
      state.error = action.payload;
    },
    logout: (state) => {
      state.currentUser = null;
      state.loading = false;
      state.error = null;
    }
  }
});

export const { loginStart, loginSuccess, loginFailure, logout } = userSlice.actions;

const store = configureStore({
  reducer: {
    user: userSlice.reducer
  }
});

// Hook personalizado para usar no componente
import { useDispatch, useSelector } from 'react-redux';

export const useAuth = () => {
  const dispatch = useDispatch();
  const { currentUser, loading, error } = useSelector(state => state.user);

  const login = async (credentials) => {
    try {
      dispatch(loginStart());
      // Simulação de API call
      const user = await api.login(credentials);
      dispatch(loginSuccess(user));
    } catch (err) {
      dispatch(loginFailure(err.message));
    }
  };

  return { currentUser, loading, error, login, logout: () => dispatch(logout()) };
};
```

### 3.3 DevOps e Infraestrutura como Código

**Hipótese Principal: Automação de Pipelines de Deployment**
- **Ramificação 1**: Estratégias de deployment (blue-green, canary, rolling)
- **Ramificação 2**: Monitoramento e observabilidade em produção
- **Ramificação 3**: Segurança em pipelines de CI/CD

```yaml
# Exemplo: Pipeline CI/CD com GitHub Actions
name: CI/CD Pipeline

on:
  push:
    branches: [ main, develop ]
  pull_request:
    branches: [ main ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3

    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.9'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt
        pip install -r requirements-dev.txt

    - name: Run tests
      run: |
        pytest --cov=src --cov-report=xml

    - name: Upload coverage to Codecov
      uses: codecov/codecov-action@v3

  build-and-deploy:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'

    steps:
    - uses: actions/checkout@v3

    - name: Build Docker image
      run: |
        docker build -t myapp:${{ github.sha }} .
        docker tag myapp:${{ github.sha }} myapp:latest

    - name: Deploy to production
      run: |
        echo "Deploying to production..."
        # Aqui seria o comando de deploy real
```

### 3.4 Segurança de Aplicações

**Hipótese Principal: Prevenção de Vulnerabilidades em Tempo de Desenvolvimento**
- **Ramificação 1**: Análise estática de segurança (SAST)
- **Ramificação 2**: Testes de penetração automatizados
- **Ramificação 3**: Gerenciamento seguro de secrets e credenciais

```python
# Exemplo: Middleware de segurança para APIs
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt
import time
from typing import Optional

class JWTAuth:
    def __init__(self, secret_key: str):
        self.secret_key = secret_key

    def create_token(self, user_id: int, role: str) -> str:
        payload = {
            'user_id': user_id,
            'role': role,
            'exp': int(time.time()) + 3600,  # 1 hora
            'iat': int(time.time())
        }
        return jwt.encode(payload, self.secret_key, algorithm='HS256')

    def verify_token(self, token: str) -> Optional[dict]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            if payload['exp'] < time.time():
                return None
            return payload
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None

class AuthMiddleware:
    def __init__(self, jwt_auth: JWTAuth):
        self.jwt_auth = jwt_auth
        self.security = HTTPBearer()

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await self.security(request)
        payload = self.jwt_auth.verify_token(credentials.credentials)

        if not payload:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        # Adicionar informações do usuário ao request
        request.state.user_id = payload['user_id']
        request.state.role = payload['role']

# Uso do middleware
auth = JWTAuth("my-secret-key")
auth_middleware = AuthMiddleware(auth)

# Exemplo de endpoint protegido
@app.get("/protected")
async def protected_route(request: Request):
    user_id = request.state.user_id
    role = request.state.role

    if role != "admin":
        raise HTTPException(status_code=403, detail="Insufficient permissions")

    return {"message": f"Hello admin user {user_id}"}
```

### 3.5 Performance e Escalabilidade

**Hipótese Principal: Otimização de Sistemas de Alto Tráfego**
- **Ramificação 1**: Cache distribuído e estratégias de invalidação
- **Ramificação 2**: Otimização de queries em bancos de dados
- **Ramificação 3**: Balanceamento de carga e auto-scaling

```python
# Exemplo: Sistema de cache com Redis
import redis
import json
from typing import Optional, Any
import asyncio

class CacheService:
    def __init__(self, redis_url: str = "redis://localhost:6379"):
        self.redis = redis.from_url(redis_url)

    async def get(self, key: str) -> Optional[Any]:
        """Busca valor do cache"""
        value = self.redis.get(key)
        if value:
            return json.loads(value)
        return None

    async def set(self, key: str, value: Any, ttl: int = 3600) -> None:
        """Armazena valor no cache com TTL"""
        self.redis.setex(key, ttl, json.dumps(value))

    async def delete(self, key: str) -> None:
        """Remove valor do cache"""
        self.redis.delete(key)

    async def get_or_set(self, key: str, func, ttl: int = 3600):
        """Padrão cache-aside"""
        cached_value = await self.get(key)
        if cached_value is not None:
            return cached_value

        # Se não está no cache, executa a função
        value = await func()
        await self.set(key, value, ttl)
        return value

# Exemplo de uso com função assíncrona
cache = CacheService()

async def expensive_database_query(user_id: int):
    # Simulação de query cara ao banco
    await asyncio.sleep(1)  # Simula latência
    return {"user_id": user_id, "name": "João", "email": "joao@example.com"}

@app.get("/users/{user_id}")
async def get_user_cached(user_id: int):
    # Cache com chave baseada no user_id
    cache_key = f"user:{user_id}"

    user_data = await cache.get_or_set(
        cache_key,
        lambda: expensive_database_query(user_id),
        ttl=300  # 5 minutos
    )

    return user_data
```

---

## 4. FERRAMENTAS E TECNOLOGIAS ESSENCIAIS

### 4.1 Stack de Desenvolvimento Moderno
```python
# Configuração recomendada para projetos Python
# requirements.txt
fastapi==0.104.1
sqlalchemy==2.0.23
pydantic==2.5.0
uvicorn==0.24.0
pytest==7.4.3
black==23.11.0
flake8==6.1.0
mypy==1.7.1
redis==5.0.1
celery==5.3.4
```

### 4.2 Frameworks e Bibliotecas
- **Backend**: FastAPI, Django, Flask, Express.js, Spring Boot
- **Frontend**: React, Vue.js, Angular, Svelte
- **Mobile**: React Native, Flutter, SwiftUI, Jetpack Compose
- **Bancos**: PostgreSQL, MongoDB, Redis, Elasticsearch
- **DevOps**: Docker, Kubernetes, Terraform, Ansible

### 4.3 Ferramentas de Desenvolvimento
- **Controle de Versão**: Git, GitHub/GitLab
- **CI/CD**: GitHub Actions, GitLab CI, Jenkins
- **Monitoramento**: Prometheus, Grafana, ELK Stack
- **Testes**: Jest, pytest, Cypress, Selenium

---

## 5. METODOLOGIA DE DESENVOLVIMENTO

### 5.1 Estrutura de Projeto
```
software_engineering_project/
├── src/
│   ├── domain/
│   │   ├── entities/
│   │   ├── value_objects/
│   │   └── repositories/
│   ├── application/
│   │   ├── services/
│   │   ├── use_cases/
│   │   └── dto/
│   ├── infrastructure/
│   │   ├── database/
│   │   ├── external_apis/
│   │   └── messaging/
│   └── presentation/
│       ├── controllers/
│       ├── middleware/
│       └── views/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── e2e/
├── docs/
│   ├── api/
│   ├── architecture/
│   └── deployment/
├── scripts/
│   ├── build/
│   ├── deploy/
│   └── monitoring/
├── docker/
├── kubernetes/
├── .github/
│   └── workflows/
└── requirements.txt
```

### 5.2 Boas Práticas de Desenvolvimento

1. **Code Reviews e Pair Programming**
```python
# Exemplo de função bem documentada e testável
def calculate_user_score(user_id: int, db_session) -> float:
    """
    Calcula a pontuação do usuário baseada em atividade recente.

    A pontuação é calculada considerando:
    - Posts criados (peso 2.0)
    - Comentários feitos (peso 1.0)
    - Likes recebidos (peso 0.5)
    - Tempo desde última atividade (decaimento exponencial)

    Args:
        user_id: ID único do usuário
        db_session: Sessão do banco de dados

    Returns:
        Pontuação calculada do usuário

    Raises:
        ValueError: Se user_id não existir
    """
    # Buscar dados do usuário
    user = db_session.query(User).filter(User.id == user_id).first()
    if not user:
        raise ValueError(f"Usuário {user_id} não encontrado")

    # Calcular componentes da pontuação
    posts_score = len(user.posts) * 2.0
    comments_score = len(user.comments) * 1.0
    likes_score = sum(len(post.likes) for post in user.posts) * 0.5

    # Aplicar decaimento baseado no tempo
    days_since_active = (datetime.now() - user.last_activity).days
    time_decay = math.exp(-days_since_active / 30)  # Meia-vida de 30 dias

    total_score = (posts_score + comments_score + likes_score) * time_decay

    return round(total_score, 2)
```

2. **Testes Automatizados**
```python
import pytest
from unittest.mock import Mock, patch
from src.domain.services.user_score_calculator import calculate_user_score

class TestCalculateUserScore:
    def test_user_not_found_raises_value_error(self):
        """Testa que usuário inexistente lança ValueError"""
        mock_session = Mock()
        mock_session.query().filter().first.return_value = None

        with pytest.raises(ValueError, match="Usuário 999 não encontrado"):
            calculate_user_score(999, mock_session)

    def test_score_calculation_with_recent_activity(self):
        """Testa cálculo de pontuação para usuário ativo recentemente"""
        # Criar mock do usuário
        mock_user = Mock()
        mock_user.posts = [Mock(likes=[1, 2, 3]), Mock(likes=[4])]  # 2 posts, 6 likes total
        mock_user.comments = [Mock(), Mock(), Mock()]  # 3 comentários
        mock_user.last_activity = datetime.now()  # Atividade recente

        mock_session = Mock()
        mock_session.query().filter().first.return_value = mock_user

        score = calculate_user_score(1, mock_session)

        # Verificar cálculo: (2*2.0 + 3*1.0 + 6*0.5) * 1.0 = 7.0
        assert score == 7.0

    @patch('src.domain.services.user_score_calculator.datetime')
    def test_score_decay_over_time(self, mock_datetime):
        """Testa decaimento da pontuação com o tempo"""
        # Configurar data mockada (30 dias atrás)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        mock_datetime.now.return_value = datetime.now()

        mock_user = Mock()
        mock_user.posts = [Mock(likes=[])]
        mock_user.comments = []
        mock_user.last_activity = thirty_days_ago

        mock_session = Mock()
        mock_session.query().filter().first.return_value = mock_user

        score = calculate_user_score(1, mock_session)

        # Pontuação deve ser reduzida pela metade devido ao decaimento
        expected_score = (1 * 2.0) * math.exp(-30/30)  # ~1.0
        assert abs(score - expected_score) < 0.01
```

3. **Monitoramento e Observabilidade**
```python
# Exemplo: Implementação de métricas e logs estruturados
import logging
import time
from prometheus_client import Counter, Histogram, generate_latest
import prometheus_client

# Configurar métricas Prometheus
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_LATENCY = Histogram('http_request_duration_seconds', 'HTTP request latency', ['method', 'endpoint'])

# Configurar logging estruturado
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MetricsMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope['type'] != 'http':
            return await self.app(scope, receive, send)

        start_time = time.time()

        # Wrapper para interceptar a resposta
        response_status = 200

        async def send_wrapper(message):
            nonlocal response_status
            if message['type'] == 'http.response.start':
                response_status = message['status']

            await send(message)

        try:
            await self.app(scope, receive, send_wrapper)

            # Registrar métricas
            REQUEST_COUNT.labels(
                method=scope['method'],
                endpoint=scope['path'],
                status=str(response_status)
            ).inc()

            REQUEST_LATENCY.labels(
                method=scope['method'],
                endpoint=scope['path']
            ).observe(time.time() - start_time)

        except Exception as e:
            # Log de erro estruturado
            logger.error(
                "Erro na requisição HTTP",
                extra={
                    'method': scope['method'],
                    'path': scope['path'],
                    'error': str(e),
                    'user_agent': dict(scope.get('headers', [])).get(b'user-agent', b'').decode()
                },
                exc_info=True
            )

            # Registrar erro nas métricas
            REQUEST_COUNT.labels(
                method=scope['method'],
                endpoint=scope['path'],
                status='500'
            ).inc()

            raise

# Endpoint para métricas
@app.get("/metrics")
async def metrics():
    return Response(
        generate_latest(),
        media_type="text/plain",
        headers={"Content-Type": "text/plain; charset=utf-8"}
    )
```

### 5.3 Estratégias de Qualidade e Segurança

1. **Análise Estática de Código**
```bash
# Script de qualidade de código
#!/bin/bash

echo "🔍 Executando análise de qualidade de código..."

# Formatação
echo "📝 Verificando formatação com Black..."
black --check --diff src/ tests/

# Linting
echo "🔧 Executando linting com flake8..."
flake8 src/ tests/ --max-line-length=88 --extend-ignore=E203,W503

# Type checking
echo "📊 Verificando tipos com mypy..."
mypy src/ --ignore-missing-imports

# Segurança
echo "🔒 Verificando segurança com bandit..."
bandit -r src/ -f json -o security_report.json

# Cobertura de testes
echo "📈 Executando testes com cobertura..."
pytest --cov=src --cov-report=html --cov-report=term-missing

echo "✅ Análise completa!"
```

2. **Gerenciamento de Dependências Seguras**
```python
# Exemplo: Verificação de vulnerabilidades em dependências
import subprocess
import json

def check_vulnerabilities():
    """Verifica vulnerabilidades em dependências usando safety"""
    try:
        result = subprocess.run(
            ['safety', 'check', '--json'],
            capture_output=True,
            text=True,
            cwd='.'
        )

        if result.returncode == 0:
            print("✅ Nenhuma vulnerabilidade encontrada!")
            return []

        vulnerabilities = json.loads(result.stdout)
        print(f"🚨 Encontradas {len(vulnerabilities)} vulnerabilidades:")

        for vuln in vulnerabilities:
            print(f"- {vuln['package']} {vuln['vulnerable_spec']}: {vuln['advisory']}")

        return vulnerabilities

    except FileNotFoundError:
        print("❌ Safety não está instalado. Instale com: pip install safety")
        return []

def update_dependencies():
    """Atualiza dependências de forma segura"""
    print("🔄 Verificando atualizações seguras...")

    # Verificar vulnerabilidades antes
    vulnerabilities = check_vulnerabilities()
    if vulnerabilities:
        print("⚠️  Corrija as vulnerabilidades antes de atualizar!")
        return

    # Atualizar dependências
    subprocess.run(['pip', 'install', '--upgrade', '-r', 'requirements.txt'])

    # Verificar novamente após atualização
    new_vulnerabilities = check_vulnerabilities()
    if new_vulnerabilities:
        print("⚠️  Novas vulnerabilidades detectadas após atualização!")
    else:
        print("✅ Dependências atualizadas com segurança!")
```

---

## 6. EXERCÍCIOS PRÁTICOS E PROJETOS

### 6.1 Projeto Iniciante: Sistema de Gerenciamento de Tarefas
**Objetivo**: Implementar CRUD básico com autenticação
**Dificuldade**: Baixa
**Tempo estimado**: 4-6 horas
**Tecnologias**: FastAPI, SQLite, JWT

### 6.2 Projeto Intermediário: E-commerce com Microserviços
**Objetivo**: Sistema de loja online com catálogo, carrinho e pagamentos
**Dificuldade**: Média-Alta
**Tempo estimado**: 20-30 horas
**Tecnologias**: React, Node.js, PostgreSQL, Redis, Docker

### 6.3 Projeto Avançado: Plataforma de Streaming
**Objetivo**: Sistema de vídeo streaming com CDN e analytics
**Dificuldade**: Alta
**Tempo estimado**: 40+ horas
**Tecnologias**: Kubernetes, Go, Cassandra, Kafka, AWS/GCP

### 6.4 Projeto Especializado: Sistema de Trading de Alta Frequência
**Objetivo**: Plataforma de trading com baixa latência e alto throughput
**Dificuldade**: Muito Alta
**Tempo estimado**: 60+ horas
**Tecnologias**: C++, Redis Cluster, TimescaleDB, Kubernetes

---

## 7. ARQUITETURA DE SOFTWARE AVANÇADA

### 7.1 Arquitetura Hexagonal (Ports and Adapters)
```python
# Exemplo: Arquitetura Hexagonal para sistema de pedidos
from abc import ABC, abstractmethod
from typing import List, Optional
from dataclasses import dataclass
from datetime import datetime

# Domain Layer - Núcleo da aplicação
@dataclass
class Order:
    id: str
    customer_id: str
    items: List[dict]
    total: float
    status: str
    created_at: datetime

class OrderRepository(ABC):
    """Port - Interface para persistência"""
    @abstractmethod
    def save(self, order: Order) -> None:
        pass
    
    @abstractmethod
    def find_by_id(self, order_id: str) -> Optional[Order]:
        pass
    
    @abstractmethod
    def find_by_customer(self, customer_id: str) -> List[Order]:
        pass

class PaymentGateway(ABC):
    """Port - Interface para pagamentos"""
    @abstractmethod
    def process_payment(self, order: Order) -> bool:
        pass

# Application Layer - Casos de uso
class OrderService:
    def __init__(self, repository: OrderRepository, payment: PaymentGateway):
        self.repository = repository
        self.payment = payment
    
    def create_order(self, customer_id: str, items: List[dict]) -> Order:
        total = sum(item['price'] * item['quantity'] for item in items)
        
        order = Order(
            id=self._generate_id(),
            customer_id=customer_id,
            items=items,
            total=total,
            status='pending',
            created_at=datetime.now()
        )
        
        self.repository.save(order)
        return order
    
    def process_order(self, order_id: str) -> bool:
        order = self.repository.find_by_id(order_id)
        if not order:
            raise ValueError(f"Order {order_id} not found")
        
        if self.payment.process_payment(order):
            order.status = 'paid'
            self.repository.save(order)
            return True
        
        order.status = 'failed'
        self.repository.save(order)
        return False
    
    def _generate_id(self) -> str:
        import uuid
        return str(uuid.uuid4())

# Infrastructure Layer - Adapters
class PostgresOrderRepository(OrderRepository):
    """Adapter - Implementação com PostgreSQL"""
    def __init__(self, connection):
        self.conn = connection
    
    def save(self, order: Order) -> None:
        query = """
            INSERT INTO orders (id, customer_id, items, total, status, created_at)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (id) DO UPDATE SET
                status = EXCLUDED.status,
                items = EXCLUDED.items,
                total = EXCLUDED.total
        """
        import json
        self.conn.execute(query, (
            order.id,
            order.customer_id,
            json.dumps(order.items),
            order.total,
            order.status,
            order.created_at
        ))
    
    def find_by_id(self, order_id: str) -> Optional[Order]:
        query = "SELECT * FROM orders WHERE id = %s"
        result = self.conn.execute(query, (order_id,)).fetchone()
        
        if result:
            return Order(**dict(result))
        return None
    
    def find_by_customer(self, customer_id: str) -> List[Order]:
        query = "SELECT * FROM orders WHERE customer_id = %s"
        results = self.conn.execute(query, (customer_id,)).fetchall()
        return [Order(**dict(row)) for row in results]

class StripePaymentGateway(PaymentGateway):
    """Adapter - Implementação com Stripe"""
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    def process_payment(self, order: Order) -> bool:
        # Simulação de chamada à API do Stripe
        try:
            # stripe.Charge.create(...)
            return True
        except Exception as e:
            print(f"Payment failed: {e}")
            return False

# Presentation Layer - API
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class CreateOrderRequest(BaseModel):
    customer_id: str
    items: List[dict]

@app.post("/orders")
async def create_order(request: CreateOrderRequest):
    # Dependency injection
    repository = PostgresOrderRepository(get_db_connection())
    payment = StripePaymentGateway(get_stripe_key())
    service = OrderService(repository, payment)
    
    order = service.create_order(request.customer_id, request.items)
    return {"order_id": order.id, "status": order.status}

@app.post("/orders/{order_id}/process")
async def process_order(order_id: str):
    repository = PostgresOrderRepository(get_db_connection())
    payment = StripePaymentGateway(get_stripe_key())
    service = OrderService(repository, payment)
    
    success = service.process_order(order_id)
    if not success:
        raise HTTPException(status_code=400, detail="Payment failed")
    
    return {"status": "success"}
```

**Conceitos Fundamentais:**
- Separação de responsabilidades (SoC)
- Inversão de dependências (DIP)
- Testabilidade e manutenibilidade
- Ports (interfaces) e Adapters (implementações)
- Domain-Driven Design (DDD)

### 7.2 Event-Driven Architecture
```python
# Exemplo: Sistema de eventos com padrão Publisher-Subscriber
from typing import Callable, Dict, List
from dataclasses import dataclass
from datetime import datetime
import asyncio
import json

@dataclass
class Event:
    type: str
    data: dict
    timestamp: datetime
    correlation_id: str

class EventBus:
    """Event Bus para comunicação assíncrona"""
    def __init__(self):
        self.subscribers: Dict[str, List[Callable]] = {}
    
    def subscribe(self, event_type: str, handler: Callable):
        if event_type not in self.subscribers:
            self.subscribers[event_type] = []
        self.subscribers[event_type].append(handler)
    
    async def publish(self, event: Event):
        if event.type in self.subscribers:
            tasks = [
                asyncio.create_task(handler(event))
                for handler in self.subscribers[event.type]
            ]
            await asyncio.gather(*tasks)
    
    def unsubscribe(self, event_type: str, handler: Callable):
        if event_type in self.subscribers:
            self.subscribers[event_type].remove(handler)

# Event Sourcing - Armazenar eventos
class EventStore:
    """Armazena todos os eventos do sistema"""
    def __init__(self):
        self.events: List[Event] = []
    
    def append(self, event: Event):
        self.events.append(event)
    
    def get_events(self, correlation_id: str) -> List[Event]:
        return [e for e in self.events if e.correlation_id == correlation_id]
    
    def replay_events(self, correlation_id: str):
        """Reconstrói estado a partir dos eventos"""
        events = self.get_events(correlation_id)
        state = {}
        
        for event in events:
            if event.type == 'OrderCreated':
                state['order_id'] = event.data['order_id']
                state['status'] = 'created'
            elif event.type == 'PaymentProcessed':
                state['status'] = 'paid'
            elif event.type == 'OrderShipped':
                state['status'] = 'shipped'
                state['tracking_number'] = event.data['tracking_number']
        
        return state

# Handlers de eventos
class OrderEventHandlers:
    def __init__(self, event_bus: EventBus, event_store: EventStore):
        self.event_bus = event_bus
        self.event_store = event_store
        self._register_handlers()
    
    def _register_handlers(self):
        self.event_bus.subscribe('OrderCreated', self.on_order_created)
        self.event_bus.subscribe('PaymentProcessed', self.on_payment_processed)
        self.event_bus.subscribe('OrderShipped', self.on_order_shipped)
    
    async def on_order_created(self, event: Event):
        print(f"Order created: {event.data['order_id']}")
        self.event_store.append(event)
        
        # Enviar email de confirmação
        await self.send_confirmation_email(event.data)
    
    async def on_payment_processed(self, event: Event):
        print(f"Payment processed for order: {event.data['order_id']}")
        self.event_store.append(event)
        
        # Iniciar processo de fulfillment
        await self.start_fulfillment(event.data)
    
    async def on_order_shipped(self, event: Event):
        print(f"Order shipped: {event.data['order_id']}")
        self.event_store.append(event)
        
        # Enviar notificação de envio
        await self.send_shipping_notification(event.data)
    
    async def send_confirmation_email(self, data: dict):
        # Simulação de envio de email
        await asyncio.sleep(0.1)
        print(f"Email sent to customer")
    
    async def start_fulfillment(self, data: dict):
        await asyncio.sleep(0.1)
        print(f"Fulfillment started")
    
    async def send_shipping_notification(self, data: dict):
        await asyncio.sleep(0.1)
        print(f"Shipping notification sent")

# CQRS - Command Query Responsibility Segregation
class OrderCommandService:
    """Serviço para comandos (write)"""
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
    
    async def create_order(self, customer_id: str, items: List[dict]):
        import uuid
        order_id = str(uuid.uuid4())
        correlation_id = str(uuid.uuid4())
        
        event = Event(
            type='OrderCreated',
            data={
                'order_id': order_id,
                'customer_id': customer_id,
                'items': items
            },
            timestamp=datetime.now(),
            correlation_id=correlation_id
        )
        
        await self.event_bus.publish(event)
        return order_id

class OrderQueryService:
    """Serviço para queries (read)"""
    def __init__(self, event_store: EventStore):
        self.event_store = event_store
    
    def get_order_state(self, correlation_id: str) -> dict:
        return self.event_store.replay_events(correlation_id)

# Exemplo de uso
async def main():
    event_bus = EventBus()
    event_store = EventStore()
    handlers = OrderEventHandlers(event_bus, event_store)
    
    command_service = OrderCommandService(event_bus)
    query_service = OrderQueryService(event_store)
    
    # Criar pedido
    order_id = await command_service.create_order(
        customer_id='cust_123',
        items=[{'product': 'laptop', 'price': 1000}]
    )
    
    print(f"Order created: {order_id}")

# asyncio.run(main())
```

**Conceitos Críticos:**
- Event Sourcing
- CQRS (Command Query Responsibility Segregation)
- Event Bus e Message Broker
- Eventual Consistency
- Saga Pattern para transações distribuídas

---

## 8. DEVOPS E INFRAESTRUTURA COMO CÓDIGO

### 8.1 Containerização e Orquestração
```yaml
# docker-compose.yml - Ambiente de desenvolvimento
version: '3.8'

services:
  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/myapp
      - REDIS_URL=redis://cache:6379
      - KAFKA_BROKERS=kafka:9092
    depends_on:
      - db
      - cache
      - kafka
    volumes:
      - ./api:/app
    command: uvicorn main:app --host 0.0.0.0 --reload
  
  db:
    image: postgres:15-alpine
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=pass
      - POSTGRES_DB=myapp
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
  
  cache:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
  
  kafka:
    image: confluentinc/cp-kafka:latest
    environment:
      - KAFKA_ZOOKEEPER_CONNECT=zookeeper:2181
      - KAFKA_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092
    depends_on:
      - zookeeper
  
  zookeeper:
    image: confluentinc/cp-zookeeper:latest
    environment:
      - ZOOKEEPER_CLIENT_PORT=2181
  
  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
  
  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
    depends_on:
      - prometheus

volumes:
  postgres_data:
  redis_data:
```

```dockerfile
# Dockerfile - Multi-stage build para produção
FROM python:3.11-slim as builder

WORKDIR /app

# Instalar dependências de build
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-dev \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependências
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage final
FROM python:3.11-slim

WORKDIR /app

# Copiar dependências do builder
COPY --from=builder /root/.local /root/.local

# Copiar código da aplicação
COPY . .

# Adicionar ao PATH
ENV PATH=/root/.local/bin:$PATH

# Criar usuário não-root
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=3s --start-period=40s \
  CMD python -c "import requests; requests.get('http://localhost:8000/health')"

# Comando de inicialização
CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

**Conceitos Fundamentais:**
- Docker e containerização
- Docker Compose para desenvolvimento
- Multi-stage builds para otimização
- Orquestração com Kubernetes
- Service mesh (Istio, Linkerd)

### 8.2 CI/CD Pipeline
```yaml
# .github/workflows/ci-cd.yml - GitHub Actions
name: CI/CD Pipeline

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:15
        env:
          POSTGRES_PASSWORD: postgres
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
          cache: 'pip'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r requirements-dev.txt
      
      - name: Run linters
        run: |
          black --check .
          flake8 .
          mypy .
      
      - name: Run tests
        run: |
          pytest --cov=. --cov-report=xml --cov-report=html
        env:
          DATABASE_URL: postgresql://postgres:postgres@localhost:5432/test
      
      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          files: ./coverage.xml
  
  security-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          format: 'sarif'
          output: 'trivy-results.sarif'
      
      - name: Upload Trivy results to GitHub Security
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: 'trivy-results.sarif'
  
  build-and-push:
    needs: [test, security-scan]
    runs-on: ubuntu-latest
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    
    permissions:
      contents: read
      packages: write
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}
      
      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v4
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=ref,event=branch
            type=sha,prefix={{branch}}-
            type=semver,pattern={{version}}
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
  
  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v3
      
      - name: Configure AWS credentials
        uses: aws-actions/configure-aws-credentials@v2
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1
      
      - name: Deploy to EKS
        run: |
          aws eks update-kubeconfig --name production-cluster
          kubectl set image deployment/api api=${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:main-${{ github.sha }}
          kubectl rollout status deployment/api
```

**Conceitos Críticos:**
- Continuous Integration/Continuous Deployment
- Automated testing e code coverage
- Security scanning (SAST, DAST)
- Container registry e artifact management
- Blue-green deployment e canary releases

---

## 9. SEGURANÇA E PROTEÇÃO DE APLICAÇÕES

### 9.1 Autenticação e Autorização
```python
# Exemplo: Sistema de autenticação JWT com refresh tokens
from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

# Configuração
SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 15
REFRESH_TOKEN_EXPIRE_DAYS = 7

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class AuthService:
    """Serviço de autenticação e autorização"""
    
    def __init__(self, user_repository):
        self.user_repo = user_repository
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        return pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encoded_jwt
    
    def create_refresh_token(self, data: dict):
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        
        return encoded_jwt
    
    def decode_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired"
            )
        except jwt.JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
    
    async def get_current_user(self, token: str = Depends(oauth2_scheme)):
        payload = self.decode_token(token)
        
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type"
            )
        
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        user = await self.user_repo.find_by_id(user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )
        
        return user

# RBAC - Role-Based Access Control
from enum import Enum
from functools import wraps

class Role(str, Enum):
    ADMIN = "admin"
    USER = "user"
    MODERATOR = "moderator"

class Permission(str, Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    ADMIN = "admin"

ROLE_PERMISSIONS = {
    Role.ADMIN: [Permission.READ, Permission.WRITE, Permission.DELETE, Permission.ADMIN],
    Role.MODERATOR: [Permission.READ, Permission.WRITE, Permission.DELETE],
    Role.USER: [Permission.READ, Permission.WRITE]
}

def require_permission(permission: Permission):
    """Decorator para verificar permissões"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, current_user=None, **kwargs):
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated"
                )
            
            user_permissions = ROLE_PERMISSIONS.get(current_user.role, [])
            
            if permission not in user_permissions:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
            
            return await func(*args, current_user=current_user, **kwargs)
        
        return wrapper
    return decorator

# Rate Limiting
from collections import defaultdict
from time import time

class RateLimiter:
    """Rate limiter usando sliding window"""
    
    def __init__(self, max_requests: int, window_seconds: int):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self.requests = defaultdict(list)
    
    def is_allowed(self, key: str) -> bool:
        now = time()
        
        # Remover requisições antigas
        self.requests[key] = [
            req_time for req_time in self.requests[key]
            if now - req_time < self.window_seconds
        ]
        
        # Verificar limite
        if len(self.requests[key]) >= self.max_requests:
            return False
        
        self.requests[key].append(now)
        return True

rate_limiter = RateLimiter(max_requests=100, window_seconds=60)

@app.middleware("http")
async def rate_limit_middleware(request, call_next):
    client_ip = request.client.host
    
    if not rate_limiter.is_allowed(client_ip):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded"
        )
    
    response = await call_next(request)
    return response
```

**Conceitos Fundamentais:**
- JWT (JSON Web Tokens)
- OAuth2 e OpenID Connect
- RBAC (Role-Based Access Control)
- Rate limiting e throttling
- Password hashing (bcrypt, argon2)

### 9.2 Proteção contra Vulnerabilidades
```python
# Exemplo: Proteção contra ataques comuns
from fastapi import Request
from sqlalchemy import text
import bleach
import re

class SecurityMiddleware:
    """Middleware de segurança"""
    
    def __init__(self):
        self.sql_injection_patterns = [
            r"(\bUNION\b.*\bSELECT\b)",
            r"(\bDROP\b.*\bTABLE\b)",
            r"(\bINSERT\b.*\bINTO\b)",
            r"(--|\#|\/\*)",
        ]
    
    def sanitize_input(self, data: str) -> str:
        """Sanitizar entrada para prevenir XSS"""
        # Remover tags HTML perigosas
        allowed_tags = ['p', 'br', 'strong', 'em', 'a']
        allowed_attributes = {'a': ['href', 'title']}
        
        cleaned = bleach.clean(
            data,
            tags=allowed_tags,
            attributes=allowed_attributes,
            strip=True
        )
        
        return cleaned
    
    def check_sql_injection(self, query: str) -> bool:
        """Verificar padrões de SQL injection"""
        for pattern in self.sql_injection_patterns:
            if re.search(pattern, query, re.IGNORECASE):
                return True
        return False
    
    def validate_csrf_token(self, request: Request, token: str) -> bool:
        """Validar token CSRF"""
        session_token = request.session.get('csrf_token')
        return session_token == token

# Prepared Statements - Proteção contra SQL Injection
class SafeDatabase:
    """Wrapper seguro para operações de banco de dados"""
    
    def __init__(self, connection):
        self.conn = connection
    
    def execute_safe(self, query: str, params: dict):
        """Executar query com prepared statements"""
        # Usar parametrização ao invés de concatenação
        stmt = text(query)
        result = self.conn.execute(stmt, params)
        return result
    
    def find_user_safe(self, username: str):
        """Exemplo de query segura"""
        query = "SELECT * FROM users WHERE username = :username"
        result = self.execute_safe(query, {"username": username})
        return result.fetchone()
    
    # ❌ NUNCA FAZER ISSO:
    def find_user_unsafe(self, username: str):
        """Exemplo de query INSEGURA - NÃO USAR"""
        query = f"SELECT * FROM users WHERE username = '{username}'"
        # Vulnerável a SQL injection: username = "admin' OR '1'='1"
        return self.conn.execute(query)

# Content Security Policy
from fastapi.responses import Response

def add_security_headers(response: Response) -> Response:
    """Adicionar headers de segurança"""
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self' 'unsafe-inline'; "
        "style-src 'self' 'unsafe-inline'; "
        "img-src 'self' data: https:;"
    )
    
    return response

@app.middleware("http")
async def security_headers_middleware(request: Request, call_next):
    response = await call_next(request)
    return add_security_headers(response)

# Secrets Management
from cryptography.fernet import Fernet
import os

class SecretsManager:
    """Gerenciamento seguro de secrets"""
    
    def __init__(self):
        # Chave deve vir de variável de ambiente ou vault
        key = os.getenv('ENCRYPTION_KEY')
        if not key:
            raise ValueError("ENCRYPTION_KEY not set")
        
        self.cipher = Fernet(key.encode())
    
    def encrypt(self, data: str) -> str:
        """Criptografar dados sensíveis"""
        encrypted = self.cipher.encrypt(data.encode())
        return encrypted.decode()
    
    def decrypt(self, encrypted_data: str) -> str:
        """Descriptografar dados"""
        decrypted = self.cipher.decrypt(encrypted_data.encode())
        return decrypted.decode()
    
    @staticmethod
    def get_secret_from_vault(secret_name: str) -> str:
        """Obter secret de um vault (AWS Secrets Manager, HashiCorp Vault)"""
        # Exemplo com AWS Secrets Manager
        import boto3
        
        client = boto3.client('secretsmanager')
        response = client.get_secret_value(SecretId=secret_name)
        
        return response['SecretString']
```

**Conceitos Críticos:**
- OWASP Top 10
- SQL Injection prevention
- XSS (Cross-Site Scripting) protection
- CSRF (Cross-Site Request Forgery) tokens
- Security headers (CSP, HSTS)
- Secrets management

---

## 10. OBSERVABILIDADE E MONITORAMENTO

### 10.1 Logging Estruturado
```python
# Exemplo: Sistema de logging estruturado
import logging
import json
from datetime import datetime
from typing import Any, Dict
import traceback

class StructuredLogger:
    """Logger com formato estruturado (JSON)"""
    
    def __init__(self, service_name: str):
        self.service_name = service_name
        self.logger = logging.getLogger(service_name)
        self.logger.setLevel(logging.INFO)
        
        # Handler para stdout
        handler = logging.StreamHandler()
        handler.setFormatter(self._get_formatter())
        self.logger.addHandler(handler)
    
    def _get_formatter(self):
        """Formatter customizado para JSON"""
        class JsonFormatter(logging.Formatter):
            def format(self, record):
                log_data = {
                    'timestamp': datetime.utcnow().isoformat(),
                    'level': record.levelname,
                    'service': record.name,
                    'message': record.getMessage(),
                    'module': record.module,
                    'function': record.funcName,
                    'line': record.lineno
                }
                
                # Adicionar contexto extra
                if hasattr(record, 'extra'):
                    log_data.update(record.extra)
                
                # Adicionar exception se houver
                if record.exc_info:
                    log_data['exception'] = {
                        'type': record.exc_info[0].__name__,
                        'message': str(record.exc_info[1]),
                        'traceback': traceback.format_exception(*record.exc_info)
                    }
                
                return json.dumps(log_data)
        
        return JsonFormatter()
    
    def info(self, message: str, **kwargs):
        extra = {'extra': kwargs}
        self.logger.info(message, extra=extra)
    
    def error(self, message: str, **kwargs):
        extra = {'extra': kwargs}
        self.logger.error(message, extra=extra, exc_info=True)
    
    def warning(self, message: str, **kwargs):
        extra = {'extra': kwargs}
        self.logger.warning(message, extra=extra)

# Distributed Tracing com OpenTelemetry
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

def setup_tracing(service_name: str):
    """Configurar distributed tracing"""
    # Configurar provider
    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)
    
    # Configurar exporter (Jaeger)
    jaeger_exporter = JaegerExporter(
        agent_host_name="localhost",
        agent_port=6831,
    )
    
    # Adicionar span processor
    span_processor = BatchSpanProcessor(jaeger_exporter)
    trace.get_tracer_provider().add_span_processor(span_processor)
    
    return tracer

# Instrumentar FastAPI
FastAPIInstrumentor.instrument_app(app)

# Usar tracing em funções
tracer = setup_tracing("my-service")

@tracer.start_as_current_span("process_order")
async def process_order(order_id: str):
    span = trace.get_current_span()
    span.set_attribute("order.id", order_id)
    
    try:
        # Processar pedido
        result = await do_processing(order_id)
        span.set_attribute("order.status", "success")
        return result
    except Exception as e:
        span.set_attribute("order.status", "failed")
        span.record_exception(e)
        raise

# Context Propagation
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar('request_id', default='')
user_id_var: ContextVar[str] = ContextVar('user_id', default='')

@app.middleware("http")
async def context_middleware(request: Request, call_next):
    import uuid
    
    # Gerar ou extrair request ID
    request_id = request.headers.get('X-Request-ID', str(uuid.uuid4()))
    request_id_var.set(request_id)
    
    # Adicionar ao response
    response = await call_next(request)
    response.headers['X-Request-ID'] = request_id
    
    return response
```

**Conceitos Fundamentais:**
- Structured logging (JSON)
- Distributed tracing (OpenTelemetry, Jaeger)
- Context propagation
- Log aggregation (ELK Stack, Loki)
- Correlation IDs

### 10.2 Métricas e Alertas
```python
# Exemplo: Métricas com Prometheus
from prometheus_client import Counter, Histogram, Gauge, generate_latest
from prometheus_client import CONTENT_TYPE_LATEST
from fastapi import Response
import time

# Definir métricas
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

http_request_duration_seconds = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

active_requests = Gauge(
    'active_requests',
    'Number of active requests'
)

database_connections = Gauge(
    'database_connections_active',
    'Number of active database connections'
)

# Middleware para coletar métricas
@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    active_requests.inc()
    
    start_time = time.time()
    
    try:
        response = await call_next(request)
        
        # Registrar métricas
        duration = time.time() - start_time
        
        http_requests_total.labels(
            method=request.method,
            endpoint=request.url.path,
            status=response.status_code
        ).inc()
        
        http_request_duration_seconds.labels(
            method=request.method,
            endpoint=request.url.path
        ).observe(duration)
        
        return response
    
    finally:
        active_requests.dec()

# Endpoint para Prometheus scraping
@app.get("/metrics")
async def metrics():
    return Response(
        content=generate_latest(),
        media_type=CONTENT_TYPE_LATEST
    )

# Custom Business Metrics
order_total = Counter(
    'orders_total',
    'Total number of orders',
    ['status']
)

revenue_total = Counter(
    'revenue_total_dollars',
    'Total revenue in dollars'
)

@app.post("/orders")
async def create_order(order_data: dict):
    # Criar pedido
    order = await order_service.create(order_data)
    
    # Registrar métricas de negócio
    order_total.labels(status='created').inc()
    revenue_total.inc(order.total)
    
    return order

# Health Checks
from typing import Dict

class HealthCheck:
    """Sistema de health checks"""
    
    def __init__(self):
        self.checks = {}
    
    def register(self, name: str, check_func):
        self.checks[name] = check_func
    
    async def run_checks(self) -> Dict[str, Any]:
        results = {
            'status': 'healthy',
            'checks': {}
        }
        
        for name, check_func in self.checks.items():
            try:
                result = await check_func()
                results['checks'][name] = {
                    'status': 'healthy',
                    'details': result
                }
            except Exception as e:
                results['status'] = 'unhealthy'
                results['checks'][name] = {
                    'status': 'unhealthy',
                    'error': str(e)
                }
        
        return results

health_check = HealthCheck()

# Registrar checks
async def check_database():
    await db.execute("SELECT 1")
    return {'latency_ms': 5}

async def check_redis():
    await redis.ping()
    return {'latency_ms': 2}

health_check.register('database', check_database)
health_check.register('redis', check_redis)

@app.get("/health")
async def health():
    results = await health_check.run_checks()
    status_code = 200 if results['status'] == 'healthy' else 503
    return Response(content=json.dumps(results), status_code=status_code)
```

**Conceitos Críticos:**
- Prometheus metrics (Counter, Gauge, Histogram)
- Grafana dashboards
- Alerting (AlertManager, PagerDuty)
- SLIs, SLOs, SLAs
- Health checks e readiness probes

---

## 11. RECURSOS ADICIONAIS PARA APRENDIZADO

### 11.1 Livros Recomendados
- "Clean Code" - Robert C. Martin
- "Design Patterns" - Gang of Four
- "Domain-Driven Design" - Eric Evans
- "Building Microservices" - Sam Newman
- "The Pragmatic Programmer" - Andrew Hunt

- "Site Reliability Engineering" - Google
- "Designing Data-Intensive Applications" - Martin Kleppmann
- "Release It!" - Michael Nygard

### 11.2 Cursos Online
- Coursera: Software Design and Architecture Specialization
- Udemy: Complete Python Developer Course
- Pluralsight: Becoming a Better Programmer
- MIT: Introduction to Computer Science and Programming
- AWS/GCP/Azure Certification Paths

### 11.3 Comunidades e Fóruns
- Stack Overflow
- GitHub (projetos open source)
- Dev.to
- Reddit r/programming, r/softwareengineering
- LinkedIn Learning paths
- Discord communities (DevOps, Cloud Native)

### 11.4 Ferramentas e Tecnologias Essenciais

**Backend:**
- Python: FastAPI, Django, Flask
- Node.js: Express, NestJS
- Go: Gin, Echo
- Java: Spring Boot

**Frontend:**
- React, Vue.js, Angular
- TypeScript
- Next.js, Nuxt.js
- TailwindCSS, Material-UI

**Databases:**
- PostgreSQL, MySQL
- MongoDB, Redis
- Elasticsearch
- Cassandra, DynamoDB

**DevOps:**
- Docker, Kubernetes
- Terraform, Ansible
- GitHub Actions, GitLab CI
- Prometheus, Grafana

**Cloud Providers:**
- AWS (EC2, S3, Lambda, RDS)
- Google Cloud Platform
- Microsoft Azure
- DigitalOcean, Heroku

---

## Conclusão

Este documento fornece uma base sólida para o desenvolvimento de um modelo de IA especializado em engenharia de software moderna. A ênfase está na integração entre princípios fundamentais, melhores práticas e tecnologias contemporâneas.

**Princípios Orientadores:**
1. **Qualidade de Código**: Manter padrões elevados e consistência
2. **Escalabilidade**: Projetar sistemas que crescem com a demanda
3. **Segurança**: Implementar proteção desde o início do desenvolvimento
4. **Monitoramento**: Observabilidade para manutenção e debugging
5. **Documentação**: Facilitar colaboração e manutenção futura
6. **Automação**: CI/CD e infraestrutura como código
7. **Resiliência**: Design para falhas e recuperação

A combinação de fundamentos sólidos em programação com práticas modernas de desenvolvimento permite não apenas resolver problemas existentes, mas também arquitetar soluções inovadoras e sistemas robustos na engenharia de software contemporânea.

**Áreas de Especialização:**
- Arquitetura de microsserviços e sistemas distribuídos
- DevOps e Site Reliability Engineering (SRE)
- Segurança de aplicações e infraestrutura
- Cloud-native development
- Event-driven architecture e streaming de dados

**Próximos Passos:**
1. Implementar projetos práticos seguindo as arquiteturas apresentadas
2. Contribuir para projetos open source
3. Estudar código de sistemas de produção em larga escala
4. Obter certificações relevantes (AWS, Kubernetes, etc.)
5. Participar de comunidades e conferências técnicas

---

**Versão:** 1.0  
**Data:** Novembro 2024  
**Licença:** MIT

---

*Este documento foi desenvolvido para fine-tuning de modelos de IA especializados em engenharia de software moderna, cobrindo desde fundamentos de programação até arquiteturas avançadas, DevOps, segurança e observabilidade em sistemas distribuídos.*
