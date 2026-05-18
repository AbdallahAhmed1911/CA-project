#include "pipeline.h"

uint8_t killDecode = 0;
uint8_t killEX = 0;


// ================= FETCH STAGE =================
void fetch()
{
    if (PC >= instructionCount)
        return;

    // FLUSH ONLY HERe
    if (flushPipeline)
    {
        IF_ID.valid = 0;
        flushPipeline = 0;
        printf("\nPipeline Flushed.\n");
        return;
    }

    uint16_t instruction = instructionMemory[PC];

    IF_ID.instruction = instruction;
    IF_ID.pc = PC;
    IF_ID.valid = 1;

    printf("\n========== FETCH STAGE ==========\n");
    printf("Fetched Instruction = 0x%04X\n", instruction);
    printf("Fetched From Address = %u\n", PC);

    PC++;
}

// ================= DECODE STAGE =================
void decode()
{
    // HARD STOP on flush 
    if (flushPipeline || killDecode)
    {
        IF_ID.valid = 0;
        killDecode = 0;
        return;
    }

    if (IF_ID.valid == 0)
    {
        printf("\nDecode Stage Empty.\n");
        return;
    }

    uint16_t instruction = IF_ID.instruction;

    uint8_t opcode    = (instruction >> 12) & 0xF;
    uint8_t r1        = (instruction >> 6) & 0x3F;
    uint8_t r2        = instruction & 0x3F;
    int8_t  immediate  = instruction & 0x3F;

    if (immediate & 0x20)
        immediate |= 0xC0;

    int8_t r1Value = registers[r1];
    int8_t r2Value = registers[r2];

    if (forwardingEnabled)
    {
        if (r1 == forwardedRegister)
            r1Value = forwardedValue;

        if (r2 == forwardedRegister)
            r2Value = forwardedValue;
    }

    // BUILD PIPELINE REGISTER ONLY IF NOT FLUSHED
    ID_EX.rawInstruction = instruction;
    ID_EX.opcode         = opcode;
    ID_EX.r1             = r1;
    ID_EX.r2             = r2;
    ID_EX.immediate      = immediate;
    ID_EX.r1Value        = r1Value;
    ID_EX.r2Value        = r2Value;
    ID_EX.pc             = IF_ID.pc;
    ID_EX.valid          = 1;

    printf("\n========== DECODE STAGE ==========\n");
    printf("Instruction = 0x%04X\n", instruction);
    printf("Opcode = %u\n", opcode);
    printf("R1 = %u\n", r1);
    printf("R2 = %u\n", r2);
    printf("Immediate = %d\n", immediate);
    printf("R1 Value = %d\n", r1Value);
    printf("R2 Value = %d\n", r2Value);

    forwardingEnabled = 0;
    IF_ID.valid = 0;
}

// ================= EXECUTE STAGE =================
void execute()
{
    // HARD KILL FIRST (VERY IMPORTANT)
    if (flushPipeline || killEX)
    {
        ID_EX.valid = 0;
        killEX = 0;
        return;
    }

    if (ID_EX.valid == 0)
    {
        printf("\nExecute Stage Empty.\n");
        return;
    }

    uint8_t opcode = ID_EX.opcode;
    uint8_t r1     = ID_EX.r1;
    uint8_t r2     = ID_EX.r2;
    int8_t imm     = ID_EX.immediate;
    int8_t val1    = ID_EX.r1Value;
    int8_t val2    = ID_EX.r2Value;
    int8_t result  = 0;

    printf("\n========== EXECUTE STAGE ==========\n");

    // ================= ADD =================
    // Flags updated: C, V, N, S, Z
    if (opcode == ADD)
    {
        result        = val1 + val2;
        registers[r1] = result;

        updateZeroFlag(result);
        updateNegativeFlag(result);

        
        updateCarryFlag(val1, val2);
        updateOverflowFlagADD(val1, val2, result);

        // FIX: S = N XOR V  (was never computed before)
        updateSignFlag();

        printf("ADD R%d R%d\n", r1, r2);
        printf("Result = %d\n", result);
    }

    // ================= SUB =================
    // Flags updated: V, N, S, Z
    else if (opcode == SUB)
    {
        result        = val1 - val2;
        registers[r1] = result;

        updateZeroFlag(result);
        updateNegativeFlag(result);

        updateOverflowFlagSUB(val1, val2, result);

        // FIX: S = N XOR V
        updateSignFlag();

        printf("SUB R%d R%d\n", r1, r2);
        printf("Result = %d\n", result);
    }

    // ================= MUL =================
    // Flags updated: N, S, Z
    else if (opcode == MUL)
    {
        result        = val1 * val2;
        registers[r1] = result;

        updateZeroFlag(result);
        updateNegativeFlag(result);
        updateSignFlag();   // FIX: S = N XOR V

        printf("MUL R%d R%d\n", r1, r2);
        printf("Result = %d\n", result);
    }

    // ================= MOVI =================
    // Flags updated: N, S, Z
    else if (opcode == MOVI)
    {
        result        = imm;
        registers[r1] = result;

        updateZeroFlag(result);
        updateNegativeFlag(result);
        updateSignFlag();   // FIX: S = N XOR V

        printf("MOVI R%d %d\n", r1, imm);
        printf("Result = %d\n", result);
    }

    // ================= ANDI =================
    // Flags updated: N, S, Z
    else if (opcode == ANDI)
    {
        result        = val1 & imm;
        registers[r1] = result;

        updateZeroFlag(result);
        updateNegativeFlag(result);
        updateSignFlag();   // FIX: S = N XOR V

        printf("ANDI R%d %d\n", r1, imm);
        printf("Result = %d\n", result);
    }

    // ================= EOR =================
    // Flags updated: N, S, Z
    else if (opcode == EOR)
    {
        result        = val1 ^ val2;
        registers[r1] = result;

        updateZeroFlag(result);
        updateNegativeFlag(result);
        updateSignFlag();   // FIX: S = N XOR V

        printf("EOR R%d R%d\n", r1, r2);
        printf("Result = %d\n", result);
    }

    // ================= SLC =================
    // Flags updated: N, S, Z
    else if (opcode == SLC)
    {
        int     safe_shamt = imm % 8;
        uint8_t u_val1     = (uint8_t)val1;

        if (safe_shamt == 0)
        {
            result = val1;
        }
        else
        {
            result = (int8_t)((u_val1 << safe_shamt) | (u_val1 >> (8 - safe_shamt)));
        }

        registers[r1] = result;

        updateZeroFlag(result);
        updateNegativeFlag(result);
        updateSignFlag();   // FIX: S = N XOR V

        printf("SLC R%d %d\n", r1, imm);
        printf("Result = %d\n", result);
    }

    // ================= SRC =================
    // Flags updated: N, S, Z
    else if (opcode == SRC)
    {
        int     safe_shamt = imm % 8;
        uint8_t u_val1     = (uint8_t)val1;

        if (safe_shamt == 0)
        {
            result = val1;
        }
        else
        {
            result = (int8_t)((u_val1 >> safe_shamt) | (u_val1 << (8 - safe_shamt)));
        }

        registers[r1] = result;

        updateZeroFlag(result);
        updateNegativeFlag(result);
        updateSignFlag();   // FIX: S = N XOR V

        printf("SRC R%d %d\n", r1, imm);
        printf("Result = %d\n", result);
    }

    // ================= BEQZ =================
    // No flag updates
    if (opcode == BEQZ)
    {
        printf("BEQZ R%d %d\n", r1, imm);

        if (val1 == 0)
        {
            PC = ID_EX.pc + 1 + imm;
            flushPipeline = 1;
            killDecode = 1;
            killEX = 1;

            printf("BRANCH TAKEN\n");
            printf("New PC = %u\n", PC);

            return;
        }
        else
        {
            printf("BRANCH NOT TAKEN\n");
        }
    }

    // ================= BR =================
    // No flag updates
    else if (opcode == BR)
    {
        printf("BR R%d R%d\n", r1, r2);

        uint16_t high    = ((uint8_t)val1) << 8;
        uint16_t low     = (uint8_t)val2;
        branchTarget     = high | low;
        PC               = branchTarget;
        flushPipeline    = 1;
        IF_ID.valid      = 0;
        ID_EX.valid      = 0;

        printf("JUMP TAKEN\n");
        printf("New PC = %u\n", PC);
    }

    // ================= LDR =================
    // Flags updated: N, S, Z
    else if (opcode == LDR)
    {
        printf("LDR R%d %d\n", r1, imm);

        uint16_t address = (uint16_t)(uint8_t)imm;

        if (address >= DATA_MEMORY_SIZE)
        {
            printf("ERROR: Address %u out of bounds\n", address);
            result = 0;
        }
        else
        {
            result = dataMemory[address];
            printf("Loaded value %d from address %u\n", result, address);
        }

        registers[r1] = result;

        updateZeroFlag(result);
        updateNegativeFlag(result);
        updateSignFlag();
    }

    // ================= STR =================
    // No flag updates
    else if (opcode == STR)
    {
        printf("STR R%d %d\n", r1, imm);

        uint16_t address = (uint16_t)(uint8_t)imm;

        if (address >= DATA_MEMORY_SIZE)
        {
            printf("ERROR: Address %u out of bounds\n", address);
        }
        else
        {
            int8_t oldValue       = dataMemory[address];
            dataMemory[address]   = registers[r1];
            printf("Stored value %d to address %u\n", registers[r1], address);
            printMemoryChange(address, oldValue, dataMemory[address]);
        }
    }

    // Print updated register and flags
    printf("Updated R%d = %d\n", r1, registers[r1]);

    printSREG();
// Enable forwarding only for instructions
// that write to registers

if(

    opcode == ADD  ||
    opcode == SUB  ||
    opcode == MUL  ||
    opcode == MOVI ||
    opcode == ANDI ||
    opcode == EOR  ||
    opcode == SLC  ||
    opcode == SRC  ||
    opcode == LDR

) {

    forwardingEnabled = 1;

    forwardedRegister = r1;

    forwardedValue = registers[r1];
}
    ID_EX.valid = 0;
}
