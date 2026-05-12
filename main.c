#include "common.h"
#include "parser.h"
#include "pipeline.h"

int main() {

    //
    // Load assembly program
    //

    loadProgram("program.txt");

    //
    // Example initial values
    //

    registers[1] = 10;
    registers[2] = 20;

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