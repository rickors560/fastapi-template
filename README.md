# FastAPI Production Template

A production-ready FastAPI template with built-in support for database migrations, background jobs, event processing, and comprehensive logging.

## Features

- FastAPI framework with async support
- PostgreSQL database integration using SQLModel
- Alembic database migrations
- APScheduler for background jobs
- Event polling system with exponential backoff
- Structured logging with request tracking
- CORS middleware with environment-based configuration
- Global exception handling
- Docker support with multi-stage builds
- Health check endpoint
- Interactive API documentation (Swagger UI and ReDoc)

## Prerequisites

- Python 3.13 or higher
- PostgreSQL 12 or higher
- Docker (optional, for containerized deployment)

## Project Structure

```
fastapi-template/
├── src/
│   ├── app.py                  # FastAPI application setup
│   ├── db/                     # Database configuration
│   │   ├── context.py          # Database session management
│   │   └── listeners.py        # SQLAlchemy event listeners
│   ├── entities/               # Database models
│   │   ├── base/               # Base entity mixins
│   │   └── sample_entity.py    # Example entity
│   ├── events/                 # Event processing system
│   │   ├── pollers/            # Event pollers
│   │   └── processor/          # Event processors
│   ├── exceptions/             # Exception handlers
│   ├── jobs/                   # Scheduled jobs
│   │   ├── base_job.py         # Base job class
│   │   ├── configure_scheduler.py
│   │   └── sample_job.py       # Example job
│   ├── middlewares/            # Custom middlewares
│   ├── routes/                 # API routes
│   └── utils/                  # Utility functions
├── migrations/                 # Alembic migration files
├── main.py                     # Application entry point
├── pyproject.toml             # Project dependencies (uv)
├── requirements.txt           # UV version pinning
├── Dockerfile                 # Multi-stage Docker build
└── alembic.ini               # Alembic configuration

```

## Installation and Setup

### Using UV (Recommended)

UV is a fast Python package installer and resolver. It's the recommended way to manage dependencies for this project.

#### Install UV

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Or using pip
pip install uv
```

#### Setup Project

1. Clone the repository:
```bash
git clone <repository-url>
cd fastapi-template
```

2. Create environment configuration:
```bash
# Copy the example environment file
cp .env.example .env.local

# Edit .env.local with your configuration
nano .env.local
```

3. Install dependencies:
```bash
# UV will automatically create a virtual environment and install dependencies
uv sync
```

4. Activate the virtual environment:
```bash
# The virtual environment is located at .venv/
source .venv/bin/activate  # On Linux/macOS
# or
.venv\Scripts\activate     # On Windows
```

### Using Traditional Pip

If you prefer using pip instead of uv:

```bash
# Create virtual environment
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # On Linux/macOS
# or
.venv\Scripts\activate     # On Windows

# Install dependencies
pip install -e .
```

## Configuration

### Environment Variables

The application uses environment-specific configuration files. Create a `.env.<environment>` file based on `.env.example`:

- `.env.local` - Local development
- `.env.dev` - Development environment
- `.env.qa` - QA environment
- `.env.prod` - Production environment

Set the `APP_PROFILE` environment variable to switch between configurations:

```bash
export APP_PROFILE=local   # Uses .env.local
export APP_PROFILE=prod    # Uses .env.prod
```

### Key Configuration Options

| Variable | Description | Example |
|----------|-------------|---------|
| HOST | Server bind address | 0.0.0.0 |
| PORT | Server port | 8080 |
| WORKERS | Number of worker processes | 1 |
| CORS_ALLOWED_ORIGINS | Allowed CORS origins | * or https://example.com,https://api.example.com |
| DATABASE_URL | PostgreSQL connection string | postgresql+psycopg://user:pass@localhost:5432/db |
| DATABASE_SCHEMA | Database schema name | public |
| JOB_STORE_DATABASE_SCHEMA | Schema for APScheduler job storage | public_job_store |

## Database Setup

### Initialize Database

Ensure PostgreSQL is running and the database specified in `DATABASE_URL` exists.

### Create Initial Migration

```bash
# Generate a new migration based on your models
alembic revision --autogenerate -m "Initial migration"

# Review the generated migration file in migrations/versions/

# Apply the migration
alembic upgrade head
```

### Alembic Commands

```bash
# Create a new migration
alembic revision --autogenerate -m "description of changes"

# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# Show current revision
alembic current

# Show migration history
alembic history

# Show SQL for migration without applying
alembic upgrade head --sql
```

## Running the Application

### Development Mode

```bash
# Using UV
uv run python main.py

# Or with activated virtual environment
python main.py
```

The application will start with:
- Auto-reload enabled
- Debug logging
- Running on http://0.0.0.0:8080 (or configured HOST:PORT)

### Production Mode

```bash
# Set production profile
export APP_PROFILE=prod

# Run the application
python main.py
```

Production mode features:
- No auto-reload
- Info-level logging
- Multiple workers (as configured)
- Optimized for performance

## API Documentation

Once the application is running, access the interactive API documentation:

### Swagger UI
```
http://localhost:8080/docs
```
Interactive API documentation with the ability to test endpoints directly in the browser.

### ReDoc
```
http://localhost:8080/redoc
```
Alternative API documentation with a clean, three-panel design.

### Health Check
```
http://localhost:8080/health
```
Returns the health status of the application.

## Docker Deployment

### Build Docker Image

```bash
# Build the image
docker build -t fastapi-template:latest .

# Build with specific target
docker build --target runtime -t fastapi-template:latest .
```

### Run with Docker

```bash
# Run the container
docker run -d \
  --name fastapi-app \
  -p 8080:8080 \
  -e APP_PROFILE=prod \
  -e DATABASE_URL=postgresql+psycopg://user:pass@host:5432/db \
  fastapi-template:latest

# View logs
docker logs -f fastapi-app

# Stop container
docker stop fastapi-app

# Remove container
docker rm fastapi-app
```

### Docker Compose (Example)

Create a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8080:8080"
    environment:
      - APP_PROFILE=prod
      - DATABASE_URL=postgresql+psycopg://postgres:password@db:5432/appdb
    depends_on:
      - db
    restart: unless-stopped

  db:
    image: postgres:16-alpine
    environment:
      - POSTGRES_DB=appdb
      - POSTGRES_USER=postgres
      - POSTGRES_PASSWORD=password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

volumes:
  postgres_data:
```

Run with Docker Compose:

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v
```

## Background Jobs

### Creating a New Job

1. Create a new job class in `src/jobs/`:

```python
from src.jobs.base_job import BaseJob
from src import settings
import logging

class MyCustomJob(BaseJob):
    def __init__(self):
        super().__init__(
            name="my_custom_job",
            cron_expression="0 */6 * * *",  # Every 6 hours
            replace_existing=True
        )
        self.__logger__ = logging.getLogger(__name__)

    def run(self):
        self.__logger__.info("Running custom job")
        # Your job logic here
```

2. Register the job in `src/jobs/__init__.py`:

```python
from .my_custom_job import MyCustomJob

my_custom_job = MyCustomJob()
my_custom_job.register_job(scheduler)
```

### Cron Expression Format

```
* * * * *
│ │ │ │ │
│ │ │ │ └─── Day of week (0-6, Sunday=0)
│ │ │ └───── Month (1-12)
│ │ └─────── Day of month (1-31)
│ └───────── Hour (0-23)
└─────────── Minute (0-59)
```

Examples:
- `"0 * * * *"` - Every hour
- `"*/15 * * * *"` - Every 15 minutes
- `"0 0 * * *"` - Daily at midnight
- `"0 9 * * 1-5"` - Weekdays at 9 AM

## Event Processing

### Creating a Custom Event Processor

1. Create a processor in `src/events/processor/`:

```python
from src.events.processor.base_event_processor import BaseEventProcessor
import logging

class MyEventProcessor(BaseEventProcessor):
    def __init__(self):
        self.__logger__ = logging.getLogger(__name__)

    async def process(self, event):
        self.__logger__.info(f"Processing event: {event}")
        # Your event processing logic here
```

2. Create a poller in `src/events/pollers/`:

```python
from src.events.pollers.sample_event_poller import SampleEventPoller

class MyEventPoller(SampleEventPoller):
    def __receive__(self):
        # Implement your message receiving logic
        # Return list of messages to process
        return []
```

3. Register in `src/events/register_event_pollers.py`:

```python
from .pollers import MyEventPoller
from .processor import MyEventProcessor

async def register_event_pollers():
    processor = MyEventProcessor()
    poller = MyEventPoller(processor)
    await poller.poll_messages()
```

## Testing

Run tests using pytest:

```bash
# Install test dependencies
uv pip install pytest pytest-asyncio pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html
```

## Logging

The application uses structured logging with the following features:

- Request ID and Correlation ID tracking
- Automatic request/response logging
- Environment-based log levels (DEBUG for local, INFO for production)
- Process ID logging for multi-worker setups

Log format:
```
2024-11-24 10:30:45 - INFO [pid:12345] - module.name - Log message
```

## Production Checklist

Before deploying to production:

- [ ] Set `APP_PROFILE=prod`
- [ ] Configure `CORS_ALLOWED_ORIGINS` with specific domains (not "*")
- [ ] Use strong database credentials
- [ ] Configure appropriate `WORKERS` count (typically 2 * CPU cores + 1)
- [ ] Set up database backups
- [ ] Configure monitoring and alerting
- [ ] Review and adjust connection pool settings in `src/db/context.py`
- [ ] Set up SSL/TLS certificates
- [ ] Configure reverse proxy (nginx/traefik)
- [ ] Enable rate limiting
- [ ] Set up log aggregation

## Troubleshooting

### Database Connection Issues

```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Test connection
psql -h localhost -U postgres -d your_database

# Check DATABASE_URL format
echo $DATABASE_URL
```

### Migration Issues

```bash
# Check current migration status
alembic current

# Show pending migrations
alembic history

# Reset migrations (caution: data loss)
alembic downgrade base
alembic upgrade head
```

### Import Errors

```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
uv sync --refresh
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or contributions, please open an issue on the project repository.

