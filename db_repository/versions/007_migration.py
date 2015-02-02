from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
temporders = Table('temporders', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('email', String(length=120)),
    Column('resturant', String(length=64)),
    Column('food', String(length=64)),
)

tempsel_resturant = Table('tempsel_resturant', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('email', String(length=120)),
    Column('resturant', String(length=120)),
)

sel_resturant = Table('sel_resturant', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('email', String(length=120)),
    Column('resturant', String(length=120)),
    Column('date', DateTime),
)

orders = Table('orders', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('email', String(length=120)),
    Column('resturant', String(length=64)),
    Column('food', String(length=64)),
    Column('date', DateTime),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['temporders'].create()
    post_meta.tables['tempsel_resturant'].create()
    post_meta.tables['sel_resturant'].columns['date'].create()
    post_meta.tables['orders'].columns['date'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['temporders'].drop()
    post_meta.tables['tempsel_resturant'].drop()
    post_meta.tables['sel_resturant'].columns['date'].drop()
    post_meta.tables['orders'].columns['date'].drop()
