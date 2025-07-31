#pragma once
/* Automatically generated
 * with the command '/home/def/.local/bin/ipxact2c --srcFile example/input/test.xml --destDir example/output'
 *
 * Do not manually edit!
 *
 * Example usage:
 *     uint32_t datareg0 = read(dev, EXAMPLE_REG_ADDRESS_REG0);
 *
 *     uint8_t byte0 = (uint8_t)GET_EXAMPLE_REG0_BYTE0(datareg0);
 *     uint8_t byte1 = (uint8_t)GET_EXAMPLE_REG0_BYTE1(datareg0);
 *     uint8_t byte2 = (uint8_t)GET_EXAMPLE_REG0_BYTE2(datareg0);
 *     uint8_t byte3 = (uint8_t)GET_EXAMPLE_REG0_BYTE3(datareg0);
 *
 *
 *     uint32_t datareg7 = read(dev, EXAMPLE_REG_ADDRESS_REG7);
 *
 *     uint8_t nibble0 = (uint8_t)GET_EXAMPLE_REG7_NIBBLE0(datareg7);
 *     uint8_t nibble1 = (uint8_t)GET_EXAMPLE_REG7_NIBBLE1(datareg7);
 *     uint8_t nibble2 = (uint8_t)GET_EXAMPLE_REG7_NIBBLE2(datareg7);
 */
// ------------------------------------------------
//  Register offsets
// ------------------------------------------------
#define EXAMPLE_REG0_OFFSET	0x00	// write something useful for reg0
#define EXAMPLE_REG1_OFFSET	0x01	// 
#define EXAMPLE_REG2_OFFSET	0x02	// write something useful for reg2
#define EXAMPLE_REG3_OFFSET	0x03	// write something useful for reg3
#define EXAMPLE_REG4_OFFSET	0x04	// reg4 is a very useful register. It can take down the moon when configured correctly.
#define EXAMPLE_REG5_OFFSET	0x05	// reg5 is as useful as reg4 but without a reset value defined.
#define EXAMPLE_REG6_OFFSET	0x06	// reg6 is a read only register.
#define EXAMPLE_REG7_OFFSET	0x07	// write something useful for reg7
#define EXAMPLE_REG8_OFFSET	0x08	// register with empty and no descriptions of the fields


// ------------------------------------------------
//  Bit operations for register reg0
// ------------------------------------------------
#define EXAMPLE_REG0_BYTE0_SHIFT	0
#define EXAMPLE_REG0_BYTE0_MASK 	0xFF
#define EXAMPLE_REG0_BYTE0_MINIMUM 	0x00
#define EXAMPLE_REG0_BYTE0_MAXIMUM 	0x07

#define EXAMPLE_REG0_BYTE1_SHIFT	8
#define EXAMPLE_REG0_BYTE1_MASK 	0xFF

#define EXAMPLE_REG0_BYTE2_SHIFT	16
#define EXAMPLE_REG0_BYTE2_MASK 	0xFF

#define EXAMPLE_REG0_BYTE3_SHIFT	24
#define EXAMPLE_REG0_BYTE3_MASK 	0xFF

// ------------------------------------------------
//  Bit operations for register reg1
// ------------------------------------------------
#define EXAMPLE_REG1_FIELD0_SHIFT	0
#define EXAMPLE_REG1_FIELD0_MASK 	0xFFFFFFFF
#define EXAMPLE_REG1_FIELD0_MINIMUM 	0x00000004
#define EXAMPLE_REG1_FIELD0_MAXIMUM 	0x00000014

// ------------------------------------------------
//  Bit operations for register reg2
// ------------------------------------------------
#define EXAMPLE_REG2_POWER_SHIFT	0
#define EXAMPLE_REG2_POWER_MASK 	0x01

#define EXAMPLE_REG2_POWER2_SHIFT	1
#define EXAMPLE_REG2_POWER2_MASK 	0x01

#define EXAMPLE_REG2_MONKEY_SHIFT	2
#define EXAMPLE_REG2_MONKEY_MASK 	0x03

#define EXAMPLE_REG2_MONKEY2_SHIFT	4
#define EXAMPLE_REG2_MONKEY2_MASK 	0x03

#define EXAMPLE_REG2_MONKEY3_SHIFT	6
#define EXAMPLE_REG2_MONKEY3_MASK 	0x03

#define EXAMPLE_REG2_MONKEY4_SHIFT	8
#define EXAMPLE_REG2_MONKEY4_MASK 	0x03

#define EXAMPLE_REG2_UNUSED0_SHIFT	10
#define EXAMPLE_REG2_UNUSED0_MASK 	0x3FFFFF

// ------------------------------------------------
//  Bit operations for register reg3
// ------------------------------------------------
#define EXAMPLE_REG3_FIELD0_SHIFT	0
#define EXAMPLE_REG3_FIELD0_MASK 	0xFFFFFFFF

// ------------------------------------------------
//  Bit operations for register reg4
// ------------------------------------------------
#define EXAMPLE_REG4_REG4_SHIFT	0
#define EXAMPLE_REG4_REG4_MASK 	0xFFFFFFFF

// ------------------------------------------------
//  Bit operations for register reg5
// ------------------------------------------------
#define EXAMPLE_REG5_REG5_SHIFT	0
#define EXAMPLE_REG5_REG5_MASK 	0xFFFFFFFF

// ------------------------------------------------
//  Bit operations for register reg6
// ------------------------------------------------
#define EXAMPLE_REG6_REG6_SHIFT	0
#define EXAMPLE_REG6_REG6_MASK 	0xFFFFFFFF

// ------------------------------------------------
//  Bit operations for register reg7
// ------------------------------------------------
#define EXAMPLE_REG7_NIBBLE0_SHIFT	0
#define EXAMPLE_REG7_NIBBLE0_MASK 	0x0F

#define EXAMPLE_REG7_UNUSED0_SHIFT	4
#define EXAMPLE_REG7_UNUSED0_MASK 	0x0F

#define EXAMPLE_REG7_NIBBLE1_SHIFT	8
#define EXAMPLE_REG7_NIBBLE1_MASK 	0x0F

#define EXAMPLE_REG7_UNUSED1_SHIFT	12
#define EXAMPLE_REG7_UNUSED1_MASK 	0x0F

#define EXAMPLE_REG7_NIBBLE2_SHIFT	16
#define EXAMPLE_REG7_NIBBLE2_MASK 	0x0F

#define EXAMPLE_REG7_UNUSED2_SHIFT	20
#define EXAMPLE_REG7_UNUSED2_MASK 	0xFFF

// ------------------------------------------------
//  Bit operations for register reg8
// ------------------------------------------------
#define EXAMPLE_REG8_NIBBLE0_SHIFT	0
#define EXAMPLE_REG8_NIBBLE0_MASK 	0x0F

#define EXAMPLE_REG8_UNUSED0_SHIFT	4
#define EXAMPLE_REG8_UNUSED0_MASK 	0x0F

#define EXAMPLE_REG8_NIBBLE1_SHIFT	8
#define EXAMPLE_REG8_NIBBLE1_MASK 	0x0F

#define EXAMPLE_REG8_UNUSED1_SHIFT	12
#define EXAMPLE_REG8_UNUSED1_MASK 	0xFFFFF


// ------------------------------------------------
//  Macro functions for register reg0
//  - GET_EXAMPLE_REG0_BYTE0 : write something useful for field0
//  - GET_EXAMPLE_REG0_BYTE1 : write something useful for field1
//  - GET_EXAMPLE_REG0_BYTE2 : write something useful for field2
//  - GET_EXAMPLE_REG0_BYTE3 : write something useful for field3
// ------------------------------------------------

#define GET_EXAMPLE_REG0_BYTE0(a)	((a >> EXAMPLE_REG0_BYTE0_SHIFT) & EXAMPLE_REG0_BYTE0_MASK)
#define GET_EXAMPLE_REG0_BYTE1(a)	((a >> EXAMPLE_REG0_BYTE1_SHIFT) & EXAMPLE_REG0_BYTE1_MASK)
#define GET_EXAMPLE_REG0_BYTE2(a)	((a >> EXAMPLE_REG0_BYTE2_SHIFT) & EXAMPLE_REG0_BYTE2_MASK)
#define GET_EXAMPLE_REG0_BYTE3(a)	((a >> EXAMPLE_REG0_BYTE3_SHIFT) & EXAMPLE_REG0_BYTE3_MASK)

// ------------------------------------------------
//  Macro functions for register reg1
//  - GET_EXAMPLE_REG1_FIELD0 : write something useful for field0
// ------------------------------------------------

#define GET_EXAMPLE_REG1_FIELD0(a)	((a >> EXAMPLE_REG1_FIELD0_SHIFT) & EXAMPLE_REG1_FIELD0_MASK)

// ------------------------------------------------
//  Macro functions for register reg2
//  - GET_EXAMPLE_REG2_POWER : write something useful for field power
//  - GET_EXAMPLE_REG2_POWER2 : write something useful for field power2
//  - GET_EXAMPLE_REG2_MONKEY : which monkey
//  - GET_EXAMPLE_REG2_MONKEY2 : which monkey
//  - GET_EXAMPLE_REG2_MONKEY3 : which monkey
//  - GET_EXAMPLE_REG2_MONKEY4 : which monkey
//  - GET_EXAMPLE_REG2_UNUSED0 : unused
// ------------------------------------------------

#define GET_EXAMPLE_REG2_POWER(a)	((a >> EXAMPLE_REG2_POWER_SHIFT) & EXAMPLE_REG2_POWER_MASK)
#define GET_EXAMPLE_REG2_POWER2(a)	((a >> EXAMPLE_REG2_POWER2_SHIFT) & EXAMPLE_REG2_POWER2_MASK)
#define GET_EXAMPLE_REG2_MONKEY(a)	((a >> EXAMPLE_REG2_MONKEY_SHIFT) & EXAMPLE_REG2_MONKEY_MASK)
#define GET_EXAMPLE_REG2_MONKEY2(a)	((a >> EXAMPLE_REG2_MONKEY2_SHIFT) & EXAMPLE_REG2_MONKEY2_MASK)
#define GET_EXAMPLE_REG2_MONKEY3(a)	((a >> EXAMPLE_REG2_MONKEY3_SHIFT) & EXAMPLE_REG2_MONKEY3_MASK)
#define GET_EXAMPLE_REG2_MONKEY4(a)	((a >> EXAMPLE_REG2_MONKEY4_SHIFT) & EXAMPLE_REG2_MONKEY4_MASK)
#define GET_EXAMPLE_REG2_UNUSED0(a)	((a >> EXAMPLE_REG2_UNUSED0_SHIFT) & EXAMPLE_REG2_UNUSED0_MASK)

// ------------------------------------------------
//  Macro functions for register reg3
//  - GET_EXAMPLE_REG3_FIELD0 : write something useful for field0
// ------------------------------------------------

#define GET_EXAMPLE_REG3_FIELD0(a)	((a >> EXAMPLE_REG3_FIELD0_SHIFT) & EXAMPLE_REG3_FIELD0_MASK)

// ------------------------------------------------
//  Macro functions for register reg4
//  - GET_EXAMPLE_REG4_REG4 :
// ------------------------------------------------

#define GET_EXAMPLE_REG4_REG4(a)	((a >> EXAMPLE_REG4_REG4_SHIFT) & EXAMPLE_REG4_REG4_MASK)

// ------------------------------------------------
//  Macro functions for register reg5
//  - GET_EXAMPLE_REG5_REG5 :
// ------------------------------------------------

#define GET_EXAMPLE_REG5_REG5(a)	((a >> EXAMPLE_REG5_REG5_SHIFT) & EXAMPLE_REG5_REG5_MASK)

// ------------------------------------------------
//  Macro functions for register reg6
//  - GET_EXAMPLE_REG6_REG6 :
// ------------------------------------------------

#define GET_EXAMPLE_REG6_REG6(a)	((a >> EXAMPLE_REG6_REG6_SHIFT) & EXAMPLE_REG6_REG6_MASK)

// ------------------------------------------------
//  Macro functions for register reg7
//  - GET_EXAMPLE_REG7_NIBBLE0 : write something useful for nibble0
//  - GET_EXAMPLE_REG7_UNUSED0 : unused
//  - GET_EXAMPLE_REG7_NIBBLE1 :
//  - GET_EXAMPLE_REG7_UNUSED1 : unused
//  - GET_EXAMPLE_REG7_NIBBLE2 : write something useful for nibble2
//  - GET_EXAMPLE_REG7_UNUSED2 : unused
// ------------------------------------------------

#define GET_EXAMPLE_REG7_NIBBLE0(a)	((a >> EXAMPLE_REG7_NIBBLE0_SHIFT) & EXAMPLE_REG7_NIBBLE0_MASK)
#define GET_EXAMPLE_REG7_UNUSED0(a)	((a >> EXAMPLE_REG7_UNUSED0_SHIFT) & EXAMPLE_REG7_UNUSED0_MASK)
#define GET_EXAMPLE_REG7_NIBBLE1(a)	((a >> EXAMPLE_REG7_NIBBLE1_SHIFT) & EXAMPLE_REG7_NIBBLE1_MASK)
#define GET_EXAMPLE_REG7_UNUSED1(a)	((a >> EXAMPLE_REG7_UNUSED1_SHIFT) & EXAMPLE_REG7_UNUSED1_MASK)
#define GET_EXAMPLE_REG7_NIBBLE2(a)	((a >> EXAMPLE_REG7_NIBBLE2_SHIFT) & EXAMPLE_REG7_NIBBLE2_MASK)
#define GET_EXAMPLE_REG7_UNUSED2(a)	((a >> EXAMPLE_REG7_UNUSED2_SHIFT) & EXAMPLE_REG7_UNUSED2_MASK)

// ------------------------------------------------
//  Macro functions for register reg8
//  - GET_EXAMPLE_REG8_NIBBLE0 :
//  - GET_EXAMPLE_REG8_UNUSED0 : unused
//  - GET_EXAMPLE_REG8_NIBBLE1 :
//  - GET_EXAMPLE_REG8_UNUSED1 : unused
// ------------------------------------------------

#define GET_EXAMPLE_REG8_NIBBLE0(a)	((a >> EXAMPLE_REG8_NIBBLE0_SHIFT) & EXAMPLE_REG8_NIBBLE0_MASK)
#define GET_EXAMPLE_REG8_UNUSED0(a)	((a >> EXAMPLE_REG8_UNUSED0_SHIFT) & EXAMPLE_REG8_UNUSED0_MASK)
#define GET_EXAMPLE_REG8_NIBBLE1(a)	((a >> EXAMPLE_REG8_NIBBLE1_SHIFT) & EXAMPLE_REG8_NIBBLE1_MASK)
#define GET_EXAMPLE_REG8_UNUSED1(a)	((a >> EXAMPLE_REG8_UNUSED1_SHIFT) & EXAMPLE_REG8_UNUSED1_MASK)

// End of example.h
