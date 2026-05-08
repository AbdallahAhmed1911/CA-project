#include "pipeline.h"

//
// ================= FETCH STAGE =================
//

void fetch() {

    //
    // Read instruction from instruction memory
    ////
// Flush if branch taken
//

if(flushPipeline) {

    IF_ID.valid = 0;

    flushPipeline = 0;

    printf("\nPipeline Flushed.\n");
}

    uint16_t instruction = instructionMemory[PC];

    //
    // Fill IF -> ID buffer
    //

    IF_ID.instruction = instruction;

    IF_ID.pc = PC;

    IF_ID.valid = 1;

    //
    // Print fetch information
    //

    printf("\n========== FETCH STAGE ==========\n");

    printf("Fetched Instruction = 0x%04X\n", instruction);

    printf("Fetched From Address = %u\n", PC);

    //
    // Increment PC
    //

    PC++;
}

//
// ================= DECODE STAGE =================
//

void decode() {

    //
    // Check if buffer contains valid instruction
    //

    if(IF_ID.valid == 0) {

        printf("\nDecode Stage Empty.\n");

        return;
    }

    //
    // Get instruction
    //

    uint16_t instruction = IF_ID.instruction;

    //
    // Extract fields
    //

    uint8_t opcode = (instruction >> 12) & 0xF;

    uint8_t r1 = (instruction >> 6) & 0x3F;

    uint8_t r2 = instruction & 0x3F;

    //
    // Immediate is lower 6 bits
    //

    int8_t immediate = instruction & 0x3F;

    //
    // Sign extension for negative immediates
    //

    if(immediate & 0x20) {

        immediate |= 0xC0;
    }

    //
    // Read register values
    //

    int8_t r1Value = registers[r1];

    int8_t r2Value = registers[r2];
    //
// ================= FORWARDING =================
//

if(forwardingEnabled) {

    //
    // Forward to R1
    //

    if(r1 == forwardedRegister) {

        r1Value = forwardedValue;

        printf("\nFORWARDED VALUE TO R1\n");
    }

    //
    // Forward to R2
    //

    if(r2 == forwardedRegister) {

        r2Value = forwardedValue;

        printf("\nFORWARDED VALUE TO R2\n");
    }
}

    //
    // Fill ID -> EX buffer
    //

    ID_EX.rawInstruction = instruction;

    ID_EX.opcode = opcode;

    ID_EX.r1 = r1;

    ID_EX.r2 = r2;

    ID_EX.immediate = immediate;

    ID_EX.r1Value = r1Value;

    ID_EX.r2Value = r2Value;

    ID_EX.pc = IF_ID.pc;

    ID_EX.valid = 1;

    //
    // Print decode information
    //

    printf("\n========== DECODE STAGE ==========\n");

    printf("Instruction = 0x%04X\n", instruction);

    printf("Opcode = %u\n", opcode);

    printf("R1 = %u\n", r1);

    printf("R2 = %u\n", r2);

    printf("Immediate = %d\n", immediate);

    printf("R1 Value = %d\n", r1Value);

    printf("R2 Value = %d\n", r2Value);

    //
    // Clear IF_ID buffer after decode
    //
forwardingEnabled = 0;
    IF_ID.valid = 0;
}

//
// ================= EXECUTE STAGE =================
//

void execute() {

    //
    // Check valid instruction
    //

    if(ID_EX.valid == 0) {

        printf("\nExecute Stage Empty.\n");

        return;
    }

    //
    // Extract fields
    //

    uint8_t opcode = ID_EX.opcode;

    uint8_t r1 = ID_EX.r1;

    uint8_t r2 = ID_EX.r2;

    int8_t imm = ID_EX.immediate;

    int8_t val1 = ID_EX.r1Value;

    int8_t val2 = ID_EX.r2Value;

    int8_t result = 0;

    //
    // Print stage
    //

    printf("\n========== EXECUTE STAGE ==========\n");
    

    //
    // ================= ADD =================
    //

    if(opcode == ADD) {

        result = val1 + val2;

        registers[r1] = result;

        updateZeroFlag(result);

        updateNegativeFlag(result);

        printf("ADD R%d R%d\n", r1, r2);

        printf("Result = %d\n", result);
    }

    //
    // ================= SUB =================
    //

    else if(opcode == SUB) {

        result = val1 - val2;

        registers[r1] = result;

        updateZeroFlag(result);

        updateNegativeFlag(result);

        printf("SUB R%d R%d\n", r1, r2);

        printf("Result = %d\n", result);
    }

    //
    // ================= MUL =================
    //

    else if(opcode == MUL) {

        result = val1 * val2;

        registers[r1] = result;

        updateZeroFlag(result);

        updateNegativeFlag(result);

        printf("MUL R%d R%d\n", r1, r2);

        printf("Result = %d\n", result);
    }

    //
    // ================= MOVI =================
    //

    else if(opcode == MOVI) {

        result = imm;

        registers[r1] = result;

        updateZeroFlag(result);

        updateNegativeFlag(result);

        printf("MOVI R%d %d\n", r1, imm);

        printf("Result = %d\n", result);
    }

    //
    // ================= ANDI =================
    //

    else if(opcode == ANDI) {

        result = val1 & imm;

        registers[r1] = result;

        updateZeroFlag(result);

        updateNegativeFlag(result);

        printf("ANDI R%d %d\n", r1, imm);

        printf("Result = %d\n", result);
    }

    //
    // ================= EOR =================
    //

    else if(opcode == EOR) {

        result = val1 ^ val2;

        registers[r1] = result;

        updateZeroFlag(result);

        updateNegativeFlag(result);

        printf("EOR R%d R%d\n", r1, r2);

        printf("Result = %d\n", result);
    }

    //
// ================= BEQZ =================
//

else if(opcode == BEQZ) {

    printf("BEQZ R%d %d\n", r1, imm);

    //
    // Branch if register equals zero
    //

    if(val1 == 0) {

        //
        // Calculate branch target
        //

        branchTarget = ID_EX.pc + 1 + imm;

        //
        // Redirect PC
        //

        PC = branchTarget;

        //
        // Flush pipeline
        //

        flushPipeline = 1;

        //
        // Clear wrong instructions
        //

        IF_ID.valid = 0;

        printf("BRANCH TAKEN\n");

        printf("New PC = %u\n", PC);
    }

    else {

        printf("BRANCH NOT TAKEN\n");
    }
}
//
// ================= BR =================
//

    else if(opcode == BR) {

        printf("BR R%d R%d\n", r1, r2);

        //
        // Concatenate registers
        //

        uint16_t high = ((uint8_t)val1) << 8;

        uint16_t low = (uint8_t)val2;

        branchTarget = high | low;

        //
        // Redirect PC
        //

        PC = branchTarget;

        //
        // Flush pipeline
        //

        flushPipeline = 1;

        //
        // Clear wrong instructions
        //

        IF_ID.valid = 0;

        printf("JUMP TAKEN\n");

        printf("New PC = %u\n", PC);
    }

    //
    // ================= LDR =================
    //

    else if(opcode == LDR) {

        printf("LDR R%d %d\n", r1, imm);

        uint16_t address = (uint16_t)imm;

        if(address >= DATA_MEMORY_SIZE) {
            printf("ERROR: Address %u out of bounds\n", address);
            result = 0;
        } else {
            result = dataMemory[address];
            printf("Loaded value %d from address %u\n", result, address);
        }

        registers[r1] = result;

        updateZeroFlag(result);
        updateNegativeFlag(result);
    }

    //
    // ================= STR =================
    //

    else if(opcode == STR) {

        printf("STR R%d %d\n", r1, imm);

        uint16_t address = (uint16_t)imm;

        if(address >= DATA_MEMORY_SIZE) {
            printf("ERROR: Address %u out of bounds\n", address);
        } else {
            int8_t oldValue = dataMemory[address];
            dataMemory[address] = registers[r1];
            printf("Stored value %d to address %u\n", registers[r1], address);
            printMemoryChange(address, oldValue, dataMemory[address]);
        }
    }

    //
    // Print updated register
    //

    printf("Updated R%d = %d\n", r1, registers[r1]);

    //
    // Print flags
    //

    printSREG();

    //
    // Clear buffer
    //
//
// Enable forwarding
//

forwardingEnabled = 1;

forwardedRegister = r1;

forwardedValue = registers[r1];
    ID_EX.valid = 0;
}