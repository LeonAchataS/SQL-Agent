# SQL Agent - Asistente Inmobiliario Conversacional

Sistema de chatbot conversacional para búsqueda de propiedades inmobiliarias que utiliza LLM (OpenAI) para extraer filtros en lenguaje natural y ejecutar consultas SQL seguras contra una base de datos PostgreSQL.

## 📋 Descripción

Este proyecto implementa un agente conversacional que:
- Recopila 5 filtros esenciales: distrito, área mínima, estado, presupuesto máximo y dormitorios
- Opcionalmente pregunta por hasta 3 filtros adicionales: pet_friendly, balcón, terraza, amoblado, baños
- Genera y ejecuta consultas SQL parametrizadas de forma segura
- Mantiene el contexto de conversación en memoria
- Retorna hasta 5 propiedades que coinciden con los criterios

## 🏗️ Arquitectura del Proyecto

```
SQL-Agent/
├── app/
│   ├── __init__.py
│   ├── config.py                    # Configuración centralizada con Pydantic Settings
│   ├── main.py                      # Punto de entrada FastAPI con lifespan
│   │
│   ├── api/
│   │   └── v1/
│   │       └── agent_router.py      # Endpoints HTTP del agente
│   │
│   ├── models/
│   │   ├── schemas.py               # Schemas Pydantic (request/response)
│   │   └── state.py                 # Estado de conversación
│   │
│   └── services/
│       ├── agent_service.py         # Orquestador principal del agente
│       ├── llm_client.py            # Cliente OpenAI para extracción de filtros
│       ├── parser.py                # Parser que normaliza y valida filtros
│       ├── query_builder.py         # Constructor de SQL parametrizado
│       ├── session_manager.py       # Gestión de sesiones en memoria
│       └── db.py                    # Pool de conexiones asyncpg
│
├── frontend/
│   ├── index.html                   # Interfaz de chat
│   ├── style.css                    # Estilos del chatbot
│   └── script.js                    # Lógica del cliente
│
├── requirements.txt
├── .env.example
└── README.md
```

## 🛠️ Stack Tecnológico

### Backend
- **FastAPI** - Framework web async para Python
- **Pydantic V2** - Validación de datos y configuración
- **OpenAI API** (gpt-4o-mini) - Extracción de filtros con LLM
- **asyncpg** - Driver PostgreSQL async con connection pooling
- **uvicorn** - Servidor ASGI

### Frontend
- **HTML5 + CSS3** - Interfaz moderna y responsive
- **Vanilla JavaScript** - Sin frameworks, fetch API nativo
- **LocalStorage** - Persistencia de session_id

### Base de Datos
- **PostgreSQL** - Base de datos relacional
- **Schema**: `property_infrastructure.propiedad` + `edificio`

## 🚀 Instalación y Configuración

### 1. Requisitos Previos
- Python 3.11+
- PostgreSQL 12+
- OpenAI API Key

### 2. Clonar el Repositorio
```bash
git clone https://github.com/LeonAchataS/SQL-Agent.git
cd SQL-Agent
```

### 3. Crear Entorno Virtual
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 4. Instalar Dependencias
```bash
pip install -r requirements.txt
```

### 5. Configurar Variables de Entorno

Crear archivo `.env` en la raíz del proyecto:

```env
# OpenAI Configuration
OPENAI_API_KEY=sk-your-api-key-here

# Database Configuration
DATABASE_URL=postgresql://user:password@localhost:5432/property_db

# API Configuration (opcional)
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true
```

### 6. Verificar Schema de Base de Datos

El sistema espera las siguientes tablas en PostgreSQL:

```sql
-- Tabla de edificios
CREATE TABLE property_infrastructure.edificio (
    id_edificio SERIAL PRIMARY KEY,
    nombre VARCHAR(255),
    distrito VARCHAR(100),
    direccion TEXT
);

-- Tabla de propiedades
CREATE TABLE property_infrastructure.propiedad (
    id_propiedad SERIAL PRIMARY KEY,
    id_edificio INTEGER REFERENCES property_infrastructure.edificio(id_edificio),
    titulo VARCHAR(255),
    area_m2 DECIMAL(10,2),
    dormitorios INTEGER,
    banios INTEGER,
    estado VARCHAR(50), -- DISPONIBLE, OCUPADA, MANTENIMIENTO, VENDIDA
    valor_comercial DECIMAL(15,2),
    pet_friendly BOOLEAN,
    balcon BOOLEAN,
    terraza BOOLEAN,
    amoblado BOOLEAN
);
```

### 7. Ejecutar el Servidor

```bash
python -m app.main
```

El servidor estará disponible en: `http://localhost:8000`

### 8. Abrir el Frontend

Abrir `frontend/index.html` en el navegador o usar un servidor local:

```bash
# Opción 1: Abrir directamente
start frontend/index.html

# Opción 2: Servidor HTTP simple
cd frontend
python -m http.server 3000
# Visitar http://localhost:3000
```

## 🐳 Instalación con Docker

### Opción 1: Docker Compose (Recomendado)

Incluye PostgreSQL + Aplicación con un solo comando:

```bash
# 1. Crear archivo .env con tu API key
echo "OPENAI_API_KEY=sk-your-api-key" > .env

# 2. Levantar todos los servicios
docker-compose up -d

# 3. Ver logs
docker-compose logs -f app

# 4. Acceder a la aplicación
# Backend: http://localhost:8000
# Frontend: abrir frontend/index.html en el navegador
```

**Servicios incluidos:**
- PostgreSQL en puerto 5432
- API en puerto 8000
- Volumen persistente para datos

**Comandos útiles:**
```bash
# Detener servicios
docker-compose down

# Reconstruir imagen
docker-compose build

# Ver estado
docker-compose ps

# Limpiar todo (incluyendo volúmenes)
docker-compose down -v
```

### Opción 2: Solo Docker (sin PostgreSQL)

Si ya tienes PostgreSQL corriendo:

```bash
# 1. Construir imagen
docker build -t sql-agent .

# 2. Ejecutar contenedor
docker run -d \
  --name sql-agent-app \
  -p 8000:8000 \
  -e OPENAI_API_KEY=sk-your-api-key \
  -e DATABASE_URL=postgresql://user:pass@host.docker.internal:5432/property_db \
  sql-agent

# 3. Ver logs
docker logs -f sql-agent-app

# 4. Detener
docker stop sql-agent-app
docker rm sql-agent-app
```

**Nota:** En Windows/Mac usa `host.docker.internal` para conectar a PostgreSQL en localhost.

## 📡 API Endpoints

### Base URL
```
http://localhost:8000/api/v1/agent
```

### 1. POST /message
Enviar un mensaje al agente y recibir respuesta.

**Request:**
```json
{
  "session_id": "uuid-string-or-null",
  "message": "Quiero un departamento en La Molina"
}
```

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "reply": "¡Perfecto! ¿Cuál es el área mínima que necesitas en m²?",
  "data": null
}
```

**Response (cuando hay resultados):**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "reply": "Encontré 3 propiedades que cumplen con tus criterios. Te las muestro.",
  "data": [
    {
      "id_propiedad": 101,
      "titulo": "Departamento moderno en La Molina",
      "distrito": "La Molina",
      "area_m2": 85.5,
      "dormitorios": 2,
      "banios": 2,
      "estado": "DISPONIBLE",
      "valor_comercial": 350000,
      "pet_friendly": true,
      "balcon": true,
      "terraza": false,
      "amoblado": false
    }
  ]
}
```

### 2. GET /properties/{session_id}
Obtener las propiedades de la última búsqueda ejecutada.

**Response:**
```json
{
  "session_id": "550e8400-e29b-41d4-a716-446655440000",
  "count": 3,
  "properties": [...],
  "sql_query": "SELECT p.id_propiedad, p.titulo, ... WHERE ..."
}
```

### 3. GET /health
Health check del servidor (raíz de la API, no en `/api/v1/agent`).

**Response:**
```json
{
  "status": "ok"
}
```

## 🔧 Configuración Avanzada

### Configuración de LLM

En `app/config.py` puedes ajustar:

```python
llm_model: str = "gpt-4o-mini"  # Modelo de OpenAI
llm_temperature: float = 0.0     # Temperatura (0 = determinístico)
properties_limit: int = 5        # Máximo de propiedades a retornar
```

### Gestión de Sesiones

Las sesiones se almacenan en memoria usando diccionarios Python. Para un entorno de producción considera:
- Redis para sesiones distribuidas
- TTL (Time To Live) para expiración automática
- Persistencia en base de datos

## 🎯 Flujo de Conversación

```mermaid
graph TD
    A[Usuario envía mensaje] --> B[Parser extrae filtros con LLM]
    B --> C{¿Todos los filtros esenciales?}
    C -->|No| D[Preguntar por filtro faltante]
    D --> A
    C -->|Sí| E[Construir SQL parametrizado]
    E --> F[Ejecutar consulta en PostgreSQL]
    F --> G[Retornar propiedades]
    G --> H[Frontend muestra resultados]
```

### Filtros Esenciales (obligatorios)
1. **distrito** - Ubicación geográfica
2. **area_min** - Área mínima en m²
3. **estado** - Estado de la propiedad (DISPONIBLE, OCUPADA, etc.)
4. **presupuesto_max** - Presupuesto máximo
5. **dormitorios** - Cantidad de dormitorios

### Filtros Opcionales (hasta 3)
- **pet_friendly** - Acepta mascotas
- **balcon** - Tiene balcón
- **terraza** - Tiene terraza
- **amoblado** - Está amoblado
- **banios** - Cantidad de baños

## 💡 Ejemplos de Uso

### Conversación Natural
```
👤: "Quiero un departamento en La Molina"
🤖: "¡Perfecto! ¿Cuál es el área mínima que necesitas en m²?"

👤: "80 metros cuadrados"
🤖: "¿Qué estado de propiedad prefieres? Puede ser: DISPONIBLE, OCUPADA, MANTENIMIENTO o VENDIDA"

👤: "Disponible"
🤖: "¿Cuál es tu presupuesto máximo?"

👤: "300000"
🤖: "¿Cuántos dormitorios necesitas?"

👤: "2"
🤖: "Encontré 3 propiedades que cumplen con tus criterios. Te las muestro."
```

### Mensaje con Múltiples Filtros
```
👤: "Busco depto de 2 ambientes en San Isidro de 80m² por 250000"
🤖: "¿Qué estado de propiedad prefieres? Puede ser: DISPONIBLE, OCUPADA, MANTENIMIENTO o VENDIDA"
```

## 🔒 Seguridad

### SQL Injection Prevention
- **Consultas parametrizadas**: Uso de placeholders `$1, $2, $3` con asyncpg
- **Validación con Pydantic**: Todos los filtros pasan por schemas estrictos
- **No concatenación de strings**: Nunca se construye SQL con f-strings

### Validación de Datos
```python
# Ejemplo de schema Pydantic
class FilterEssential(BaseModel):
    distrito: str | None = None
    area_min: float | None = None
    estado: str | None = None
    presupuesto_max: float | None = None
    dormitorios: int | None = None
```

## 🐛 Troubleshooting

### Error: "OPENAI API key not configured"
Verificar que `.env` tenga `OPENAI_API_KEY` configurado correctamente.

### Error: "No module named 'app'"
Ejecutar siempre como módulo: `python -m app.main` (no `python app/main.py`)

### Error de conexión a PostgreSQL
Verificar:
- PostgreSQL está corriendo
- `DATABASE_URL` en `.env` es correcto
- Schema `property_infrastructure` existe
- Tablas `propiedad` y `edificio` existen

### Frontend muestra "placeholder"
- Verificar que el backend esté corriendo (`http://localhost:8000/health`)
- Revisar consola del navegador (F12) para errores
- Verificar que no haya funciones duplicadas en `agent_service.py`

### LLM no extrae filtros correctamente
- Revisar temperatura en config (debe ser 0.0 para determinismo)
- Verificar prompt en `llm_client.py`
- Probar con mensajes más explícitos

## 📊 Estructura de Datos

### ConversationState (en memoria)
```python
{
    "session_id": "uuid",
    "messages": [
        {"role": "user", "content": "mensaje"},
        {"role": "assistant", "content": "respuesta"}
    ],
    "collected_filters": {
        "distrito": "La Molina",
        "area_min": 80,
        "dormitorios": 2,
        ...
    },
    "required_remaining": ["estado", "presupuesto_max"],
    "optional_allowed": 3
}
```

### Query Results Storage
```python
{
    "session_id": {
        "sql": "SELECT ... WHERE ...",
        "results": [{"id_propiedad": 1, ...}]
    }
}
```

## 🔄 Próximas Mejoras

- [ ] Sistema de logging estructurado
- [ ] Tests unitarios con pytest
- [ ] Redis para sesiones distribuidas
- [ ] Rate limiting por sesión
- [ ] Paginación de resultados
- [ ] Historial de conversaciones persistente
- [ ] Métricas con Prometheus
- [ ] Docker Compose para desarrollo
- [ ] CI/CD con GitHub Actions
- [ ] Documentación OpenAPI mejorada

## 📝 Notas de Desarrollo

### Comandos Útiles

```bash
# Ejecutar servidor en desarrollo
python -m app.main

# Ejecutar tests (cuando se implementen)
pytest tests/

# Verificar tipos con mypy
mypy app/

# Formatear código
black app/
isort app/

# Linting
ruff check app/
```

### Estructura de Commits
```
feat: agregar filtro de X
fix: corregir extracción de distrito
refactor: mejorar prompt del LLM
docs: actualizar README
```

## 🌐 Variables de Entorno Completas

```env
# === OpenAI Configuration ===
OPENAI_API_KEY=sk-...
LLM_MODEL=gpt-4o-mini
LLM_TEMPERATURE=0.0

# === Database Configuration ===
DATABASE_URL=postgresql://user:pass@localhost:5432/db
DB_POOL_MIN_SIZE=10
DB_POOL_MAX_SIZE=20

# === API Configuration ===
API_HOST=0.0.0.0
API_PORT=8000
API_RELOAD=true

# === Agent Configuration ===
PROPERTIES_LIMIT=5
SESSION_TTL_SECONDS=3600
```

---

**Última actualización:** Octubre 2025
**Versión:** 1.0.0
