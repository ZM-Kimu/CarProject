#include <FastLED.h>     //转向灯
#include <Servo.h>       //转向
#include <ArduinoJson.h> // 引入 ArduinoJson 库

#define EmergencyStop 0     // 电平位于高位时生效，用以紧急停止
#define SpeedDetectLeft A4  // 用以检测左电机回传的速度
#define SpeedDetectRight A5 // 用以检测右电机回传的速度
#define LeftPIN 13          // 左LED数据接口
#define RightPIN 12         // 右LED数据接口

#define NUM_LEDS 62 // LED数量
#define bandRate 115200 // Arduino通信带宽

int OperationTick = 0;
int isLeftLight = 0;
int isRightLight = 0;
bool EmergencyLightUp = false;
bool EmergencyOn = false;

String DebugStr;
String CommandCode="-1";

const char SendStart = '\x01';    // 发送的起始校验符
const char SendEnd = '\x02';      // 发送的结尾校验符
const char ReceiveStart = '\x03'; // 接收的起始校验符
const char ReceiveEnd = '\x04';   // 接收结尾校验符

unsigned long LastMessageTime = 0;    // 上次接收到消息的时间
unsigned long TimeoutInterval = 5000; // 没有接收到消息的超时时间，单位为毫秒

unsigned long LastLight = 0;       //
unsigned long LightInterval = 500; //

unsigned long LastEmer = 0;       //
unsigned long EmerInterval = 220; //

CRGB LeftLED[NUM_LEDS];
CRGB RightLED[NUM_LEDS];

// 控制转向灯，0为左，1为右
void TurningLight()
{
  for (int Bright = 0; Bright <= 255; Bright += 5)
  {
    FastLED.setBrightness(255 - Bright);
    FastLED.show();
  }
  fill_solid(LeftLED, NUM_LEDS, CRGB::Black);
  fill_solid(RightLED, NUM_LEDS, CRGB::Black);
  FastLED.setBrightness(255);
  FastLED.show();
  // 从中心向两端发光
  for (int i = 0; i <= NUM_LEDS / 2; i++)
  {
    CRGB color = CRGB(255, 100, 0);
    // 左LED
    if (isLeftLight == 1)
    {
      LeftLED[NUM_LEDS / 2 - i] = color;
      LeftLED[NUM_LEDS / 2 + i] = color;
    }
    // 右LED
    else if (isRightLight == 1)
    {
      RightLED[NUM_LEDS / 2 - i] = color;
      RightLED[NUM_LEDS / 2 + i] = color;
    }
    FastLED.show();
    delay(5);
  }
  if (isLeftLight || isRightLight)
  {
    OperationTick += 1;
  }
  if (OperationTick > 3)
  {
    isLeftLight = 0;
    isRightLight = 0;
    OperationTick = 0;
    CommandCode = -1;
  }
}
//将灯带改为应急灯状态
void EmergencyLight()
{
  if (EmergencyOn && CommandCode == "01")
  {
    if (!EmergencyLightUp)
    {
      fill_solid(LeftLED, NUM_LEDS, CRGB::Red);
      fill_solid(RightLED, NUM_LEDS, CRGB::Red);
      FastLED.setBrightness(0);
      FastLED.show();
    }

    for (int i = 0; i <= 255; i += 10)
    {
      if (!EmergencyLightUp)
      {
        FastLED.setBrightness(i);
      }
      else if (EmergencyLightUp)
      {
        FastLED.setBrightness(255 - i);
      }
      FastLED.show();
    }
    if (!EmergencyLightUp)
    {
      EmergencyLightUp = true;
    }
    else if (EmergencyLightUp)
    {
      EmergencyLightUp = false;
    }
    DebugStr=EmergencyLightUp;
  }
  else if (EmergencyOn == false && CommandCode == "-1")
  {
    fill_solid(LeftLED, NUM_LEDS, CRGB::Black);
    fill_solid(RightLED, NUM_LEDS, CRGB::Black);
    FastLED.setBrightness(255);
    FastLED.show();
  }
}

// 接收串口的数据，并做出响应
void GetInfoFromComputer()
{
  if (Serial.peek() == ReceiveStart)
  {
    Serial.read();                                       // 丢弃起始校验符
    String message = Serial.readStringUntil(ReceiveEnd); // 读取到结束校验符为止的字符串
    int messageSize = Serial.parseInt();                 // 读取信息的大小
    int len = message.length();
    Serial.print(message);
    if (message.length() == messageSize)
    {
      LastMessageTime = millis();
      StaticJsonDocument<200> jsonDocument;
      DeserializationError error = deserializeJson(jsonDocument, message);
      if (!error)
      {
        // Usage: int Variable = jsonDocument["Key"];
        int StatusInfo = jsonDocument["Status"];
        switch (StatusInfo)
        {
        case 2:
          break;
        case 0:
        break;
        }
        String OperationInfo = jsonDocument["Turnning"].as<String>();
        if (OperationInfo == "Left" && OperationTick < 2)
        {
          isLeftLight = 1;
          CommandCode = "10";
        }
        else if (OperationInfo == "Right" && OperationTick < 2)
        {
          isRightLight = 1;
          CommandCode = "11";
        }
        String EmergencyInfo = jsonDocument["Emergency"].as<String>();
        if (EmergencyInfo == "On")
        {
          EmergencyOn = true;
          CommandCode = "01";
        }
        else if (EmergencyInfo == "Off")
        {
          EmergencyOn = false;
          CommandCode = "-1";
        }

        String InitInfo = jsonDocument["InitAll"].as<String>();
        if (InitInfo == "True")
        {
          EmergencyOn = false;
          CommandCode = "-1";
        }
      }
    }
  }
}

//----------------------函数SendInfoToComputer用于键值对处理及发送信息
// 递归函数处理参数包
template <typename T, typename U, typename... Args>
void AddKeyValuePair(JsonObject &obj, const T &key, const U &value, const Args &...args)
{
  obj[key] = value;
  AddKeyValuePair(obj, args...); // 递归处理剩余的键值对
}

// 递归函数的结束条件
template <typename T, typename U>
void AddKeyValuePair(JsonObject &obj, const T &key, const U &value)
{
  obj[key] = value;
}

template <typename... Args>
void SendInfoToComputer(const Args &...args)
{
  const size_t capacity = 200;
  StaticJsonDocument<capacity> jsonDocument;
  char output[capacity];

  // 构建 JSON 对象
  JsonObject root = jsonDocument.to<JsonObject>();
  AddKeyValuePair(root, args...); // 逐个添加键值对
  // 序列化 JSON 对象为字符串
  size_t messageSize = serializeJson(root, output, sizeof(output));

  // 发送数据到串口
  Serial.print(SendStart);
  Serial.print(output);
  Serial.print((char)messageSize);
  Serial.print(SendEnd);
}
//----------------------

// 在时间内未收到来自主机的回应
void Timeout()
{
  if (millis() - LastMessageTime > TimeoutInterval)
  {
  }
}

void setup()
{
  Serial.begin(bandRate);
  FastLED.addLeds<NEOPIXEL, LeftPIN>(LeftLED, NUM_LEDS);
  FastLED.addLeds<NEOPIXEL, RightPIN>(RightLED, NUM_LEDS);
  int a, b;
  for (a = 0; a < NUM_LEDS; a += 3)
  {
    for (b = 0; b < NUM_LEDS - a; b += 3)
    {
      CRGB randomColor = CRGB(random(180, 255), random(180, 255), random(180, 255));
      LeftLED[b] = randomColor;
      RightLED[b] = randomColor;
      FastLED.show();
      LeftLED[b] = CRGB::Black;
      RightLED[b] = CRGB::Black;
      FastLED.show();
    }
    fill_solid(LeftLED + 61 - a, a + 3, CRGB(0, 248, 255));
    fill_solid(RightLED + 61 - a, a + 3, CRGB(0, 248, 255));
    FastLED.show();
  }
  fill_solid(LeftLED, NUM_LEDS, CRGB::Black);
  fill_solid(RightLED, NUM_LEDS, CRGB::Black);
  FastLED.show();
}

void loop()
{
  int SpeedLeft = analogRead(SpeedDetectLeft);
  int SpeedRight = analogRead(SpeedDetectRight);
  int AverageSpeed = (SpeedDetectLeft + SpeedRight);
  String testString = "hello";
  int speedLeft = random(10); // 模拟从硬件上收到的变量
  int speedRight = random(10);
  int power = random(10);
  int accelerator = random(10000);

  SendInfoToComputer("SLeft", speedLeft, "SRight", speedRight, "Pow", power, "Accel", accelerator, "Status", 1, "CmdCode", CommandCode, "debug", DebugStr);
  delay(20);
  GetInfoFromComputer();
  if (millis() - LastLight > LightInterval)
  {
    TurningLight();
    LastLight = millis();
  }
  if (millis() - LastEmer > EmerInterval && EmergencyOn)
  {
    EmergencyLight();
    LastEmer = millis();
  }
}
