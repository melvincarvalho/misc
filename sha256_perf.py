#!/usr/bin/python

# Need to add support for more hash functions for timing.

import base64
import hmac
import hashlib
import faker
import time

# Set up data.
secret = 'Z3IYZSH2UJA7VN3QYFVSVCF7PI'

def encoded_policy():
    json_policy = '{"handle":"KW9EJhYtS6y48Whm2S6D","expiry":1508141504}'
    policy = base64.urlsafe_b64encode(json_policy)
    return policy

def m(secret, encoded_policy, n):
    t1 = time.time()
    for i in range(n):
        x = hmac.new(secret, encoded_policy, hashlib.sha256).hexdigest()
    t2 = time.time()
    return t2-t1


def m2(secret, len_s, n):
    # create random strings of len_s just to see if different strings make a difference
    # in case there is some funkyness with hashing the same string again and again.
    fake = faker.Factory.create()
    _s = fake.text(len_s*n)
    #print len(_s)
    strings = []
    for i in range(len(_s)/len_s - 2):
        f = len_s*i
        t = len_s*i + len_s - 1
        #print f, t
        strings.append(_s[f:t]) 
    t1 = time.time()
    for i in range(len(strings)):
        x = hmac.new(secret, strings[i], hashlib.sha256).hexdigest()
    t2 = time.time()
    return t2-t1

n = 1000
total_time_secs = m(secret, encoded_policy(), n)
#total_time_secs = m2(secret, 100, n)

time_per_hash_micros = total_time_secs * 1000000 / n

print time_per_hash_micros
