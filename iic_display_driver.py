import smbus
import time

class IICDisplay:

    # commands
    LCD_CLEARDISPLAY = 0x01
    LCD_RETURNHOME = 0x02
    LCD_ENTRYMODESET = 0x04
    LCD_DISPLAYCONTROL = 0x08
    LCD_CURSORSHIFT = 0x10
    LCD_FUNCTIONSET = 0x20
    LCD_SETCGRAMADDR = 0x40
    LCD_SETDDRAMADDR = 0x80

    # flags for display entry mode
    LCD_ENTRYRIGHT = 0x00
    LCD_ENTRYLEFT = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    # flags for display on/off control
    LCD_DISPLAYON = 0x04
    LCD_DISPLAYOFF = 0x00
    LCD_CURSORON = 0x02
    LCD_CURSOROFF = 0x00
    LCD_BLINKON = 0x01
    LCD_BLINKOFF = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00
    LCD_MOVERIGHT = 0x04
    LCD_MOVELEFT = 0x00

    # flags for function set
    LCD_8BITMODE = 0x10
    LCD_4BITMODE = 0x00
    LCD_2LINE = 0x08
    LCD_1LINE = 0x00

    LCD_5x10DOTS = 0x04
    LCD_5x8DOTS = 0x00

    # flags for backlight control
    LCD_BACKLIGHT = 0x08
    LCD_NOBACKLIGHT = 0x00

    En = 0b00000100 # Enable bit
    Rw = 0b00000010 # Read/Write bit
    Rs = 0b00000001 # Register select bit

    def __init__(self, addr, port = 1, width = 14):
        self.bus = smbus.SMBus(port) 
        self.addr = addr
        self.width = width
        self.iic_delay = 0.0001
        self.display_delay = 0.005
    
    # IIC

    # Write a single command
    def IIC_write_cmd(self, cmd):
        self.bus.write_byte(self.addr, cmd)
        time.sleep(self.iic_delay)

    # Write a command and argument
    def IIC_write_cmd_arg(self, cmd, data):
        self.bus.write_byte_data(self.addr, cmd, data)
        time.sleep(self.iic_delay)

    # Write a block of data
    def IIC_write_block_data(self, cmd, data):
        self.bus.write_block_data(self.addr, cmd, data)
        time.sleep(self.iic_delay)

    # Read a single byte
    def IIC_read(self):
        return self.bus.read_byte(self.addr)

    # Read
    def IIC_read_data(self, cmd):
        return self.bus.read_byte_data(self.addr, cmd)

    # Read a block of data
    def IIC_read_block_data(self, cmd):
        return self.bus.read_block_data(self.addr, cmd)

    # Display

    def Init(self):
        self.display_write(0x03)
        self.display_write(0x03)
        self.display_write(0x03)
        self.display_write(0x02)

        self.display_write(self.LCD_FUNCTIONSET | self.LCD_2LINE | self.LCD_5x8DOTS | self.LCD_4BITMODE)
        self.display_write(self.LCD_DISPLAYCONTROL | self.LCD_DISPLAYON)
        self.display_write(self.LCD_CLEARDISPLAY)
        self.display_write(self.LCD_ENTRYMODESET | self.LCD_ENTRYLEFT)

    # clocks EN to latch command
    def display_strobe(self, data):
        self.IIC_write_cmd(data | self.En | self.LCD_BACKLIGHT)
        time.sleep(self.display_delay)
        self.IIC_write_cmd(((data & ~self.En) | self.LCD_BACKLIGHT))
        time.sleep(self.display_delay)

    def display_write_four_bits(self, data):
        self.IIC_write_cmd(data | self.LCD_BACKLIGHT)
        self.display_strobe(data)

    # write a command to lcd
    def display_write(self, cmd, mode=0):
        self.display_write_four_bits(mode | (cmd & 0xF0))
        self.display_write_four_bits(mode | ((cmd << 4) & 0xF0))
      
    #turn on/off the lcd backlight
    def display_backlight(self, state):
        if state == 1:
            self.IIC_write_cmd(self.LCD_BACKLIGHT)
        elif state == 0:
            self.IIC_write_cmd(self.LCD_NOBACKLIGHT)

    # put string function
    def display_display_string(self, string, line):
        if line == 1:
            self.display_write(0x80)
        if line == 2:
            self.display_write(0xC0)
        if line == 3:
            self.display_write(0x94)
        if line == 4:
            self.display_write(0xD4)

        for char in string:
            self.display_write(ord(char), self.Rs)

    # clear lcd and set to home
    def display_clear(self):
        self.display_write(self.LCD_CLEARDISPLAY)
        self.display_write(self.LCD_RETURNHOME)
