#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 9
#define SS_PIN 10
#define LED_PIN 8
#define BUZZER_PIN 6

MFRC522 mfrc522(SS_PIN, RST_PIN);
unsigned long lastCardTime = 0;
const unsigned long cardInterval = 5000;  // 카드 인식 간격 (5초)
int cardList[10];  // 카드 UID를 저장하는 배열 (최대 10개 카드까지 저장 가능)
int cardCount = 0;  // 현재 저장된 카드 개수
bool isLedOn = false;  // LED 상태

void setup() {
  Serial.begin(9600);
  pinMode(LED_PIN, OUTPUT);  // LED_PIN을 출력으로 설정
  pinMode(BUZZER_PIN, OUTPUT); // BUZZER_PIN을 출력으로 설정
  SPI.begin();
  mfrc522.PCD_Init();
}

void loop() {
  // 일정 시간 이내에는 카드 인식 무시
  if (millis() - lastCardTime < cardInterval) {
    return;
  }

  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }

  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }
  playBuzzer(); // 부저 소리 재생

  int test_array[4];
  delay(500);
  for (byte i = 0; i < 4; i++) {
    test_array[i] = mfrc522.uid.uidByte[i];
    Serial.print(test_array[i]);
    Serial.print(" ");
  }
  Serial.println();

  lastCardTime = millis();  // 마지막으로 카드를 인식한 시간 갱신

  int uid = convertUidToInt(test_array);

  if (isCardInList(uid)) {
    removeCardFromList(uid);
    
  } else {
    addCardToList(uid);
  }

  updateLedState();
}

// 카드 UID를 정수 값으로 변환
int convertUidToInt(int uidArray[]) {
  int uid = 0;
  for (byte i = 0; i < 4; i++) {
    uid |= uidArray[i] << (8 * i);
  }
  return uid;
}

// 카드 UID가 리스트에 있는지 확인
bool isCardInList(int uid) {
  for (int i = 0; i < cardCount; i++) {
    if (cardList[i] == uid) {
      return true;
    }
  }
  return false;
}

// 카드 UID를 리스트에 추가
void addCardToList(int uid) {
  if (cardCount < 10) {
    cardList[cardCount] = uid;
    cardCount++;
  }
}

// 카드 UID를 리스트에서 제거
void removeCardFromList(int uid) {
  for (int i = 0; i < cardCount; i++) {
    if (cardList[i] == uid) {
      // 배열에서 제거하기 위해 뒤의 요소들을 앞으로 이동
      for (int j = i; j < cardCount - 1; j++) {
        cardList[j] = cardList[j + 1];
      }
      cardCount--;
      break;
    }
  }
}

// LED 상태 업데이트
void updateLedState() {
  if (cardCount == 0) {
    digitalWrite(LED_PIN, LOW);  // LED 끄기
    isLedOn = false;
  } else if (!isLedOn) {
    digitalWrite(LED_PIN, HIGH); // LED 켜기
    isLedOn = true;
  }
}

// 부저 소리 재생
void playBuzzer() {
  tone(BUZZER_PIN, 1000, 200);  // 1kHz 주파수로 200ms 동안 소리 발생
  delay(200);  // 소리 재생 후 200ms 대기
  noTone(BUZZER_PIN);  // 부저 소리 중지
}

