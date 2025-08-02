#include <stdio.h>
#include <string.h>

#define MAX_COMMAND_LEN 32

void init_system() {
    printf("[System] Initialization complete.\n");
}

void receive_command(char *command) {
    if (strcmp(command, "DEPLOY_ANTENNA") == 0) {
        printf("[Satellite] Deploying antenna...\n");
    } else if (strcmp(command, "ACTIVATE_THRUSTER") == 0) {
        printf("[Satellite] Activating thruster...\n");
    } else {
        printf("[Error] Unknown command received: %s\n", command);
    }
}

int main() {
    char command[MAX_COMMAND_LEN];

    init_system();

    while (1) {
        printf("\nAwaiting command: ");
        if (fgets(command, MAX_COMMAND_LEN, stdin) != NULL) {
            // Remove trailing newline character
            command[strcspn(command, "\n")] = '\0';

            receive_command(command);
        }
    }

    return 0;
}
