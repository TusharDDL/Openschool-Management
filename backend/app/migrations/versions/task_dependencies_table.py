"""task dependencies table

Revision ID: task_dependencies_table
Revises: combined_tables
Create Date: 2024-01-01 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'task_dependencies_table'
down_revision: Union[str, None] = 'combined_tables'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create task_dependencies table
    op.create_table(
        'task_dependencies',
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('depends_on_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['task_id'], ['onboarding_tasks.id'], ),
        sa.ForeignKeyConstraint(['depends_on_id'], ['onboarding_tasks.id'], ),
        sa.PrimaryKeyConstraint('task_id', 'depends_on_id')
    )


def downgrade() -> None:
    # Drop task_dependencies table
    op.drop_table('task_dependencies')