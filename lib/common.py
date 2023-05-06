import json
import hashlib
import time

import struct
import os

def login_auth(func):
    def wrapper(*args,**kwargs):
        from TcpServer import use_data as mu
        # for value in use_data.alive_user.values():
        #     if value[0] == args[0]['session']:
        #         user_id = value[1]
        #         args[0]['user_id'] = user_id
        #         break
        #
        # user_id=args[0].get('user_id',None)
        # if user_id:
        #     func(*args,**kwargs)
        # else:
        #     back_dic={'flag':False,'msg':'您不是授权用户'}
        #     send_back(back_dic,args[1])
        for value in mu.alive_user.values():
            if value[0] == args[0]['session']:
                args[0]['user_id'] = value[1]
                break
        if not args[0].get('user_id', None):
            send_back({'flag': False, 'msg': '您没有登录'}, args[1])
        else:
            return func(*args, **kwargs)
    return wrapper

def send_back(back_dic,conn):
    head_json_bytes = json.dumps(back_dic).encode('utf-8')
    conn.send(struct.pack('i', len(head_json_bytes)))  # 先发报头的长度
    conn.send(head_json_bytes)

def get_uuid(name):
    md=hashlib.md5()
    md.update(name.encode('utf-8'))
    md.update(str(time.clock()).encode('utf-8'))
    return md.hexdigest()

def get_time():
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return now_time

def get_colck_time():
    return str(time.clock())

def get_bigfile_md5(file_path):
    if os.path.exists(file_path):
        md = hashlib.md5()
        file_size = os.path.getsize(file_path)
        file_list = [0, file_size // 3, (file_size // 3) * 2, file_size - 10]
        with open(file_path, 'rb') as f:
            for line in file_list:
                f.seek(line)
                md.update(f.read(10))
        return md.hexdigest()

if __name__ == '__main__':
    print(get_time())