# Copyright (c) 2014 The Johns Hopkins University/Applied Physics Laboratory
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

"""create_secret_store_metadata_table

Revision ID: 13d127569afa
Revises: 1a0c2cdafb38
Create Date: 2014-04-24 13:15:41.858266

"""

# revision identifiers, used by Alembic.
revision = '13d127569afa'
down_revision = '1a0c2cdafb38'

from alembic import op
import sqlalchemy as sa

from barbican.model import repositories as rep


def upgrade():
    meta = sa.MetaData()
    meta.reflect(bind=rep._ENGINE, only=['secret_store_metadata'])
    if 'secret_store_metadata' not in meta.tables.keys():
        op.create_table(
            'secret_store_metadata',
            sa.Column('id', sa.String(length=36), nullable=False),
            sa.Column('created_at', sa.DateTime(), nullable=False),
            sa.Column('updated_at', sa.DateTime(), nullable=False),
            sa.Column('deleted_at', sa.DateTime(), nullable=True),
            sa.Column('deleted', sa.Boolean(), nullable=False),
            sa.Column('status', sa.String(length=20), nullable=False),
            sa.Column('secret_id', sa.String(length=36), nullable=False),
            sa.Column('key', sa.String(length=255), nullable=False),
            sa.Column('value', sa.String(length=255), nullable=False),
            sa.ForeignKeyConstraint(['secret_id'], ['secrets.id'],),
            sa.PrimaryKeyConstraint('id'),
        )


def downgrade():
    op.drop_table('secret_store_metadata')
