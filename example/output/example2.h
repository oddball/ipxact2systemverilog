#pragma once
/* Automatically generated
 *  with the command 'ipxact2c --srcFile example/input/test2.xml --destDir example/output'
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
#define EXAMPLE2_REG0_OFFSET	0x00	// read something useful for reg0
#define EXAMPLE2_REG1_OFFSET	0x01	// 
#define EXAMPLE2_SAMENAME_OFFSET	0x1D	// samename register


// ------------------------------------------------
//  Bit operations for register reg0
// ------------------------------------------------
#define EXAMPLE2_REG0_FIELD0_SHIFT	0
#define EXAMPLE2_REG0_FIELD0_MASK 	0x03

#define EXAMPLE2_REG0_FIELD1_SHIFT	2
#define EXAMPLE2_REG0_FIELD1_MASK 	0x3F

// ------------------------------------------------
//  Bit operations for register reg1
// ------------------------------------------------
#define EXAMPLE2_REG1_FIELD0_SHIFT	0
#define EXAMPLE2_REG1_FIELD0_MASK 	0xFF
#define EXAMPLE2_REG1_FIELD0_MIN 	0x00
#define EXAMPLE2_REG1_FIELD0_MAX 	0x07

// ------------------------------------------------
//  Bit operations for register samename
// ------------------------------------------------
#define EXAMPLE2_SAMENAME_SAMENAME_SHIFT	0
#define EXAMPLE2_SAMENAME_SAMENAME_MASK 	0x03

#define EXAMPLE2_SAMENAME_UNUSED0_SHIFT	2
#define EXAMPLE2_SAMENAME_UNUSED0_MASK 	0x3F


// ------------------------------------------------
//  Macro functions for register reg0
//  - GET_EXAMPLE2_REG0_FIELD0 : read something useful for field0
//  - GET_EXAMPLE2_REG0_FIELD1 : read something useful for field1
// ------------------------------------------------

#define GET_EXAMPLE2_REG0_FIELD0(a)	((a >> EXAMPLE2_REG0_FIELD0_SHIFT) & EXAMPLE2_REG0_FIELD0_MASK)
#define GET_EXAMPLE2_REG0_FIELD1(a)	((a >> EXAMPLE2_REG0_FIELD1_SHIFT) & EXAMPLE2_REG0_FIELD1_MASK)

// ------------------------------------------------
//  Macro functions for register reg1
//  - GET_EXAMPLE2_REG1_FIELD0 : read something useful for field0
// ------------------------------------------------

#define GET_EXAMPLE2_REG1_FIELD0(a)	((a >> EXAMPLE2_REG1_FIELD0_SHIFT) & EXAMPLE2_REG1_FIELD0_MASK)

// ------------------------------------------------
//  Macro functions for register samename
//  - GET_EXAMPLE2_SAMENAME_SAMENAME :
//  - GET_EXAMPLE2_SAMENAME_UNUSED0 : unused
// ------------------------------------------------

#define GET_EXAMPLE2_SAMENAME_SAMENAME(a)	((a >> EXAMPLE2_SAMENAME_SAMENAME_SHIFT) & EXAMPLE2_SAMENAME_SAMENAME_MASK)
#define GET_EXAMPLE2_SAMENAME_UNUSED0(a)	((a >> EXAMPLE2_SAMENAME_UNUSED0_SHIFT) & EXAMPLE2_SAMENAME_UNUSED0_MASK)

// End of example2.h
