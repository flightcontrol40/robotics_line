# E_STOP              =-1
# WAITING_FOR_HANDOFF = 0  # Waiting for R2 to begin handoff
# MOVING_TO_HANDOFF   = 1
# IN_HANDOFF          = 2 # Dice Gripped, Waiting for R2 to let go
# MOVE_TO_CONV1       = 3
# SEND_TO_R4          = 5 # Sending Dice to R4
# WAIT_FOR_CONV1      = 6 # Waiting For Dice to arrive at R4
# WAITING_FOR_R4_CONV = 7 # Waiting for R4 to send Dice Back
# MOVE_TO_QA          = 8 
# QA                  = 9 # QA Dice
# QA_PASS             = 10 
# QA_FAIL             = 11
# RANDOM_PLACE        = 12 # Placing In a Random Position for R4
uint8 process_state  # State Indicator

uint8 error_code     # Error Code
bool error_status    # 1 Error, 0 Ok

bool die_qa          # R BIT bool 1 QA Pass, 0 QA Fail
bool r2_handoff      # 1 Ready to Handoff, 0 Not Ready