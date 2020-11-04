from hashlib import sha1


def get_hash(s, salt=None):
    # 提高字符串的复杂度
    s = "!@#$" + s + "!@$%^"
    if salt:
        s += salt
    sh = sha1()
    sh.update(s.encode("utf-8"))
    return sh.hexdigest()



