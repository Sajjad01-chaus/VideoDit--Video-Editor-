from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context

from app.database.db_models import Base
from app.core import config as app_config  

# Alembic config
alembic_config = context.config

# Override DB URL from app config
alembic_config.set_main_option("sqlalchemy.url", app_config.DATABASE_URL)

# Logging
if alembic_config.config_file_name is not None:
    fileConfig(alembic_config.config_file_name)

# Models metadata
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = alembic_config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        alembic_config.get_section(alembic_config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
