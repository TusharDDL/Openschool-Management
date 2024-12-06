import typer
from sqlalchemy_utils import database_exists, create_database
from app.core.config import get_settings
from app.core.database import engine, Base
from app.scripts.create_superuser import create_superuser
from app.scripts.seed_data import create_test_data
from app.core.database import SessionLocal

settings = get_settings()

def init_db(
    create_superuser: bool = True,
    create_test_data: bool = False
):
    # Create database if it doesn't exist
    if not database_exists(engine.url):
        create_database(engine.url)
        typer.echo(f"Created database: {engine.url}")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    typer.echo("Created database tables")
    
    if create_superuser:
        db = SessionLocal()
        try:
            user = create_superuser(
                db,
                username="admin",
                email="admin@schoolmanagement.com",
                password="admin123"
            )
            typer.echo(f"Created superuser: {user.email}")
        finally:
            db.close()
    
    if create_test_data:
        db = SessionLocal()
        try:
            create_test_data(db)
            typer.echo("Created test data")
        finally:
            db.close()

def main(
    superuser: bool = typer.Option(True, "--superuser/--no-superuser", help="Create default superuser"),
    testdata: bool = typer.Option(False, "--testdata/--no-testdata", help="Create test data")
):
    """Initialize the database with tables and optional data"""
    try:
        init_db(create_superuser=superuser, create_test_data=testdata)
        typer.echo("Database initialization completed successfully!")
    except Exception as e:
        typer.echo(f"Error initializing database: {e}")
        raise typer.Exit(1)

if __name__ == "__main__":
    typer.run(main)