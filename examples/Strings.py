import sys
sys.path.append("..")
from iic_display_driver import IICDisplay

display = IICDisplay(addr = 0x27, width = 20)

display.display_string("Test", 1)








