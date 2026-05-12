//gcc main.c memory.c parser.c pipeline.c -o processor.exe
#include "common.h"
#include "parser.h"
#include "pipeline.h"

int main() {

    //
    // Load assembly program
    //

    loadProgram("test2.txt");

    for (int i = 0; i < NUM_REGISTERS; i++)
        registers[i] = 0;

    for (int i = 0; i < DATA_MEMORY_SIZE; i++)
        dataMemory[i] = 0;

    PC = 0;
    instructionCount = 0;

    //
    // Clock cycle counter
    //

    int cycle = 1;

    //
    // Continue while:
    // - instructions remain to fetch
    // - OR pipeline still contains instructions
    //

    while(

        PC < instructionCount ||

        IF_ID.valid ||

        ID_EX.valid
    ) {

        printf("\n\n");
        printf("=====================================\n");
        printf("CLOCK CYCLE %d\n", cycle);
        if(!IF_ID.valid && !ID_EX.valid && PC < instructionCount) {

            printf("Pipeline Bubble Present\n");
        }
        printf("=====================================\n");

        //
        // IMPORTANT:
        // Execute first
        // Then Decode
        // Then Fetch
        //
        execute();

        decode();

        //
        // Fetch only if instructions remain
        //

        if(PC < instructionCount) {

            fetch();
        }

        cycle++;
    }

    //
    // Final processor state
    //

    printf("\n\n========== FINAL STATE ==========\n");

    printRegisters();

    printSREG();

    printDataMemory();

    return 0;
}