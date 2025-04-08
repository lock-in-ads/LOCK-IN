#include <SPI.h>
#include <MFRC522.h>
#include <Servo.h>

#define SS_PIN 10
#define RST_PIN 9
#define SERVO_PIN 5

MFRC522 mfrc522(SS_PIN, RST_PIN);
Servo servo;

byte authorizedUID[] = {0x76, 0xF7, 0xF9, 0x20}; // Your RFID card's UID

int angle = 0; // Initial servo angle

void setup() {
  Serial.begin(9600);
  SPI.begin(); // Initialize SPI bus
  mfrc522.PCD_Init(); // Initialize MFRC522
  pinMode(SERVO_PIN, OUTPUT); // Set servo pin as output
  delay(100); // Wait for a moment before attaching servo
  servo.attach(SERVO_PIN); // Attach servo to pin
  servo.write(angle); // Set initial servo position
  delay(100); // Allow servo to stabilize
  Serial.println("Tap RFID/NFC Tag on reader");
}

void loop() {
  // Check if a new card is present
  if (mfrc522.PICC_IsNewCardPresent()) {
    
    if (mfrc522.PICC_ReadCardSerial()) {
      MFRC522::PICC_Type piccType = mfrc522.PICC_GetType(mfrc522.uid.sak);
      
      // Compare the UID of the card to the authorized UID
      if (mfrc522.uid.uidByte[0] == authorizedUID[0] &&
          mfrc522.uid.uidByte[1] == authorizedUID[1] &&
          mfrc522.uid.uidByte[2] == authorizedUID[2] &&
          mfrc522.uid.uidByte[3] == authorizedUID[3]) {
        
        Serial.println("Authorized Tag");
        
        // Change servo angle
        if (angle == 0) {
          angle = 50;
        } else {
          angle = 0;
        }
        
        // Control servo motor according to the angle
        servo.write(angle);
        Serial.print("Rotate Servo Motor to ");
        Serial.print(angle);
        Serial.println("°");
        
      } else {
        Serial.print("Unauthorized Tag with UID:");
        for (int i = 0; i < mfrc522.uid.size; i++) {
          Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
          Serial.print(mfrc522.uid.uidByte[i], HEX);
        }
        Serial.println();
        
        // Reset servo to initial position if unauthorized card is detected
        angle = 0;
        servo.write(angle);
        Serial.println("Resetting servo to initial position");
      }
      
      mfrc522.PICC_HaltA(); // Halt PICC
      mfrc522.PCD_StopCrypto1(); // Stop encryption on PCD
    }
  }
  
  // Optional: Add a delay to prevent continuous servo movement
  delay(50); // Adjust this delay as needed
}
