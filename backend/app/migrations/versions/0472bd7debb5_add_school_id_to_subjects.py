"""Add school_id to subjects

Revision ID: 0472bd7debb5
Revises: 16030629440e
Create Date: 2024-12-09 05:13:11.724190

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '0472bd7debb5'
down_revision: Union[str, None] = '16030629440e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add school_id column to subjects table
    op.add_column('subjects', sa.Column('school_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'subjects', 'schools', ['school_id'], ['id'])

    # Update existing subjects with school_id from academic_years
    op.execute("""
        UPDATE subjects s
        SET school_id = (
            SELECT ay.school_id
            FROM academic_years ay
            JOIN classes c ON c.academic_year_id = ay.id
            JOIN teacher_sections ts ON ts.section_id = s.id
            WHERE ts.subject_id = s.id
            LIMIT 1
        )
    """)

    # Make school_id not nullable
    op.alter_column('subjects', 'school_id', nullable=False)


def downgrade() -> None:
    # Drop school_id column from subjects table
    op.drop_constraint(None, 'subjects', type_='foreignkey')
    op.drop_column('subjects', 'school_id')