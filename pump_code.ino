//#include <Arduino.h>
//#include "A4988.h"

#define DIR 9
#define STEP 8

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
float dosage_amount = 50.0;

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
  digitalWrite(DIR, HIGH);
  //digitalWrite(STEP, LOW);
}

void loop() {
  if (Serial.available() > 0) {
    incomingByte = Serial.read();
    if (incomingByte == 'C') {
      correct(correct_frequency, correct_volume, duration_ms, dosage_amount);
    }
    else if (incomingByte == 'I') {
      incorrect(incorrect_frequency, incorrect_volume, duration_ms);
    }
  } 
}

void correct(int frequency, int volume, int duration_ms, float dosage_amount) {
  playTone(frequency, volume, duration_ms);
  pump(dosage_amount);
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
