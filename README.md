# Audit Manager - Aurora GeoEnergy

Sistema de gerenciamento de releases com workflow de aprovação e auditoria completa.

### Componentes

- **Frontend (Angular)**: SPA com páginas de Applications, Releases e Approvals
- **API Gateway (Node.js)**: Orquestração de rotas, autenticação JWT
- **Application Service (Flask/Python)**: Lógica de negócio e persistência
- **MySQL**: Banco de dados relacional com migrations (Alembic)

## Tecnologias Utilizadas

### Backend

- **Python 3.11** com Flask 3.1
- **SQLAlchemy 2.0** (ORM)
- **Alembic** (Migrations)
- **PyMySQL** (Driver MySQL)
- **Pytest** (Testes)

### Frontend

- **Angular 19**
- **TypeScript**
- **RxJS**
- **Angular Material** (UI Components)

### API Gateway

- **Node.js 20**
- **Express.js**
- **JWT** (Autenticação)

### Infraestrutura

- **Docker** & **Docker Compose**
- **MySQL 8.0**

## Setup e Instalação

### Pré-requisitos

- Docker 20.10+
- Docker Compose 2.0+
- 4GB RAM disponível
- Portas disponíveis: 3000, 4200, 5000, 3306, 5672, 15672

### Instalação Rápida

Execute o script de setup:

```bash
./setup.sh
```

O script irá:

1. Copiar `.env.example` para `.env` (se não existir)
2. Parar containers existentes (`docker-compose down`)
3. Construir e iniciar todos os serviços (`docker-compose up --build -d`)

### Acesso aos Serviços

Após a inicialização:

| Serviço                 | URL                    | Credenciais   |
| ----------------------- | ---------------------- | ------------- |
| **Frontend**            | http://localhost:4200  | -             |
| **API Gateway**         | http://localhost:3000  | JWT Token     |
| **Application Service** | http://localhost:5000  | JWT Token     |
| **MySQL**               | localhost:3306         | user/password |
| **RabbitMQ Management** | http://localhost:15672 | guest/guest   |

## Workflow de Release

### Diagrama de Estados

```
CREATED → PENDING_PREPROD → APPROVED_PREPROD → PENDING_PROD → APPROVED_PROD → DEPLOYED
            ↓                      ↓                  ↓              ↓
         REJECTED             REJECTED           REJECTED       REJECTED
```

## API Endpoints

### Applications

| Método | Endpoint                  | Descrição         | Autenticação |
| ------ | ------------------------- | ----------------- | ------------ |
| GET    | `/audit/applications`     | Listar aplicações | JWT          |
| POST   | `/audit/applications`     | Criar aplicação   | JWT          |
| GET    | `/audit/applications/:id` | Buscar aplicação  | JWT          |

### Releases

| Método | Endpoint                           | Descrição             | Role Necessária |
| ------ | ---------------------------------- | --------------------- | --------------- |
| GET    | `/audit/releases`                  | Listar releases       | -               |
| GET    | `/audit/releases?application_id=1` | Filtrar por aplicação | -               |
| POST   | `/audit/releases`                  | Criar release         | DEVELOPER       |
| GET    | `/audit/releases/:id`              | Buscar release        | -               |
| POST   | `/audit/releases/:id/approve`      | Aprovar release       | APPROVER        |
| POST   | `/audit/releases/:id/disapprove`   | Reprovar release      | APPROVER        |
| POST   | `/audit/releases/:id/promote`      | Promover release      | DEVOPS          |

## Decisões Técnicas

### 1. Escolha do Python/Flask

**Por quê?**

- Sintaxe clara e expressiva
- Ecossistema robusto (SQLAlchemy, Alembic, Pytest)
- Rápido desenvolvimento e prototipagem
- Excelente para APIs REST

**Alternativas consideradas:**

- Java Spring Boot (mais verboso, curva de aprendizado maior)

### 2. SQLAlchemy ORM

**Por quê?**

- Abstração elegante sobre SQL
- Migrations automáticas com Alembic
- Type safety com Python type hints
- Facilita testes com mock_alchemy

**Trade-off:**

- Performance um pouco inferior a SQL puro
- Curva de aprendizado inicial

### 3. Arquitetura em Camadas

```
Routes → Views → Controllers → Repositories → Models
```

**Por quê?**

- Separação clara de responsabilidades
- Facilita testes unitários
- Facilita manutenção e evolução
- Código mais testável

### 4. RabbitMQ para Notificações

**Por quê?**

- Desacoplamento entre serviços
- Resiliência (retry automático)
- Escalabilidade horizontal
- Padrão Producer/Consumer

**Alternativas consideradas:**

- Envio direto de email (acoplamento forte)
- Webhook (sem garantia de entrega)

### 5. Docker Compose para Orquestração

**Por quê?**

- Setup simplificado
- Consistência entre ambientes
- Networking automático entre containers
- Gestão de volumes e variáveis de ambiente

### 6. Validações de Segurança Simuladas

**Implementação:**

```python
def __simulate_validation(self, release: ReleasesTable) -> Tuple[bool, str]:
    # Simula com 90% de chance de sucesso
    passed = random.random() < 0.9
    evidence_url = f"/evidences/release_{release.id}_evidence.txt"
    return passed, evidence_url
```

**Por quê?**

- Foco na lógica de workflow
- Placeholder para integração futura (SonarQube, OWASP ZAP, etc.)

### 7. Deployment Simulado

**Implementação:**

```python
def __fake_deployment(self, release: ReleasesTable) -> Tuple[bool, str]:
    success = random.random() < 0.9
    logs = f"""
    [{datetime.now()}] Starting deployment...
    [{datetime.now()}] Deploying version {release.version}...
    [{datetime.now()}] {'Deployment successful!' if success else 'Deployment failed!'}
    """
    return success, logs
```

**Por quê?**

- Simula cenários reais (sucesso/falha)
- Gera logs para auditoria
- Facilita demonstração do sistema

## Trade-offs

### 1. Autenticação Simplificada (Headers)

**Decisão:** Usar headers `x-user-role` e `x-user-email` em vez de JWT completo

**Prós:**

- Simplicidade na demonstração
- Foco no workflow de negócio
- Fácil testar diferentes roles

**Contras:**

- Não é seguro para produção
- Falta validação real do token

### 2. SQLite para Testes de Integração

**Decisão:** Usar SQLite in-memory para testes de integração

**Prós:**

- Rápido (sem I/O)
- Isolamento total
- Não requer setup externo

**Contras:**

- Pequenas diferenças com MySQL
- Não testa features específicas do MySQL

**Mitigação:**

- Testes end-to-end no ambiente real (MySQL)
- CI/CD com banco de teste real

### 5. Modelo de Dados Simplificado

**Decisão:** 3 entidades principais (Application, Release, Approval)

**Prós:**

- Atende todos os requisitos
- Simples de entender
- Fácil manutenção

**Contras:**

- Logs de deployment dentro da entidade Release
- Sem versionamento de evidências

## Testes

### Estrutura de Testes

```
src/
├── controllers/
│   ├── *_controller.py
│   └── *_controller_test.py          # 35 testes unitários
├── models/mysql/repositories/
│   ├── *_repository.py
│   └── *_repository_test.py          # 27 testes unitários
└── tests/
    └── integration/
        ├── test_applications_integration.py    # 8 testes

```

### Executar Testes

```bash
# Todos os testes
docker-compose exec application-service pytest src/ -v

# Apenas testes unitários
docker-compose exec application-service pytest src/controllers/ src/models/mysql/repositories/ -v

# Apenas testes de integração
docker-compose exec application-service pytest src/tests/integration/ -v

# Com cobertura
docker-compose exec application-service pytest src/ --cov=src --cov-report=html
```

### Cobertura de Testes

| Categoria        | Quantidade    | Status      |
| ---------------- | ------------- | ----------- |
| **Controllers**  | 35 testes     | 100%        |
| **Repositories** | 27 testes     | 100%        |
| **Integration**  | 8 testes      | 100%        |
| **Total**        | **70 testes** | **Passing** |

### Exemplo de Teste de Integração

## Itens Opcionais Implementados

### 1. Node.js API Gateway (Express)

**Implementação:**

- Orquestração de rotas `/api/*`
- Proxy reverso para Application Service
- Autenticação JWT
- CORS configurado
- Error handling centralizado

**Arquivos:**

- `/api-gateway/src/server.js`
- `/api-gateway/src/middleware/auth.js`

### 2. Docker Compose

**Implementação:**

- Orquestração completa de 6 serviços
- Networking automático
- Health checks para MySQL e RabbitMQ
- Volumes persistentes
- Variáveis de ambiente centralizadas

**Arquivo:** `/docker-compose.yaml`

### 3. Migrations com Alembic

**Implementação:**

- Versionamento completo do schema
- Migration automática no startup
- Histórico de mudanças

**Comandos:**

```bash
# Ver histórico
alembic history

# Aplicar migrations
alembic upgrade head

# Criar nova migration
alembic revision --autogenerate -m "description"
```
