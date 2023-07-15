#include <FastLED.h>     //转向灯
#include <Servo.h>       //转向
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

unsigned long LastMessageTime = 0;    // 上次接收到消息的时间
unsigned long TimeoutInterval = 5000; // 没有接收到消息的超时时间，单位为毫秒

// 接收串口的数据，并做出响应
void GetInfoFromComputer()
{
  if (Serial.available())
  {
    if (Serial.peek() == ReceiveStart)
    {
      Serial.read();                                       // 丢弃起始校验符
      String message = Serial.readStringUntil(ReceiveEnd); // 读取到结束校验符为止的字符串
      int messageSize = Serial.parseInt();                 // 读取信息的大小
      int len = message.length();
      if (message.length() == messageSize)
      {
        Serial.print("Received message: ");
        Serial.println(message);
        LastMessageTime = millis();
        StaticJsonDocument<200> jsonDocument;
        DeserializationError error = deserializeJson(jsonDocument, message);
        if (!error)
        {
          //int Variable = jsonDocument["Key"];
          int status = jsonDocument["Status"];
          if (status == 1)
          {
            //Code
          }
          else if (status == 0)
          {
            //Code
          }

          String operation = jsonDocument["Operation"].as<String>();
          if (operation == "Start")
          {
            //Code
          }
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
  Serial.begin(115200);
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

  SendInfoToComputer("SpeedLeft", speedLeft, "SpeedRight", speedRight, "Power", power, "Accelerator", accelerator);
  //GetInfoFromComputer();
  //Timeout();
  delay(50);
}
