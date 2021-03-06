import ctypes
import random

from .base import DataType


class Int:
    ctype = ctypes.c_int
    signed = True

    def __init__(self, value):
        from common.helpers.bytearray import ByteArray

        if isinstance(value, (Int, DataType)):
            super(self.ctype, self).__init__(value.value)
        elif isinstance(value, list):
            super(self.ctype, self).__init__(int.from_bytes(bytes(ByteArray(value)), "little"))
        else:
            super(self.ctype, self).__init__(int(value))

    @property
    def length(self):
        return ctypes.sizeof(self.ctype)

    def encode(self):
        from common.helpers.bytearray import ByteArray

        return ByteArray(self.value.to_bytes(self.length, "little", signed=self.signed))

    @classmethod
    def decode(cls, data):
        from common.helpers.bytearray import ByteArray

        if isinstance(data, list):
            data = bytes(ByteArray(data))
        return cls(int.from_bytes(data, "little", signed=cls.signed))

    @classmethod
    def new(cls, value):
        return cls(value)

    def __and__(self, other: int):
        if isinstance(other, Int):
            return self.new(self.value & other.value)
        return self.new(self.value & other)

    def __lshift__(self, other):
        if isinstance(other, Int):
            return self.new(self.value << other.value)
        return self.new(self.value << other)

    def __rshift__(self, other):
        if isinstance(other, Int):
            return self.new(self.value >> other.value)
        return self.new(self.value >> other)

    def __xor__(self, other):
        if isinstance(other, Int):
            return self.new(self.value ^ other.value)
        return self.new(self.value ^ other)

    def __ixor__(self, other):
        self.value = (self ^ other).value
        return self

    def __or__(self, other):
        if isinstance(other, Int):
            return self.new(self.value | other.value)
        return self.new(self.value | other)

    def __ior__(self, other):
        self.value = (self | other).value
        return self

    def __add__(self, other):
        if isinstance(other, Int):
            return self.new(self.value + other.value)
        return self.new(self.value + other)

    def __iadd__(self, other):
        self.value = (self.value + other).value
        return self

    def __radd__(self, other):
        return self + other

    def __repr__(self):
        return str(self.value)

    def __bytes__(self):
        value = ctypes.c_uint(self.value)
        return bytes(value.value)

    def __sub__(self, other):
        if isinstance(other, Int):
            return self.new(self.value - other.value)
        return self.new(self.value - other)

    def __isub__(self, other):
        self.value = (self - other).value
        return self

    def __lt__(self, other):
        if isinstance(other, Int):
            return self.value < other.value
        else:
            return self.value < other

    def __gt__(self, other):
        if isinstance(other, Int):
            return self.value > other.value
        else:
            return self.value > other

    def __ge__(self, other):
        if isinstance(other, Int):
            return self.value >= other.value
        return self.value >= other

    def __int__(self):
        return self.value

    def __eq__(self, other):
        if isinstance(other, Int):
            return self.value == other.value
        else:
            return self.value == other

    def __len__(self):
        return ctypes.sizeof(self.ctype)

    def __reversed__(self):
        return self.new(self.encode().data[::-1])

    @classmethod
    def random(cls):
        size = ctypes.sizeof(cls.ctype) * 8
        limit = 2 ** (size) - 1 if cls.signed else 2 ** size
        if cls.signed:
            return cls(random.randrange(-limit, limit - 1))
        else:
            return cls(random.randrange(0, limit - 1))

    def __iter__(self):
        return iter(self.encode().data)

    def __hash__(self):
        return hash(self.value)

    def __mul__(self, other):
        if isinstance(other, Int):
            return self.value * other.value
        return self.value * other


class UInt(Int):
    ctype = ctypes.c_uint
    signed = False


class Int8(Int, ctypes.c_int8):
    ctype = ctypes.c_int8


class Int16(Int, ctypes.c_int16):
    ctype = ctypes.c_int16


class Int32(Int, ctypes.c_int32):
    ctype = ctypes.c_int32


class Int64(Int, ctypes.c_int64):
    ctype = ctypes.c_int64


class UInt8(UInt, ctypes.c_uint8):
    ctype = ctypes.c_uint8


class UInt16(UInt, ctypes.c_uint16):
    ctype = ctypes.c_uint16


class UInt32(UInt, ctypes.c_uint32):
    ctype = ctypes.c_uint32


class Bool(Int, ctypes.c_bool):
    ctype = ctypes.c_bool
