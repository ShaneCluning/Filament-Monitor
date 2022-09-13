_SET_CONTRAST = 0x81
_SET_ENTIRE_ON = 0xA4
_SET_NORM_INV = 0xA6
_SET_DISP = 0xAE
_SET_MEM_ADDR = 0x20
_SET_COL_ADDR = 0x21
_SET_PAGE_ADDR = 0x22
_SET_DISP_START_LINE = 0x40
_SET_SEG_REMAP = 0xA0
_SET_MUX_RATIO = 0xA8
_SET_IREF_SELECT = 0xAD
_SET_COM_OUT_DIR = 0xC0
_SET_DISP_OFFSET = 0xD3
_SET_COM_PIN_CFG = 0xDA
_SET_DISP_CLK_DIV = 0xD5
_SET_PRECHARGE = 0xD9
_SET_VCOM_DESEL = 0xDB
_SET_CHARGE_PUMP = 0x8D
WIDTH = 128
HEIGHT = 64

from PiicoDev_Unified_slim import *

compat_str = "\nUnified PiicoDev library out of date.  Get the latest module: https://piico.dev/unified \n"

import framebuf


class PiicoDev_SSD1306(framebuf.FrameBuffer):
    def init_display(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.pages = HEIGHT // 8
        self.buffer = bytearray(self.pages * WIDTH)
        for cmd in (
            _SET_DISP,  # display off
            # address setting
            _SET_MEM_ADDR,
            0x00,  # horizontal
            # resolution and layout
            _SET_DISP_START_LINE,  # start at line 0
            _SET_SEG_REMAP | 0x01,  # column addr 127 mapped to SEG0
            _SET_MUX_RATIO,
            HEIGHT - 1,
            _SET_COM_OUT_DIR | 0x08,  # scan from COM[N] to COM0
            _SET_DISP_OFFSET,
            0x00,
            _SET_COM_PIN_CFG,
            0x12,
            # timing and driving scheme
            _SET_DISP_CLK_DIV,
            0x80,
            _SET_PRECHARGE,
            0xF1,
            _SET_VCOM_DESEL,
            0x30,  # 0.83*Vcc
            # display
            _SET_CONTRAST,
            0xFF,  # maximum
            _SET_ENTIRE_ON,  # output follows RAM contents
            _SET_NORM_INV,  # not inverted
            _SET_IREF_SELECT,
            0x30,  # enable internal IREF during display on
            # charge pump
            _SET_CHARGE_PUMP,
            0x14,
            _SET_DISP | 0x01,  # display on
        ):  # on
            self.write_cmd(cmd)

    def poweroff(self):
        self.write_cmd(_SET_DISP)

    def poweron(self):
        self.write_cmd(_SET_DISP | 0x01)

    def setContrast(self, contrast):
        self.write_cmd(_SET_CONTRAST)
        self.write_cmd(contrast)

    def invert(self, invert):
        self.write_cmd(_SET_NORM_INV | (invert & 1))

    def rotate(self, rotate):
        self.write_cmd(_SET_COM_OUT_DIR | ((rotate & 1) << 3))
        self.write_cmd(_SET_SEG_REMAP | (rotate & 1))

    def show(self):
        x0 = 0
        x1 = WIDTH - 1
        self.write_cmd(_SET_COL_ADDR)
        self.write_cmd(x0)
        self.write_cmd(x1)
        self.write_cmd(_SET_PAGE_ADDR)
        self.write_cmd(0)
        self.write_cmd(self.pages - 1)
        self.write_data(self.buffer)

    def write_cmd(self, cmd):
        try:
            self.i2c.writeto_mem(
                self.addr, int.from_bytes(b"\x80", "big"), bytes([cmd])
            )
            self.comms_err = False
        except:
            print(i2c_err_str.format(self.addr))
            self.comms_err = True

    def write_data(self, buf):
        try:
            self.write_list[1] = buf
            self.i2c.writeto_mem(
                self.addr, int.from_bytes(self.write_list[0], "big"), self.write_list[1]
            )
            self.comms_err = False
        except:
            print(i2c_err_str.format(self.addr))
            self.comms_err = True


class PiicoDev_SSD1306_MicroPython(PiicoDev_SSD1306):
    def __init__(self, bus=None, freq=None, sda=None, scl=None, addr=0x3C):
        self.i2c = create_unified_i2c(bus=bus, freq=freq, sda=sda, scl=scl)
        self.addr = addr
        self.temp = bytearray(2)
        self.write_list = [b"\x40", None]  # Co=0, D/C#=1
        self.init_display()
        super().__init__(self.buffer, WIDTH, HEIGHT, framebuf.MONO_VLSB)
        self.fill(0)
        self.show()


def create_PiicoDev_SSD1306(
    address=0x3C, bus=None, freq=None, sda=None, scl=None, asw=None
):
    if asw == 0:
        _a = 0x3C
    elif asw == 1:
        _a = 0x3D
    else:
        _a = address  # parse desired address from direct address input or asw switch position (0 or 1)
    try:
        if compat_ind >= 1:
            pass
        else:
            print(compat_str)
    except:
        print(compat_str)
    display = PiicoDev_SSD1306_MicroPython(
        addr=_a, bus=bus, freq=freq, sda=sda, scl=scl
    )
    return display
