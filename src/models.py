'''
This module contains the model of 
all database tables\n
Copyright (c) 2017 Aimirim STI.\n
## Dependencies are:
* sqlalchemy
'''

# Import system libs
from sqlalchemy import Column, ForeignKey, Boolean, Integer, String
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import relationship

# Import custom libs
from .database import Base

#######################################

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    change_password = Column(Boolean, default=False)
    is_admin = Column(Boolean, default=False)

class Collector(Base):
    __tablename__ = "collector"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    ip = Column(String)
    ssh_port = Column(Integer)
    ssh_user = Column(String, nullable=False)
    ssh_pass = Column(String, nullable=False)
    prj_path = Column(String, nullable=False)
    opcua_port = Column(Integer)
    health_port = Column(Integer)
    valid = Column(Boolean, default=False)
    update_period = Column(Integer)
    timeout = Column(Integer)
    # Other tables
    datasources = relationship("DataSource", back_populates="collector")# 1 to N
    
# --------------------
class DataPoint(Base):
    __tablename__ = "datapoints"
    # id = Column(Integer, primary_key=True, index=True)
    # Items
    name = Column(String, primary_key=True, index=True)
    description = Column(String)
    num_type = Column(String)
    access = Column(String, nullable=False)
    active = Column(Boolean, default=True)
    pending = Column(Boolean, default=True)
    upload = Column(Boolean, default=False)
    # Other tables
    datasource = relationship("DataSource", back_populates="datapoints")# N to 1
    datasource_name = Column(Integer, ForeignKey("datasources.name"))
    # Allow inheritance
    __mapper_args__ = {'polymorphic_on': access}
# --------------------

# --------------------
class DataSource(Base):
    __tablename__ = "datasources"
    # id = Column(Integer, primary_key=True, index=True)
    # Items
    name = Column(String, primary_key=True, index=True)
    plc_ip = Column(String)
    plc_port = Column(Integer)
    cycletime = Column(Integer)
    timeout = Column(Integer)
    active = Column(Boolean, default=True)
    pending = Column(Boolean, default=True)
    # Other tables
    protocol = relationship("Protocol", uselist=False)# 1 to 1
    datapoints = relationship("DataPoint", back_populates="datasource")# 1 to N
    collector = relationship("Collector", back_populates="datasources")# N to 1
    collector_id = Column(Integer, ForeignKey("collector.id"))
# --------------------

# --------------------
class Protocol(Base):
    __tablename__ = "protocols"
    id = Column(Integer, primary_key=True, index=True)
    # Items
    name = Column(String, nullable=False)
    # Other tables
    datasource = relationship("DataSource", back_populates="protocol")# 1 to 1
    datasource_name = Column(Integer, ForeignKey("datasources.name"))
    # Allow inheritance
    __mapper_args__ = {'polymorphic_on': name,'polymorphic_identity' : 'protocol'}
# --------------------

# --------------------
class ProtSiemens(Protocol):
    # Inheritance info
    __mapper_args__ = {'polymorphic_identity': 'Siemens'}
    # Items
    @declared_attr
    def rack(cls):
        return Protocol.__table__.c.get('rack', Column(Integer))
    @declared_attr
    def slot(cls):
        return Protocol.__table__.c.get('slot', Column(Integer))
    @declared_attr
    def plc(cls):
        return Protocol.__table__.c.get('plc', Column(String))

class DataSiemens(DataPoint):
    # Inheritance info
    __mapper_args__ = {'polymorphic_identity': 'Siemens'}
    # Items
    @declared_attr
    def address(cls):
        return DataPoint.__table__.c.get('address', Column(String))
# --------------------

# --------------------
class ProtRockwell(Protocol):
    # Inheritance info
    __mapper_args__ = {'polymorphic_identity': 'Rockwell'}
    # Items
    @declared_attr
    def path(cls):
        return Protocol.__table__.c.get('path', Column(String))
    @declared_attr
    def slot(cls):
        return Protocol.__table__.c.get('slot', Column(Integer))
    @declared_attr
    def connection(cls):
        return Protocol.__table__.c.get('connection', Column(String))

class DataRockwell(DataPoint):
    # Inheritance info
    __mapper_args__ = {'polymorphic_identity': 'Rockwell'}
    # Items
    @declared_attr
    def tag_name(cls):
        return DataPoint.__table__.c.get('tag_name', Column(String))
# --------------------

# --------------------
class ProtModbus(Protocol):
    # Inheritance info
    __mapper_args__ = {'polymorphic_identity': 'Modbus'}
    # Items
    @declared_attr
    def slave_id(cls):
        return Protocol.__table__.c.get('slave_id', Column(Integer))

class DataModbus(DataPoint):
    # Inheritance info
    __mapper_args__ = {'polymorphic_identity': 'Modbus'}
    # Items
    @declared_attr
    def func_code(cls):
        return DataPoint.__table__.c.get('func_code', Column(Integer))
    @declared_attr
    def address(cls):
        return DataPoint.__table__.c.get('address', Column(Integer))
# --------------------

# --------------------
IMPLEMENTED_PROT = {
    'Siemens':  ProtSiemens,
    'Rockwell': ProtRockwell,
    'Modbus':   ProtModbus
}

IMPLEMENTED_DATA = {
    'Siemens':  DataSiemens,
    'Rockwell': DataRockwell,
    'Modbus':   DataModbus
}
# --------------------
