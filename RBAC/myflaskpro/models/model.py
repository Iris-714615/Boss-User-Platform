from . import db

tb_role_res = db.Table('tb_role_res',
                    db.Column('roleid', db.Integer, db.ForeignKey('roles.id')),
                    db.Column('resid', db.Integer, db.ForeignKey('resources.id'))
                             )

#角色表
class Roles(db.Model):
    __tablename__ = 'roles'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    resources = db.relationship('Resources', secondary=tb_role_res, backref=db.backref('roles', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'resources': [resource.to_dict() for resource in self.resources]
        }
  
#用户表，外键关联角色表
class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    role = db.Column(db.Integer, db.ForeignKey('roles.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'role': self.role
        }

#资源表
class Resources(db.Model):
    __tablename__ = 'resources'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    url = db.Column(db.String(100), unique=True, nullable=True)
    pid = db.Column(db.Integer, db.ForeignKey('resources.id'), nullable=True)
    parent = db.relationship('Resources', backref=db.backref('children', remote_side=[id]), lazy=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url,
            'pid': self.pid
        }

#接口表
class Interfaces(db.Model):
    __tablename__ = 'interfaces'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(100), unique=True, nullable=True)
    resource = db.Column(db.Integer, db.ForeignKey('resources.id'))
    
    def to_dict(self):
        return {
            'id': self.id,
            'url': self.url,
            'resource': self.resource
        }
       