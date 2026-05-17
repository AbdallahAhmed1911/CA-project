//gcc main.c memory.c parser.c pipeline.c -o processor.exe
//processor.exe
//python simulator_gui.py
#include "common.h"
#include "parser.h"
#include "pipeline.h"
int main() {

    // Reset everything FIRST
    for (int i = 0; i < NUM_REGISTERS; i++)
        registers[i] = 0;

    for (int i = 0; i < DATA_MEMORY_SIZE; i++)
        dataMemory[i] = 0;

    for (int i = 0; i < INSTRUCTION_MEMORY_SIZE; i++)
        instructionMemory[i] = 0;

    PC = 0;
    instructionCount = 0;

    SREG.C = SREG.V = SREG.N = SREG.S = SREG.Z = 0;

    IF_ID.valid = 0;
    ID_EX.valid = 0;

    flushPipeline     = 0;
    forwardingEnabled = 0;

    // THEN load (this sets instructionCount)
    loadProgram("test1.txt");
    printf("Loaded %d instructions\n", instructionCount);  // Should print 5
    int cycle = 1;

    while(
        PC < instructionCount ||
        IF_ID.valid           ||
        ID_EX.valid
    ) {
        printf("\n\n");
        printf("=====================================\n");
        printf("CLOCK CYCLE %d\n", cycle);
        printf("=====================================\n");

        execute();
        decode();

        if(PC < instructionCount) {
            fetch();
        }

        cycle++;
    }

    printf("\n\n========== FINAL STATE ==========\n");
    printRegisters();
    printSREG();
    printDataMemory();

    return 0;
}