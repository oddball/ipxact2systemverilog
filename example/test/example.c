#include <stdint.h>
#include <stdio.h>

#include "../output/example.h"

#define BYTE_COUNT      4
#define NIBBLE_COUNT    3
#define DATA_REG        0x12345678

int main(int argc, char** argv)
{
    printf("Testing generated example header file\n");

    uint8_t data_byte[BYTE_COUNT];
    uint8_t data_nibble[NIBBLE_COUNT];

    data_byte[0] = (uint8_t)GET_EXAMPLE_REG0_BYTE0(DATA_REG);
    data_byte[1] = (uint8_t)GET_EXAMPLE_REG0_BYTE1(DATA_REG);
    data_byte[2] = (uint8_t)GET_EXAMPLE_REG0_BYTE2(DATA_REG);
    data_byte[3] = (uint8_t)GET_EXAMPLE_REG0_BYTE3(DATA_REG);

    for (int i=0; i<BYTE_COUNT; ++i)
    {
        printf("REG0 - Byte %d = %02x\n", i, data_byte[i]);
    }
    
    printf("REG2 - Power   = 0x%x\n", GET_EXAMPLE_REG2_POWER(  0b00000001));
    printf("REG2 - Power2  = 0x%x\n", GET_EXAMPLE_REG2_POWER2( 0b00000010));
    printf("REG2 - Monkey  = 0x%x\n", GET_EXAMPLE_REG2_MONKEY( 0b00001100));
    printf("REG2 - Monkey2 = 0x%x\n", GET_EXAMPLE_REG2_MONKEY2(0b00110000));

    data_nibble[0] = (uint8_t)GET_EXAMPLE_REG7_NIBBLE0(DATA_REG);
    data_nibble[1] = (uint8_t)GET_EXAMPLE_REG7_NIBBLE1(DATA_REG);
    data_nibble[2] = (uint8_t)GET_EXAMPLE_REG7_NIBBLE2(DATA_REG);

    for (int i=0; i<NIBBLE_COUNT; ++i)
    {
        printf("REG7 - Nibble %d = %02x\n", i, data_nibble[i]);
    }
    return 0;
}