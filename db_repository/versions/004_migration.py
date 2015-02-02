from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
menu = Table('menu', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('resturant', String(length=64)),
    Column('food', String(length=64)),
)

resturant = Table('resturant', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menu'].create()
    post_meta.tables['resturant'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['menu'].drop()
    post_meta.tables['resturant'].drop()
