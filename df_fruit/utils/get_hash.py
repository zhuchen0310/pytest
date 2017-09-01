# coding=utf-8
import hashlib


# 哈希加密
def get_hash(str, salt=None):
    str = '@#$%' + str + '#$%@'
    if salt:
        str += salt
    sh = hashlib.sha1()
    sh.update(str.encode('utf-8'))
    return sh.hexdigest()
