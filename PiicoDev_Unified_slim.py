compat_ind = 1
i2c_err_str = (
    "PiicoDev could not communicate with module at address 0x{:02X}, check wiring"
)

from machine import I2C, Pin


class I2CBase:
    def writeto_mem(self, addr, memaddr, buf, *, addrsize=8):
        raise NotImplementedError("writeto_mem")

    def readfrom_mem(self, addr, memaddr, nbytes, *, addrsize=8):
        raise NotImplementedError("readfrom_mem")

    def write8(self, addr, buf, stop=True):
        raise NotImplementedError("write")

    def read16(self, addr, nbytes, stop=True):
        raise NotImplementedError("read")

    def __init__(self, bus=None, freq=None, sda=None, scl=None):
        raise NotImplementedError("__init__")


class I2CUnifiedMachine8266(I2CBase):
    def __init__(self):

        self.i2c = I2C(freq=100000, sda=Pin(4), scl=Pin(5))

        self.writeto_mem = self.i2c.writeto_mem
        self.readfrom_mem = self.i2c.readfrom_mem

    def write8(self, addr, reg, data):
        if reg is None:
            self.i2c.writeto(addr, data)
        else:
            self.i2c.writeto(addr, reg + data)

    def read16(self, addr, reg):
        self.i2c.writeto(addr, reg, False)
        return self.i2c.readfrom(addr, 2)


def create_unified_i2c(bus=None, freq=None, sda=None, scl=None):
    i2c = I2CUnifiedMachine8266()
    return i2c
