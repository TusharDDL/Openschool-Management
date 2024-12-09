"""Add school_id to classes

Revision ID: 16030629440e
Revises: initial_schema
Create Date: 2024-12-09 04:30:15.774539

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '16030629440e'
down_revision: Union[str, None] = 'initial_schema'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add school_id column to classes table
    op.add_column('classes', sa.Column('school_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'classes', 'schools', ['school_id'], ['id'])

    # Update existing classes with school_id from academic_years
    op.execute("""
        UPDATE classes
        SET school_id = academic_years.school_id
        FROM academic_years
        WHERE classes.academic_year_id = academic_years.id
    """)

    # Make school_id not nullable
    op.alter_column('classes', 'school_id', nullable=False)


def downgrade() -> None:
    # Drop school_id column from classes table
    op.drop_constraint(None, 'classes', type_='foreignkey')
    op.drop_column('classes', 'school_id')