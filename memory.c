#include "common.h"

//
// ================= MEMORY DEFINITIONS =================
//

uint16_t instructionMemory[INSTRUCTION_MEMORY_SIZE];

int8_t dataMemory[DATA_MEMORY_SIZE];

int8_t registers[NUM_REGISTERS];

//
// ================= SPECIAL REGISTERS =================
//

uint16_t PC = 0;

SREG_t SREG = {0,0,0,0,0};

//
// ================= PIPELINE BUFFERS =================
//

IF_ID_Buffer IF_ID = {0};

ID_EX_Buffer ID_EX = {0};

//
// ================= PRINT FUNCTIONS =================
//

void printRegisters() {

    printf("\n========== REGISTERS ==========\n");

    for(int i = 0; i < 10; i++) {
        printf("R%d = %d\n", i, registers[i]);
    }

    printf("PC = %u\n", PC);
}

void printDataMemory() {

    printf("\n========== DATA MEMORY ==========\n");

    for(int i = 0; i < 20; i++) {

        printf("MEM[%d] = %d\n", i, dataMemory[i]);
    }
}

void printInstructionMemory() {

    printf("\n========== INSTRUCTION MEMORY ==========\n");

    for(int i = 0; i < 20; i++) {

        printf("INST[%d] = 0x%04X\n", i, instructionMemory[i]);
    }
}

void printRegisterChange(int reg, int8_t oldValue, int8_t newValue) {

    printf("Register R%d changed: %d -> %d\n",
           reg,
           oldValue,
           newValue);
}

void printMemoryChange(int address, int8_t oldValue, int8_t newValue) {

    printf("Memory[%d] changed: %d -> %d\n",
           address,
           oldValue,
           newValue);
}

void printSREG() {

    printf("\n========== SREG ==========\n");

    printf("C = %d\n", SREG.C);
    printf("V = %d\n", SREG.V);
    printf("N = %d\n", SREG.N);
    printf("S = %d\n", SREG.S);
    printf("Z = %d\n", SREG.Z);
}

void updateZeroFlag(int8_t result) {

    SREG.Z = (result == 0);
}

void updateNegativeFlag(int8_t result) {

    SREG.N = (result < 0);
}

int instructionCount = 0;
uint8_t flushPipeline = 0;

uint16_t branchTarget = 0;
extern uint8_t forwardingEnabled;

extern uint8_t forwardedRegister;

extern int8_t forwardedValue;
uint8_t forwardingEnabled = 0;

uint8_t forwardedRegister = 0;

int8_t forwardedValue = 0;