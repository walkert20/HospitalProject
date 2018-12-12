import string
import random
from hashlib import md5

alphabet = string.ascii_uppercase + string.digits

def makeId():
   return ''.join([random.choice(alphabet) for _ in range(6)])

def getHash(password):
   return md5(password.encode('utf-8')).hexdigest()
