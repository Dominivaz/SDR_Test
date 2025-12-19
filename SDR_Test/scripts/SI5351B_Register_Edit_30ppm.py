from smbus import SMBus
from micropython import const
import time

def main():
	R1 =  [const(0x0002), 0x33]
	R2 =  [const(0x0003), 0x00]
	R3 =  [const(0x0004), 0x10]
	R4 =  [const(0x0007), 0x01]
	R5 =  [const(0x000F), 0x00]
	Rx =  [const(0x0010), 0x2F] #Originally second value was 0x0F, turned to 0x80
	R6 =  [const(0x0011), 0x8C] #Originally 0x8C, turned into 80
	R7 =  [const(0x0012), 0x8C] #Originally 0x8C, turned into 80
	R8 =  [const(0x0013), 0x8C] #Originally 0x8C, turned into 80
	R9 =  [const(0x0014), 0x8C] #Originally 0x8C, turned into 80
	R10 = [const(0x0015), 0x8C] #Originally 0x8C, turned into 80
	R11 = [const(0x0016), 0x8C] #Originally 0x8C, turned into 80
	R12 = [const(0x0017), 0x8C] #Originally 0x8C, turned into 80
	R13 = [const(0x0022), 0x42]
	R14 = [const(0x0023), 0x40]
	R15 = [const(0x0024), 0x00]
	R16 = [const(0x0025), 0x10] # originally 0x10, turned to 0x0d
	R17 = [const(0x0026), 0x00]
	R18 = [const(0x0027), 0xF0]
	R19 = [const(0x0028), 0x00]
	R20 = [const(0x0029), 0x00]
	R21 = [const(0x002A), 0x00] # synth0 bits 15:8 fractional divider. maybe we can optimize these?
	R22 = [const(0x002B), 0x04] # 0x04 : Best Values with V = 1.7, synth0 bits 7:0 fractional divider
	R23 = [const(0x002C), 0x00]
	R24 = [const(0x002D), 0x0E]# Originally 0x0d, turned to 0x0c  0x0D : 0x0E Best Values eith V = 1.7. synth0 bits 15:8 integer divider
	R25 = [const(0x002E), 0xE0]# Originally 0xA0, turned to 0x05  0xA0 : 0xE0 Best Values with V = 1.7. synth0 bits 7:0 integer divider
	R26 = [const(0x002F), 0x00] # synth0 bits 19:16 fractional divider. maybe we can optimize these?
	R27 = [const(0x0030), 0x00]
	R28 = [const(0x0031), 0x00]
	
	#Re1 =  [const(0x0032), 0x00]
	#Re2 =  [const(0x0033), 0x01]
	#Re3 =  [const(0x0034), 0x00]
	#Re4 =  [const(0x0035), 0x0D]
	#Re5 =  [const(0x0036), 0x00]
	#Re6 =  [const(0x0037), 0x00]
	#Re7 =  [const(0x0038), 0x00]
	#Re8 =  [const(0x0039), 0x00]
	#Re9 =  [const(0x003A), 0x00]
	#Re10 = [const(0x003B), 0x01]
	#Re11 = [const(0x003C), 0x00]
	#Re12 = [const(0x003D), 0x0D]
	#Re13 = [const(0x003E), 0x00]
	#Re14 = [const(0x003F), 0x00]
	#Re15 = [const(0x0040), 0x00]
	#Re16 = [const(0x0041), 0x00]
	
	R29 = [const(0x005A), 0x00]
	R30 = [const(0x005B), 0x00]
	R31 = [const(0x0095), 0x00]
	R32 = [const(0x0096), 0x00]
	R33 = [const(0x0097), 0x00]
	R34 = [const(0x0098), 0x00]
	R35 = [const(0x0099), 0x00]
	R36 = [const(0x009A), 0x00]
	R37 = [const(0x009B), 0x00]
	R38 = [const(0x00A2), 0x33]##
	R39 = [const(0x00A3), 0x2C]# block to set synth1
	R40 = [const(0x00A4), 0x02]##
	R41 = [const(0x00A5), 0x00]
	
	#Re17 = [const(0x00A6), 0x00]
	#Re18 = [const(0x00A7), 0x00]
	
	R42 = [const(0x00B7), 0x92]
	
	i2cbus = SMBus(1)
	i2caddress = 0x60
	
	#i2cbus.write_byte_data(i2caddress, 0x00, 0x40) #Added the initialize register, hoping to save the configuration
	i2cbus.write_byte_data(i2caddress, R1[0], R1[1])  
	i2cbus.write_byte_data(i2caddress, R2[0], R2[1])  
	i2cbus.write_byte_data(i2caddress, R3[0], R3[1])  
	i2cbus.write_byte_data(i2caddress, R4[0], R4[1])
	i2cbus.write_byte_data(i2caddress, R5[0], R5[1])
	i2cbus.write_byte_data(i2caddress, Rx[0], Rx[1])  
	i2cbus.write_byte_data(i2caddress, R6[0], R6[1])  
	i2cbus.write_byte_data(i2caddress, R7[0], R7[1])  
	i2cbus.write_byte_data(i2caddress, R8[0], R8[1])  
	i2cbus.write_byte_data(i2caddress, R9[0], R9[1])  
	i2cbus.write_byte_data(i2caddress, R10[0], R10[1])
	i2cbus.write_byte_data(i2caddress, R11[0], R11[1])
	i2cbus.write_byte_data(i2caddress, R12[0], R12[1])
	i2cbus.write_byte_data(i2caddress, R13[0], R13[1])
	i2cbus.write_byte_data(i2caddress, R14[0], R14[1])
	i2cbus.write_byte_data(i2caddress, R15[0], R15[1])
	i2cbus.write_byte_data(i2caddress, R16[0], R16[1])
	i2cbus.write_byte_data(i2caddress, R17[0], R17[1])
	i2cbus.write_byte_data(i2caddress, R18[0], R18[1])
	i2cbus.write_byte_data(i2caddress, R19[0], R19[1])
	i2cbus.write_byte_data(i2caddress, R20[0], R20[1])
	i2cbus.write_byte_data(i2caddress, R21[0], R21[1])
	i2cbus.write_byte_data(i2caddress, R22[0], R22[1])
	i2cbus.write_byte_data(i2caddress, R23[0], R23[1])
	i2cbus.write_byte_data(i2caddress, R24[0], R24[1])
	i2cbus.write_byte_data(i2caddress, R25[0], R25[1])
	i2cbus.write_byte_data(i2caddress, R26[0], R26[1])
	i2cbus.write_byte_data(i2caddress, R27[0], R27[1])
	i2cbus.write_byte_data(i2caddress, R28[0], R28[1])
	i2cbus.write_byte_data(i2caddress, R29[0], R29[1])
	i2cbus.write_byte_data(i2caddress, R30[0], R30[1])
	i2cbus.write_byte_data(i2caddress, R31[0], R31[1])
	i2cbus.write_byte_data(i2caddress, R32[0], R32[1])
	i2cbus.write_byte_data(i2caddress, R33[0], R33[1])
	i2cbus.write_byte_data(i2caddress, R34[0], R34[1])
	i2cbus.write_byte_data(i2caddress, R35[0], R35[1])
	i2cbus.write_byte_data(i2caddress, R36[0], R36[1])
	i2cbus.write_byte_data(i2caddress, R37[0], R37[1])
	i2cbus.write_byte_data(i2caddress, R38[0], R38[1])
	i2cbus.write_byte_data(i2caddress, R39[0], R39[1])
	i2cbus.write_byte_data(i2caddress, R40[0], R40[1])
	i2cbus.write_byte_data(i2caddress, R41[0], R41[1])
	i2cbus.write_byte_data(i2caddress, R42[0], R42[1])
	
	
	
	#i2cbus.write_byte_data(i2caddress, Re1[0], Re1[1])
	#i2cbus.write_byte_data(i2caddress, Re2[0], Re2[1])
	#i2cbus.write_byte_data(i2caddress, Re3[0], Re3[1])
	#i2cbus.write_byte_data(i2caddress, Re4[0], Re4[1])
	#i2cbus.write_byte_data(i2caddress, Re5[0], Re5[1])
	#i2cbus.write_byte_data(i2caddress, Re6[0], Re6[1])
	#i2cbus.write_byte_data(i2caddress, Re7[0], Re7[1])
	#i2cbus.write_byte_data(i2caddress, Re8[0], Re8[1])
	#i2cbus.write_byte_data(i2caddress, Re9[0], Re9[1])
	#i2cbus.write_byte_data(i2caddress, Re10[0], Re10[1])
	#i2cbus.write_byte_data(i2caddress, Re11[0], Re11[1])
	#i2cbus.write_byte_data(i2caddress, Re12[0], Re12[1])
	#i2cbus.write_byte_data(i2caddress, Re13[0], Re13[1])
	#i2cbus.write_byte_data(i2caddress, Re14[0], Re14[1])
	#i2cbus.write_byte_data(i2caddress, Re15[0], Re15[1])
	#i2cbus.write_byte_data(i2caddress, Re16[0], Re16[1])
	#i2cbus.write_byte_data(i2caddress, Re17[0], Re17[1])
	#i2cbus.write_byte_data(i2caddress, Re18[0], Re18[1])
	#i2cbus.write_byte_data(i2caddress, 0x00, 0x00) #Added the initialize register, hoping to save the configuration
	
	print('VCXO Configured \n')
	print('Set voltage to 1.6 V to get 28.8 MHz')
	
    
if __name__ == "__main__":
	main()
