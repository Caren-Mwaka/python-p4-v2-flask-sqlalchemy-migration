"""rename address again

Revision ID: 9cee90390755
Revises: e5f8bc0ed367
Create Date: 2024-06-28 14:14:22.301410

"""
from alembic import op
import sqlalchemy as sa

# Revision identifiers, used by Alembic.
revision = '9cee90390755'
down_revision = 'e5f8bc0ed367'
branch_labels = None
depends_on = None

def upgrade():
    # Create a new table without the 'location' column
    op.create_table(
        'departments_new',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        # Add other columns except 'location'
    )

    # Copy data from the old table to the new table
    op.execute('''
        INSERT INTO departments_new (id, name)
        SELECT id, name FROM departments
    ''')

    # Drop the old table
    op.drop_table('departments')

    # Rename the new table to the original table name
    op.rename_table('departments_new', 'departments')

def downgrade():
    # Create the old table with the 'location' column
    op.create_table(
        'departments_old',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(50), nullable=False),
        sa.Column('location', sa.String(100)),  # Add 'location' column back
    )

    # Copy data from the new table to the old table
    op.execute('''
        INSERT INTO departments_old (id, name)
        SELECT id, name FROM departments
    ''')

    # Drop the new table
    op.drop_table('departments')

    # Rename the old table to the original table name
    op.rename_table('departments_old', 'departments')
