// SPDX-License-Identifier: MPL-2.0
// General Purpose box. Pin map DRAFT: see hardware/general-purpose/README.md.
#pragma once
#define SKU_NAME "gp"
#define SKU_RELAYS 4
#define SKU_OUTPUTS 2
#define SKU_INPUTS 2
#define SKU_HAS_RINGER 0
#define SKU_IO_EXPANDER_MCP23017 1
// Expander pin assignments (MCP23017: 0-7 = GPA0-7, 8-15 = GPB0-7)
#define SKU_RELAY_PINS {0, 1, 2, 3}
#define SKU_RELAY_ACTIVE_LOW 1
#define SKU_INPUT_PINS {8, 9}
#define SKU_OUTPUT_PINS {10, 11}
