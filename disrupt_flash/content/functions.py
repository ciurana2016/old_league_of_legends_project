import string

from random import choice



def random_string(l):
	return ''.join(choice(string.ascii_uppercase + string.digits + string.ascii_lowercase) for _ in range(l))
