from orm import mysql_singleton

class Fileld:
    def __init__(self,name,column_type,primary_key,default):
        self.name=name
        self.column_type=column_type
        self.primary_key=primary_key
        self.default=default

class StringFileld(Fileld):
    def __init__(self,name=None,column_type='varchar(200)',primary_key=False,default=None):
        super().__init__(name,column_type,primary_key,default)

class IntegerFileld(Fileld):
    def __init__(self,name=None,column_type='int',primary_key=False,default=0):
        super().__init__(name,column_type,primary_key,default)

class ModelsMetaclass(type):
    def __new__(cls,name,bases,attrs):
        if name =='Models':
            return type.__new__(cls,name,bases,attrs)
        table_name=attrs.get('table_name',None)

        primary_key=None
        mappings=dict()
        for k,v in attrs.items():
            if isinstance(v,Fileld):
                mappings[k]=v
                if v.primary_key:
                    if primary_key:
                        raise TypeError('主键重复：%s' %k)
                    primary_key=k

        for k in mappings.keys():
            attrs.pop(k)
        if not primary_key:
            raise TypeError('没有主键')
        attrs['table_name']=table_name
        attrs['primary_key']=primary_key
        attrs['mappings']=mappings
        return type.__new__(cls,name,bases,attrs)

class Models(dict,metaclass=ModelsMetaclass):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def __setattr__(self, key, value):
        self[key]=value

    def __getattr__(self, item):
        try:
            return self[item]
        except TypeError:
            print('没有该属性')

    @classmethod
    def select_one(cls,**kwargs):
        key=list(kwargs)[0]
        value=kwargs[key]
        sql='select * from %s where %s=?' %(cls.table_name,key)
        sql=sql.replace('?','%s')
        ms=mysql_singleton.Mysql()
        re=ms.select(sql,value)
        if re:
            u=cls(**re[0])
            return u
        else:
            return

    @classmethod
    def select_all(cls,**kwargs):
        ms=mysql_singleton.Mysql()
        if kwargs:
            key=list(kwargs.keys())[0]
            value=kwargs[key]
            sql='select * from %s where %s=?' %(cls.table_name,key)
            sql=sql.replace('?','%s')
            re=ms.select(sql,value)
        else:
            sql='select * from %s' %cls.table_name
            re=ms.select(sql)
        if re:
            list_obj=[cls(**r) for r in re]
            return list_obj
        else:
            return

    def update(self):
        ms=mysql_singleton.Mysql()
        filed=[]
        pr=None
        args=[]
        for k,v in self.mappings.items():
            if v.primary_key:
                pr=getattr(self,v.name,None)
            else:
                filed.append(v.name + '=?')
                args.append(getattr(self,v.name,v.default))
        sql='update %s set %s where %s=%s' %(self.table_name,','.join(filed),self.primary_key,pr)
        sql=sql.replace('?','%s')
        ms.execute(sql,args)

    def save(self):
        ms=mysql_singleton.Mysql()
        filed=[]
        values=[]
        args=[]
        for k,v in self.mappings.items():
            if not v.primary_key:
                filed.append(v.name)
                values.append('?')
                args.append(getattr(self,v.name,v.default))
        sql='insert into %s (%s) VALUES (%s)' %(self.table_name,','.join(filed),','.join(values))
        sql=sql.replace('?','%s')
        ms.execute(sql,args)

class User(Models):
    table_name='user'
    id=IntegerFileld('id',primary_key=True)
    name=StringFileld('name')
    password=StringFileld('password')

class Notic(Models):
    table_name='notice'
    id=IntegerFileld('id',primary_key=True)
    name=StringFileld('name')
    content=StringFileld('content')
    user_id=IntegerFileld('user_id')

if __name__ == '__main__':
    user=User.select_one(id=1)
    print(user)