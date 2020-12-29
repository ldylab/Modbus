#include "Arduino.h"
#include "Modbus.h"
#include "ModbusSerial.h"

const int LED_COIL = 13;
const int LEDPin = 13;
const int PressTimesAddress = 100;
int PressTimes = 0;
int ButtonStateLast;
int ButtonStateInit = 1;
ModbusSerial mb;

void setup() {
  // put your setup code here, to run once:
  //Config Modbus Serial(port,speed,byte format)
  mb.config(&Serial, 9600, SERIAL_8N1);
  //slave ID 1-247
  mb.setSlaveId(1); //setting its ID is 1
  mb.addCoil(LED_COIL, false);
  mb.addIreg(PressTimesAddress);
  pinMode(LEDPin, OUTPUT);
  pinMode(12, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  mb.task();

  int SignalRead = mb.Coil(LED_COIL);
  if (ButtonStateInit == 1)
  {
    ButtonStateLast = SignalRead;
    ButtonStateInit = 0;
  }

  if (SignalRead == 1)
  {
    digitalWrite(LEDPin, 0);
    digitalWrite(12, 1);
  }
  else if (SignalRead == 0)
  {
    digitalWrite(LEDPin, 1);
    digitalWrite(12, 0);
  }

  if (SignalRead != ButtonStateLast)
  {
    if(SignalRead == 1)
    {
      PressTimes++;
    }
    ButtonStateLast = !ButtonStateLast;
  }

  mb.Ireg(PressTimesAddress, PressTimes);
}
