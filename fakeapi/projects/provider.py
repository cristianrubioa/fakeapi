from datetime import UTC
from datetime import datetime
from datetime import timedelta

projects_seed: list[dict] = [
    {
        "id": 1,
        "name": "Core Platform v2",
        "description": "Full rebuild of the core platform with microservices architecture and improved scalability.",
        "status": "active",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC),
    },
    {
        "id": 2,
        "name": "Mobile App Launch",
        "description": "Design, develop, and ship the first mobile application for iOS and Android.",
        "status": "active",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC) + timedelta(days=15),
    },
    {
        "id": 3,
        "name": "Data Pipeline Overhaul",
        "description": "Replace legacy ETL jobs with a real-time streaming data pipeline using modern tooling.",
        "status": "active",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC) + timedelta(days=30),
    },
    {
        "id": 4,
        "name": "Security Hardening",
        "description": "Comprehensive security audit and remediation across all services and infrastructure.",
        "status": "active",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC) + timedelta(days=45),
    },
    {
        "id": 5,
        "name": "Customer Portal Redesign",
        "description": "Redesign the customer-facing portal with a modern UI and improved onboarding flow.",
        "status": "on_hold",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC) + timedelta(days=60),
    },
    {
        "id": 6,
        "name": "AI Integration Sprint",
        "description": "Integrate AI-powered features including smart search, recommendations, and anomaly detection.",
        "status": "active",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC) + timedelta(days=75),
    },
    {
        "id": 7,
        "name": "Infrastructure as Code",
        "description": "Migrate all infrastructure provisioning to Terraform and establish GitOps workflows.",
        "status": "active",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC) + timedelta(days=90),
    },
    {
        "id": 8,
        "name": "Compliance & Audit",
        "description": "Achieve SOC 2 Type II compliance and prepare documentation for external audit.",
        "status": "completed",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC) + timedelta(days=105),
    },
    {
        "id": 9,
        "name": "Developer Experience",
        "description": "Improve internal tooling, documentation, and local development environment setup.",
        "status": "active",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC) + timedelta(days=120),
    },
    {
        "id": 10,
        "name": "Legacy System Sunset",
        "description": "Decommission legacy monolith after migrating all features to the new platform.",
        "status": "archived",
        "created_at": datetime(2024, 1, 1, tzinfo=UTC) + timedelta(days=135),
    },
]
