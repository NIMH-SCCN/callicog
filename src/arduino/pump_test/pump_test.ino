//#include <Arduino.h>
//#include "A4988.h"

#define DIR 9
#define STEP 8
#define ENA 2

#define MS1 4
#define MS2 5
#define MS3 6

#include <SPI.h>

int pot_CS = 10;
int spi_address = 0;
int pot_max_step = 127;
int tone_pin = 3;
int max_volume = 100;

int correct_frequency = 800;
int incorrect_frequency = 100;
int correct_volume = 90;
int incorrect_volume = 100;

int duration_ms = 1000;
float dosage_amount = 100.0;

int incomingByte;

void setup() {
  //Serial setup
  Serial.begin(9600);
  //SPI setup
  pinMode(pot_CS, OUTPUT);
  SPI.begin();
  //Motor setup
  pinMode(DIR, OUTPUT);
  pinMode(STEP, OUTPUT);
  pinMode(ENA, OUTPUT);
  pinMode(MS1, OUTPUT);
  pinMode(MS2, OUTPUT);
  pinMode(MS3, OUTPUT);
  digitalWrite(DIR, HIGH);
  digitalWrite(ENA, HIGH);
  //digitalWrite(STEP, LOW);

  // Configure Big Easy Driver in FULL STEP mode
  // See mode table here: https://learn.sparkfun.com/tutorials/big-easy-driver-hookup-guide
  digitalWrite(MS1, LOW);
  digitalWrite(MS2, LOW);
  digitalWrite(MS3, LOW);
}

void loop() {
  // Loop for bench testing:
  correct(correct_frequency, correct_volume, duration_ms, dosage_amount);
  delay(5000);
  incorrect(incorrect_frequency, incorrect_volume, duration_ms);
  delay(5000);
}

void correct(int frequency, int volume, int duration_ms, float dosage_amount) {
  playTone(frequency, volume, duration_ms);
  digitalWrite(ENA, LOW);
  pump(dosage_amount);
  digitalWrite(ENA, HIGH);
}

void incorrect(int frequency, int volume, int duration_ms) {
  playTone(frequency, volume, duration_ms);
}

void digitalPotWrite(int address, int value) {
  digitalWrite(pot_CS, LOW);
  SPI.transfer(address);
  SPI.transfer(value);
  digitalWrite(pot_CS, HIGH);
}

void playTone(int frequency, int volume, int duration_ms) {
  //set volume
  int value = abs(volume - max_volume) * pot_max_step / 100;
  digitalPotWrite(spi_address, value);
  delay(20);
  //play tone
  tone(tone_pin, frequency, duration_ms);
}

void pump(float dosage_amount) {
  int steps = (0.9712 * dosage_amount) - 0.4845;
  for (int i = 0; i < steps; i++) {
    digitalWrite(STEP, HIGH);
    delay(10);
    digitalWrite(STEP, LOW);
    delay(10);
  }
}
