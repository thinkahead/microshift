import os
import fileinput
import hashlib
import random
from ipython_genutils.py3compat import cast_bytes, str_to_bytes

# Get the password from the environment
password_environment_variable = os.environ.get('JUPYTER_PASSWORD')

# Hash the password, this is taken from https://github.com/jupyter/notebook/blob/master/notebook/auth/security.py
salt_len = 12
algorithm = 'sha1'
h = hashlib.new(algorithm)
salt = ('%0' + str(salt_len) + 'x') % random.getrandbits(4 * salt_len)
h.update(cast_bytes(password_environment_variable, 'utf-8') + str_to_bytes(salt, 'ascii'))
hashed_passphrase = ':'.join((algorithm, salt, h.hexdigest()))
print(hashed_passphrase)

algorithm, salt, pw_digest = hashed_passphrase.split(':', 2)
h = hashlib.new(algorithm)
if len(pw_digest) == 0:
    print("0 length")
else:
    h.update(cast_bytes(password_environment_variable, 'utf-8') + cast_bytes(salt, 'ascii'))
    print(h.hexdigest() == pw_digest)

