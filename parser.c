#include "parser.h"


// convert mnemonic to opcode
int getOpcode(char* mnemonic) {

    if(strcmp(mnemonic, "ADD") == 0) return ADD;
    if(strcmp(mnemonic, "SUB") == 0) return SUB;
    if(strcmp(mnemonic, "MUL") == 0) return MUL;
    if(strcmp(mnemonic, "MOVI") == 0) return MOVI;
    if(strcmp(mnemonic, "BEQZ") == 0) return BEQZ;
    if(strcmp(mnemonic, "ANDI") == 0) return ANDI;
    if(strcmp(mnemonic, "EOR") == 0) return EOR;
    if(strcmp(mnemonic, "BR") == 0) return BR;
    if(strcmp(mnemonic, "SLC") == 0) return SLC;
    if(strcmp(mnemonic, "SRC") == 0) return SRC;
    if(strcmp(mnemonic, "LDR") == 0) return LDR;
    if(strcmp(mnemonic, "STR") == 0) return STR;

    return -1;
}

// extract register number from string like "R1"
int parseRegister(char* reg) {

    return atoi(reg + 1);
}

void loadProgram(const char* filename) {

    FILE* file = fopen(filename, "r");

    if(file == NULL) {
        printf("Error opening file.\n");
        return;
    }

    char line[100];

    int instructionIndex = 0;
   while(fgets(line, sizeof(line), file)) {

    // Skip empty lines
    if(line[0] == '\n' || line[0] == '\0')
        continue;

    char mnemonic[10] = {0};
    char op1[10] = {0};
    char op2[10] = {0};

    int tokens = sscanf(line, "%9s %9s %9s",
                        mnemonic,
                        op1,
                        op2);

    // Ignore invalid lines
    if(tokens < 1)
        continue;

    int opcode = getOpcode(mnemonic);

    if(opcode == -1) {
        printf("Invalid opcode: %s\n", mnemonic);
        continue;
    }

    uint16_t instruction = 0;

    // R-FORMAT
    if(opcode == ADD ||
       opcode == SUB ||
       opcode == MUL ||
       opcode == EOR ||
       opcode == BR) {

        int r1 = parseRegister(op1);
        int r2 = parseRegister(op2);

        instruction |= (opcode << 12);
        instruction |= (r1 << 6);
        instruction |= r2;
    }

    // I-FORMAT
    else {

        int r1 = parseRegister(op1);
        int immediate = atoi(op2);

        instruction |= (opcode << 12);
        instruction |= (r1 << 6);
        instruction |= (immediate & 0x3F);
    }

    instructionMemory[instructionIndex] = instruction;

    printf("Loaded Instruction %d = 0x%04X\n",
           instructionIndex,
           instruction);

    instructionIndex++;
    instructionCount++;
}

    fclose(file);
}