// SPDX-License-Identifier: MPL-2.0
//
// showbox product firmware: SKELETON ONLY.
//
// This file exists so the build system and per-SKU targets can be exercised.
// Product firmware starts after phase 1 answers the hardware questions and the
// owner signs off on the open questions (docs/phase1-bench-plan.md).
// Behaviour contract: docs/protocol.md. Structure: docs/architecture.md.

#include <Arduino.h>
#include <ETH.h>

#include "product.h"
#include "sku.h"

static void outputsSafeState() {
  // Boot step 1 (ADR-0009): every output inactive before anything else.
#if SKU_HAS_RINGER
  digitalWrite(SKU_PIN_RING_GATE, LOW);
  pinMode(SKU_PIN_RING_GATE, OUTPUT);
  digitalWrite(SKU_PIN_RING_FR, LOW);
  pinMode(SKU_PIN_RING_FR, OUTPUT);
#endif
  // Expander-driven SKUs: the MCP23017 resets with all pins as high-Z inputs,
  // so relays are already off. The expander driver will set the output latches
  // to inactive before switching pins to outputs.
}

void setup() {
  outputsSafeState();
  Serial.begin(115200);
  Serial.printf("%s %s sku=%s api=%s\n", PRODUCT_NAME, FIRMWARE_VERSION, SKU_NAME, API_VERSION);

  // Olimex ESP32-POE-ISO (WROOM): LAN8720 addr 0, MDC 23, MDIO 18, power 12, clock out on GPIO17.
  ETH.begin(ETH_PHY_LAN8720, 0, 23, 18, 12, ETH_CLOCK_GPIO17_OUT);
}

void loop() {
  delay(1000);
}
