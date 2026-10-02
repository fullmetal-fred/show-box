// SPDX-License-Identifier: MPL-2.0
// Selects the per-SKU hardware description. Exactly one SHOWBOX_SKU_* is
// defined by the PlatformIO env (see platformio.ini).
#pragma once

#if defined(SHOWBOX_SKU_GP)
#include "gp.h"
#elif defined(SHOWBOX_SKU_RELAY8)
#include "relay8.h"
#elif defined(SHOWBOX_SKU_INPUT)
#include "input.h"
#elif defined(SHOWBOX_SKU_RINGER)
#include "ringer.h"
#else
#error "No SKU selected: build with -e gp|relay8|input|ringer"
#endif

// Every SKU header must define:
//   SKU_NAME          string, as reported in /status "sku"
//   SKU_RELAYS        number of /relay channels (0 if none)
//   SKU_OUTPUTS       number of /out channels
//   SKU_INPUTS        number of /in channels
//   SKU_HAS_RINGER    0 or 1
// plus pin maps. All pin maps are DRAFT until the phase 1 boot-glitch test.
