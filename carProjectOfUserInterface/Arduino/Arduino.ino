#include <FastLED.h>//转向灯
#include <Servo.h>//转向
#include <ArduinoJson.h> // 引入 ArduinoJson 库

#define EmergencyStop 0     // 电平位于高位时生效，用以紧急停止
#define SpeedDetectLeft A4  // 用以检测左电机回传的速度
#define SpeedDetectRight A5 // 用以检测右电机回传的速度
#define LEDDataLeft 13      // 用以向左侧LED发送信息
#define LEDDataRight 12     // 用以向右侧LED发送信息

const char SendStart = '\x01';    // 发送的起始校验符
const char SendEnd = '\x02';      // 发送的结尾校验符
const char ReceiveStart = '\x03'; // 接收的起始校验符
const char ReceiveEnd = '\x04';   // 接收结尾校验符

unsigned long LastMessageTime = 0; // 上次接收到消息的时间
unsigned long TimeoutInterval = 5000; // 没有接收到消息的超时时间，单位为毫秒

//接收串口的数据，并做出响应
void GetInfoFromComputer()
{
  if (Serial.available())
  {
    if (Serial.peek() == ReceiveStart)
    {
      Serial.read();                                       // 丢弃起始校验符
      String message = Serial.readStringUntil(ReceiveEnd); // 读取到结束校验符为止的字符串
      int messageSize = Serial.parseInt();                 // 读取信息的大小
      int len=message.length();
      if (message.length() == messageSize)
      {
        Serial.print("Received message: ");
        Serial.println(message);
        LastMessageTime = millis();
        StaticJsonDocument<200> jsonDocument;
        DeserializationError error = deserializeJson(jsonDocument, message);
        if (!error)
        {
          // 检查键 "Status" 的值
          int status = jsonDocument["Status"];
          if (status == 1)
          {
            Serial.print("status1");
          }
          else if (status == 0)
          {
            Serial.print("status0");
          }

          // 检查键 "Operation" 的值
          String operation = jsonDocument["Operation"].as<String>();
          if (operation == "Start")
          {
            Serial.print("OpeStart");
          }
        }
      }
    }
  }
}

//将收集的数据向串口发出
void SendInfoToComputer(int speedLeft, int speedRight, int power, int accelerator)
{
  char format[100];
  char output[100];
  int messageSize = snprintf(format, sizeof(format), "{'SpeedLeft':%d,'SpeedRight':%d,'Power':%d,'Accelerator':%d}", speedLeft, speedRight, power, accelerator);
  // int messageSize = sizeof(output);
  sprintf(output, "%c%s%c%c", SendStart, format, (char)messageSize, SendEnd);
  Serial.print(output);
}

void Timeout()
{
  if (millis() - LastMessageTime > TimeoutInterval)
  {
    Serial.print("Timeout");
  }
}

void setup()
{
  Serial.begin(9600);
}

void loop()
{
  int SpeedLeft = analogRead(SpeedDetectLeft);
  int SpeedRight = analogRead(SpeedDetectRight);
  int AverageSpeed = (SpeedDetectLeft + SpeedRight);
  String testString = "hello";
  int speedLeft = random(10); //模拟从硬件上收到的变量
  int speedRight = random(10);
  int power = random(10);
  int accelerator = random(10000);

  //SendInfoToComputer(speedLeft, speedRight, power, accelerator);
  GetInfoFromComputer();
  Timeout();

}
