#include <Adafruit_CircuitPlayground.h>

// #include "Adafruit_Circuit_Playground/utility/IRLibSAMD21.h"

const int PROXIMITY = A10;
int proximity = 0;
int tick_count = 0;
enum State {INACTIVE, READY, LOCKED, FLAT, INVERTED, TILTED_LEFT, TILTED_RIGHT, TILTED_FORWARD,
            TILTED_BACKWARD,  INVERTED_TILTED_LEFT, INVERTED_TILTED_RIGHT, INVERTED_TILTED_FORWARD,
            INVERTED_TILTED_BACKWARD};
const uint16_t PROXIMITY_THRESHOLD = 600;
State state = INACTIVE;

void setup() {
  CircuitPlayground.begin(); 
  Serial.begin(9600);
  pinMode(13, OUTPUT);
  digitalWrite(13, LOW);
  pinMode(25, OUTPUT);
  digitalWrite(25, LOW);
  setupTC1();
  CircuitPlayground.clearPixels();
}

void loop() {
  float a_x = (CircuitPlayground.motionX() - 0.268867) / 9.44291;
  float a_y = (CircuitPlayground.motionY() + 0.194099) / 9.76308;
  float a_z = (CircuitPlayground.motionZ() - 0.105363) / 9.7;
  /*
  Serial.print(a_x); Serial.print("G, ");
  Serial.print(a_y); Serial.print("G, ");
  Serial.print(a_z); Serial.println("G");
  */
  
  switch (state) {
  case INACTIVE:
    CircuitPlayground.clearPixels();
    if (proximity > PROXIMITY_THRESHOLD) {
      state = READY;
    } else {
      state = INACTIVE;
    }
    break;
  case READY:
    setPixelsColor(0, 9, 255, 255, 255);
    if (proximity < PROXIMITY_THRESHOLD) {
      state = INACTIVE;
    } else if (abs(a_x) <= 0.2 && a_y >= 0.75 && a_z <= 0.65) {
      state = LOCKED;
    }
    break;
  case LOCKED:
    setPixelsColor(0, 9, 0, 255, 0);
    if (proximity < PROXIMITY_THRESHOLD && abs(a_x) < 0.5 && abs(a_y) < 0.5 && a_z >= 0.8) {
      state = FLAT;
    }
    break;
  case FLAT:
    setPixelsColor(0, 9, 0, 0, 255);
    if (proximity > PROXIMITY_THRESHOLD) {
      state = READY;
    } else if (abs(a_x) < 0.5 && abs(a_y) < 0.5 && a_z <= -0.8) {
      state = INVERTED;
    } else if (a_x <= -0.8 && abs(a_y) <= 0.4 && abs(a_z) <= 0.4) {
      state = TILTED_LEFT;
    } else if (a_x >= 0.8 && abs(a_y) <= 0.4 && abs(a_z) <= 0.4) {
      state = TILTED_RIGHT;
    } else if (abs(a_x) <= 0.2 && a_y >= 0.75 && a_z <= 0.65) {
      state = TILTED_FORWARD;
    } else if (abs(a_x) <= 0.2 && a_y <= -0.75 && a_z <= 0.65) {
      state = TILTED_BACKWARD;
    }
    break;
  case INVERTED:
    setPixelsColor(0, 9, 255, 0, 0);
    if (abs(a_x) < 0.5 && abs(a_y) < 0.5 && a_z >= 0.8) {
      state = FLAT;
    } else if (a_x >= 0.8 && abs(a_y) <= 0.4 && abs(a_z) <= 0.4) {
      state = INVERTED_TILTED_LEFT;
    } else if (a_x <= -0.8 && abs(a_y) <= 0.4 && abs(a_z) <= 0.4) {
      state = INVERTED_TILTED_RIGHT;
    } else if (abs(a_x) <= 0.2 && a_y >= 0.75 && a_z >= -0.65) {
      state = INVERTED_TILTED_FORWARD;
    } else if (abs(a_x) <= 0.2 && a_y <= -0.75 && a_z >= -0.65) {
      state = INVERTED_TILTED_BACKWARD;
    }
    break;
  case TILTED_LEFT:
    setPixelsColor(0, 5, 0, 0, 255);
    setPixelsColor(6, 8, 255, 0, 0);
    CircuitPlayground.setPixelColor(9, 0, 0, 255);
    if (abs(a_x) < 0.5 && abs(a_y) < 0.5 && a_z >= 0.8) {
      state = FLAT;
    } else if (abs(a_x) < 0.5 && abs(a_y) < 0.5 && a_z <= -0.8) {
      state = INVERTED;
    }
    break;
  case TILTED_RIGHT:
    CircuitPlayground.setPixelColor(0, 0, 0, 255);
    setPixelsColor(1, 3, 255, 0, 0);
    setPixelsColor(4, 9, 0, 0, 255);
    if (abs(a_x) < 0.5 && abs(a_y) < 0.5 && a_z >= 0.8) {
      state = FLAT;
    } else if (abs(a_x) < 0.5 && abs(a_y) < 0.5 && a_z <= -0.8) {
      state = INVERTED;
    }
    break;
  case TILTED_FORWARD:
    setPixelsColor(0, 2, 0, 0, 255);
    setPixelsColor(3, 6, 255, 0, 0);
    setPixelsColor(7, 9, 0, 0, 255);
    if (abs(a_x) < 0.5 && abs(a_y) < 0.5 && a_z >= 0.8) {
      state = FLAT;
    } else if (abs(a_x) < 0.5 && abs(a_y) < 0.5 && a_z <= -0.8) {
      state = INVERTED;
    }
    break;
  case TILTED_BACKWARD:
    setPixelsColor(0, 1, 255, 0, 0);
    setPixelsColor(2, 7, 0, 0, 255);
    setPixelsColor(8, 9, 255, 0, 0);
    if (abs(a_x) < 0.5 && abs(a_y) < 0.5 && a_z >= 0.8) {
      state = FLAT;
    } else if (abs(a_x) < 0.5 && abs(a_y) < 0.5 && a_z <= -0.8) {
      state = INVERTED;
    }
    break;
  case INVERTED_TILTED_LEFT:
    setPixelsColor(0, 5, 255, 0, 0);
    setPixelsColor(6, 8, 0, 0, 255);
    CircuitPlayground.setPixelColor(9, 255, 0, 0);
    if (abs(a_x) < 0.5 && abs(a_y) < 0.5 && a_z >= 0.8) {
      state = FLAT;
    } else if (abs(a_x) < 0.5 && abs(a_y) < 0.5 && a_z <= -0.8) {
      state = INVERTED;
    }
    break;
  case INVERTED_TILTED_RIGHT:
    CircuitPlayground.setPixelColor(0, 255, 0, 0);
    setPixelsColor(1, 3, 0, 0, 255);
    setPixelsColor(4, 9, 255, 0, 0);
    if (abs(a_x) < 0.5 && abs(a_y) < 0.5 && a_z >= 0.8) {
      state = FLAT;
    } else if (abs(a_x) < 0.5 && abs(a_y) < 0.5 && a_z <= -0.8) {
      state = INVERTED;
    }
    break;
  case INVERTED_TILTED_FORWARD:
    setPixelsColor(0, 1, 0, 0, 255);
    setPixelsColor(2, 7, 255, 0, 0);
    setPixelsColor(8, 9, 0, 0, 255);
    if (abs(a_x) < 0.5 && abs(a_y) < 0.5 && a_z >= 0.8) {
      state = FLAT;
    } else if (abs(a_x) < 0.5 && abs(a_y) < 0.5 && a_z <= -0.8) {
      state = INVERTED;
    }
    break;
  case INVERTED_TILTED_BACKWARD:
    setPixelsColor(0, 2, 255, 0, 0);
    setPixelsColor(3, 6, 0, 0, 255);
    setPixelsColor(7, 9, 255, 0, 0);
    if (abs(a_x) < 0.5 && abs(a_y) < 0.5 && a_z >= 0.8) {
      state = FLAT;
    } else if (abs(a_x) < 0.5 && abs(a_y) < 0.5 && a_z <= -0.8) {
      state = INVERTED;
    }
    break;
  }
  delay(100);
}

void setPixelsColor(uint8_t startIndex, uint8_t stopIndex, uint8_t r, uint8_t g, uint8_t b) {
  for (uint8_t index = startIndex; index <= stopIndex; ++index) {
    CircuitPlayground.setPixelColor(index, r, g, b);
  }
}

void TCC1_Handler() {
  Tcc* TC = (Tcc*) TCC1;
  if (TC->INTFLAG.bit.OVF == 1) {
    digitalWrite(25, tick_count % 32 == 0);
    if (tick_count > 32) {
      proximity = analogRead(PROXIMITY);
      // Serial.println(proximity);
      tick_count = 0;
    }
    TC->INTFLAG.bit.OVF = 1;
    ++tick_count;
  }

  if (TC->INTFLAG.bit.MC0 == 1) {
    TC->INTFLAG.bit.MC0 = 1;
  }
}

void setupTC1() {
  // Enable clock for TC
  REG_GCLK_CLKCTRL = (uint16_t) (GCLK_CLKCTRL_CLKEN | GCLK_CLKCTRL_GEN_GCLK0 | GCLK_CLKCTRL_ID_TCC0_TCC1) ;
  while (GCLK->STATUS.bit.SYNCBUSY == 1); // wait for sync

  // The type cast must fit with the selected timer mode
  Tcc* TC = (Tcc*) TCC1;

  TC->CTRLA.reg &= ~TC_CTRLA_ENABLE;   // Disable TC
  while (TC->SYNCBUSY.bit.ENABLE == 1); // wait for sync

  TC->CTRLA.reg |= TC_CTRLA_WAVEGEN_NFRQ; // Set TC as normal Normal Frq
  while (TC->SYNCBUSY.bit.ENABLE == 1); // wait for sync

  TC->CTRLA.reg |= TC_CTRLA_PRESCALER_DIV256;   // Set perscaler

  TC->PER.reg = 0xFF;   // Set counter Top using the PER register but the 16/32 bit timer counts allway to max 
  while (TC->SYNCBUSY.bit.WAVE == 1); // wait for sync

  TC->CC[0].reg = 0xFFF;
  while (TC->SYNCBUSY.bit.CC0 == 1); // wait for sync
 
  // Interrupts
  TC->INTENSET.reg = 0;              // disable all interrupts
  TC->INTENSET.bit.OVF = 1;          // enable overfollow
  TC->INTENSET.bit.MC0 = 1;          // enable compare match to CC0

  // Enable InterruptVector
  NVIC_EnableIRQ(TCC1_IRQn);

  // Enable TC
  TC->CTRLA.reg |= TCC_CTRLA_ENABLE;
  while (TC->SYNCBUSY.bit.ENABLE == 1); // wait for sync
}
