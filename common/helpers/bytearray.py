import functools
import struct
from collections import UserList

from common.datatypes import Int8
import os


def to_bytearray_deco(func):
    @functools.wraps(func)
    def wrap(datatype):
        packed = func(datatype)
        array = ByteArray(packed)
        return array

    return wrap


def to_bytearray(data, little_endian=False, signed=False):
    return to_bytearray_deco(lambda datatype: datatype)(data)


class ByteArray(UserList):

    def __init__(self, iterable: bytes):
        self.data = []
        for value in iterable:
            self.data.append(Int8(value))

    def __setitem__(self, key, value):
        try:
            if isinstance(key, slice):
                start = key.start
                stop = key.stop
                if start is None:
                    start = 0
                if stop is None:
                    stop = len(self.data) - 1

                if len(value) > stop - start:
                    raise ValueError("Value is too long")
                elif start < len(self.data) and stop < len(self.data):
                    for item_n, item in enumerate(value):
                        self[start + item_n] = item
                else:
                    raise ValueError()
            elif isinstance(value, Int8):
                self.data[key] = value
            else:
                self.data[key] = Int8(value)
        except IndexError:
            for _ in range(len(self.data), key):
                self.data.append(0)
            if isinstance(value, Int8):
                self.data.append(value)
            else:
                self.data.append(Int8(value))

    def __getitem__(self, item):
        return self.data[item]

    def to_bytes(self, reverse=False):
        if reverse:
            return bytes(self.data[::-1])
        return bytes(self.data)

    def encrypt(self, crypt):
        encrypted = crypt.encrypt(bytes(self))
        self.data = encrypted

    def __repr__(self):
        return str(bytes(self))

    def __bytes__(self):
        return struct.pack("!{}".format("b" * len(self.data)), *[int(i) for i in self.data])

    def pad(self, pad_length):
        self[len(self.data) - 1 + pad_length] = 0

    def append(self, item) -> None:
        array = item.encode()
        self.data = self.data + array.data

    @classmethod
    def random(cls, length):
        return cls(os.urandom(length))
