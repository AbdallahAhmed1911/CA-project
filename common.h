#ifndef COMMON_H
#define COMMON_H

#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>

//
// ================= MEMORY SIZES =================
//

#define INSTRUCTION_MEMORY_SIZE 1024
#define DATA_MEMORY_SIZE 2048
#define NUM_REGISTERS 64

//
// ================= OPCODES =================
//

#define ADD   0
#define SUB   1
#define MUL   2
#define MOVI  3
#define BEQZ  4
#define ANDI  5
#define EOR   6
#define BR    7
#define SLC   8
#define SRC   9
#define LDR   10
#define STR   11

//
// ================= PROCESSOR MEMORY =================
//

// Instruction Memory
// 1024 words, each word = 16 bits
extern uint16_t instructionMemory[INSTRUCTION_MEMORY_SIZE];

// Data Memory
// 2048 bytes
extern int8_t dataMemory[DATA_MEMORY_SIZE];

// Register File
// 64 registers, each = 8 bits
extern int8_t registers[NUM_REGISTERS];

//
// ================= SPECIAL REGISTERS =================
//

// Program Counter
extern uint16_t PC;

// Status Register
typedef struct {
    uint8_t C; // Carry
    uint8_t V; // Overflow
    uint8_t N; // Negative
    uint8_t S; // Sign
    uint8_t Z; // Zero
} SREG_t;

extern SREG_t SREG;

//
// ================= PIPELINE BUFFERS =================
//

// IF -> ID Buffer
typedef struct {
    uint16_t instruction;
    uint16_t pc;

    uint8_t valid;
} IF_ID_Buffer;

extern IF_ID_Buffer IF_ID;

//
// ID -> EX Buffer
//

typedef struct {

    uint16_t rawInstruction;

    uint8_t opcode;

    uint8_t r1;
    uint8_t r2;

    int8_t immediate;

    int8_t r1Value;
    int8_t r2Value;

    uint16_t pc;

    uint8_t valid;

} ID_EX_Buffer;

extern ID_EX_Buffer ID_EX;

//
// ================= FUNCTION DECLARATIONS =================
//

void printRegisters();
void printDataMemory();
void printInstructionMemory();

void printRegisterChange(int reg, int8_t oldValue, int8_t newValue);
void printMemoryChange(int address, int8_t oldValue, int8_t newValue);

void printSREG();
void updateZeroFlag(int8_t result);
void updateNegativeFlag(int8_t result);
extern int instructionCount;
extern uint8_t flushPipeline;
extern uint16_t branchTarget;

extern uint8_t forwardingEnabled;

extern uint8_t forwardedRegister;

extern int8_t forwardedValue;
#endif