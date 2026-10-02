// SPDX-License-Identifier: MPL-2.0
// Ringer box. Pin map DRAFT: see hardware/ringer/README.md.
// Ring module (Ag1171 vs Black Magic) is decided in phase 1.
#pragma once
#define SKU_NAME "ringer"
#define SKU_RELAYS 0
#define SKU_OUTPUTS 0
#define SKU_INPUTS 0
#define SKU_HAS_RINGER 1
#define SKU_IO_EXPANDER_MCP23017 0
#define SKU_PIN_RING_GATE 4      // Ag1171 RM, or Black Magic gate relay
#define SKU_PIN_RING_FR 32       // Ag1171 F/R; unused for Black Magic [verify pin is broken out]
#define SKU_PIN_LID_BUTTON 36    // input-only, external pull-up
