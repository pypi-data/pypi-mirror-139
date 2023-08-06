
from sdg_io import SdgIO
from sdg_utils import log_open, DEBUG
from __init__ import Flasher
import os

PATH = 'C:/Users/chernecov/Documents/MCUXpressoIDE_11.5.0_7232/workspace'
OC = 'j:/Prog/eclipse/2017-q2-update/bin/arm-none-eabi-objcopy.exe '
PRJ = 'MIMXRT1051_Project_3'

cmd = f'{OC} -O binary {PATH}/{PRJ}/Debug/{PRJ}.axf {PATH}/{PRJ}/{PRJ}.bin'
print(cmd)
if 0 != os.system(cmd):
    exit()

file = f'{PATH}/{PRJ}/{PRJ}.bin'

# file = 'test.bin'
# with open(file, 'wb') as fd:
#     fd.write(b'\x55'*16*1024)

if __name__ == '__main__':
    log = log_open()
    log.setLevel(DEBUG)
    io = SdgIO('COM13', '115200_O_2', log=log)
    flasher = Flasher(io,
                      filename=file,
                      device='rt1050',
                      opt='wv',
                      addr=bytes([1, ]),
                      reboot=None,
                      log=log)
    flasher.do()
    # flasher.send_fullerase()

