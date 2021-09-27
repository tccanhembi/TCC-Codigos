/////Declaração das Bibliotecas e Variáveis///////

#define SIM800L_RX     27
#define SIM800L_TX     26
#define SIM800L_PWRKEY 4
#define SIM800L_RST    5
#define SIM800L_POWER  23
#include <OneWire.h>
#include <DallasTemperature.h>

//fator de conversão de microsegundos para segundos
#define uS_TO_S_FACTOR 1000000

//tempo que o ESP32 ficará em modo sleep (em segundos)
#define TIME_TO_SLEEP_01 120
#define TIME_TO_SLEEP 120
#include <Pangodream_18650_CL.h>
Pangodream_18650_CL BL;
#define VOLTAGE_PIN 15
#define PIN_PORTA 35
#define PIN_BUZZER 4
RTC_DATA_ATTR static int boot_count = 0;
#include <Wire.h>
#include "RTClib.h"
#include <SD.h>
#include "FS.h"
#include "SD.h"
#include <SPI.h>
SPIClass SPISD(HSPI);

#define SD_CS_PIN 32
#define SD_SCK 14
#define SD_MISO 25
#define SD_MOSI 13

File myFile;
File arquivosend;
File testando;
 
RTC_DS3231 rtc;



#define DS18B20     0 // OK 
String MEUID = "Victor"; //existente na lista

// Sensor de Temperatura DS18B20
//Instacia o Objeto oneWire e Seta o pino do Sensor para iniciar as leituras
OneWire oneWire(DS18B20);
//Repassa as referencias do oneWire para o Sensor Dallas (DS18B20)
DallasTemperature Sensor(&oneWire);

String apn = "timbrasil.br";                    //APN
String apn_u = "tim";                     //APN-Username
String apn_p = "tim";                     //APN-Password
String url = "http://meuitach.dyndns.org:8090";  //URL of Server
String url2 = "http://meuitach.dyndns.org:8091";

void setup()
{

///// Início do Programa /////

////Declara os valores de data e hora e faz o setup da hora no momento de upload do programa////

pinMode(PIN_BUZZER,OUTPUT);
#ifndef ESP8266
  while (!Serial); // for Leonardo/Micro/Zero
#endif
 
  Serial.begin(115200);
 
  delay(3000); // wait for console opening
 
  if (! rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);
  }
 
  if (rtc.lostPower()) {
    Serial.println("RTC lost power, lets set the time!");
    // following line sets the RTC to the date &amp; time this sketch was compiled
    rtc.adjust(DateTime(F(__DATE__), F(__TIME__)));
    // This line sets the RTC with an explicit date &amp; time, for example to set
    // January 21, 2014 at 3am you would call:
    // rtc.adjust(DateTime(2014, 1, 21, 3, 0, 0));
  }

//// Inicia sensores, declara GPIOs de entrada ou saída ////
 
Sensor.begin();
Sensor.requestTemperatures();
pinMode(VOLTAGE_PIN,INPUT);
pinMode(PIN_PORTA,INPUT_PULLUP);

Serial.println("ESP32+SIM800L AT CMD Test");

Serial.println ("");
Serial.print ("Status Porta:");
Serial.println (digitalRead(PIN_PORTA));
Serial.println ("");
float volts = 0.0;
volts = analogRead(15)*(5.0/1023.0);
Serial.print ("Bateria:");
Serial.println (volts);
Serial.println ("");
Serial.print ("Temperatura:");
Serial.println (Sensor.getTempCByIndex(0));
Serial.println ("");

//// Incrementa ao valor boot_count +1 ////
++boot_count;
Serial.printf("Numero de boots: %d\n", boot_count);
int Resto;
int Resto2;

//// Resto 2 é usado para saber exatamente quando o programa faz 5 gravações ////
Resto2 = boot_count % 6;
Resto = boot_count % 5;
Serial.println("");
Serial.println("Resto = ");
Serial.println(Resto);
Serial.println("");
Serial.println("Resto2 = ");
Serial.println(Resto2);


if (Resto2 == 0 || boot_count == 1){ ////Quando o programa gravou as 5 vezes ou iniciou pela primeira vez, ele entrará neste "if"////
  /// "if" responsável por iniciar o SD Card, apagar o arquivo "send.text"
  /// Criar um novo arquivo "send.text"
  /// Isso assegura que cada arquivo "send.text" terá 5 valores gravados.
  
  Serial.println("");
  Serial.println("Entrando no loop de Resto2");

   SPISD.begin(SD_SCK, SD_MISO, SD_MOSI);
    if (!SD.begin(SD_CS_PIN,SPISD)) {  //SD_CS_PIN this pin is just the dummy pin since the SD need the input 
    Serial.println(F("failed!"));
    return;
    }
    else Serial.println(F("SD read!"));
    delay(2000);
    
    SD.remove("/send.txt"); // remove is a function in SD library to delete a file
    delay(1000);
    Serial.println("Arquivo Removido");
    testando = SD.open("/send.txt", FILE_WRITE);
    testando.close();
    Serial.println("Arquivo Criado");
    

}

/// Com os dados de data e hora que já foram gravados, vamos tratar esses dados e dividí-los em ano, mês, dia, hora, minuto, segundo. ////

DateTime now = rtc.now();
    Serial.println("");
    Serial.print("Data e Hora agora: ");
    String ano = "";
    ano = now.year();
    String mes = "";
    mes = now.month();
    String dia = "";
    dia = now.day();

    

    String hora = "";
    hora = now.hour();
    String minuto = "";
    minuto = now.minute();
    String segundo = "";
    segundo = now.second();

if (mes.length() < 2) { /// "if" para garantir sempre 2 digitos no mês
      mes = "0"+mes;
    }
    

    if (dia.length() < 2) { ///"if" para garantir sempre 2 digitos no dia
      dia = "0"+dia;
    }


    if (hora.length() < 2) { ///"if" para garantir sempre 2 digitos na hora
      hora = "0"+hora;
    }

    if (minuto.length() < 2) { ///"if" para garantir sempre 2 digitos no minuto
      minuto = "0"+minuto;
    }

    if (segundo.length() < 2) { ///"if" para garantir sempre 2 digitos no minuto
      segundo = "0"+segundo;
    }
    String datahora = "";
    datahora = ano+mes+dia+hora+minuto+segundo;
    Serial.println(datahora);

String sep1 = ",";
String sep2 = ",";

//Temperatura
int temperaturainteiro = Sensor.getTempCByIndex(0);
String valortemperatura = "";
valortemperatura = temperaturainteiro;

if (valortemperatura == "-127") { ///"if" para evitar o erro dando o valor de "99".
  valortemperatura = "99";
}


//Porta
String valorporta = "";
valorporta = digitalRead(PIN_PORTA);

/// String todasinfos é utilizada para gravar o dado no SD Card, no arquivo text.txt
String todasinfos = MEUID+sep2+ano+sep2+mes+sep2+dia+sep2+hora+sep2+minuto+sep2+segundo+sep2+valortemperatura+sep2+valorporta+sep2+volts;
/// String todasinfossend é utilizada para enviar ao Python.
String todasinfossend = MEUID+sep1+ano+sep1+mes+sep1+dia+sep1+hora+sep1+minuto+sep1+segundo+sep1+valortemperatura+sep1+valorporta+sep1+volts+sep1;


Serial.print("Valor de Todas as Infos:");
Serial.println(todasinfos);


//Salvando no SD Card a string todasinfos. Arquivo LOG. "text.txt"

SPISD.begin(SD_SCK, SD_MISO, SD_MOSI);
    if (!SD.begin(SD_CS_PIN,SPISD)) {  //SD_CS_PIN this pin is just the dummy pin since the SD need the input 
    Serial.println(F("failed!"));
    return;
    }
    else Serial.println(F("SD read!"));
    myFile = SD.open("/test.txt", "a"); //append to file
  if (myFile)
  {
    Serial.print("Writing to test.txt...");
    myFile.println(todasinfos);
    myFile.close();
    Serial.println("done.");
  }
  else
  {
    Serial.println("error opening test.txt to write");
  }
  myFile = SD.open("/test.txt", "r"); //read from file
  if (myFile)
  {
    Serial.println("test.txt:");
    String inString;  //need to use Strings because of the ESP32 webserver
    while (myFile.available())
    {
      inString += myFile.readString();
    }
    myFile.close();
    Serial.println("");
  Serial.print("Conteúdo total:");

  }
  
  
  else
  {
    Serial.println("error opening test.txt to read");
  }


//Salvando no SD Card. Arquivosend. no arquivo send.txt a String todasinfossend. Todas as Strings do send.txt serão enviadas para o Python.

String arquivodeenvio = "";

SPISD.begin(SD_SCK, SD_MISO, SD_MOSI);
    if (!SD.begin(SD_CS_PIN,SPISD)) {  //SD_CS_PIN this pin is just the dummy pin since the SD need the input 
    Serial.println(F("failed!"));
    return;
    }
    else Serial.println(F("SD read!"));
    arquivosend = SD.open("/send.txt", "a"); //append to file
  if (arquivosend)
  {
    Serial.print("Writing to send.txt...");
    arquivosend.print(todasinfossend);
    arquivosend.close();
    Serial.println("done.");
  }
  else
  {
    Serial.println("error opening test.txt to write");
  }
  arquivosend = SD.open("/send.txt", "r"); //read from file
  if (arquivosend)
  {
    Serial.println("send.txt:");
    String sendpost;  //need to use Strings because of the ESP32 webserver
    while (arquivosend.available())
    {
      sendpost += arquivosend.readString();
    }
    arquivosend.close();
    Serial.println("");
  Serial.print("Conteúdo total:");
  Serial.println(sendpost);
  arquivodeenvio = sendpost;
  }

  
  
  else
  {
    Serial.println("error opening test.txt to read");
  }
  
  Serial.print("Gravações: ");
  Serial.println(boot_count);
  Serial.print("Tamanho da String Arquivodeenvio: ");
  Serial.println(arquivodeenvio.length());

/// "if" principal do programa, responsável por ligar o rádio e enviar os dados para o Python
/// Se a Temperatura estiver maior ou igual a 8 graus, a programação entrará no "if"
/// Se a Porta for aberta, a programação entrará no "if"
/// Se o arquivosend (send.txt do SD Card) estiver com as 5 ultimas gravações (totalizando 185 caracteres), a programação entrará no "if"

if ( Sensor.getTempCByIndex(0) >= 7 || digitalRead(PIN_PORTA) == HIGH || arquivodeenvio.length() == 185 ) {

/// Caso a porta tenha acionado o "if" principal, com este próximo "if", o programa acionará o Buzzer 

  if (digitalRead(PIN_PORTA) == HIGH){
    digitalWrite (PIN_BUZZER, HIGH);
    Serial.println("LIGANDO O BUZZER");
  }

/// Caso a temperatura tenha acionado o "if" principal, com este próximo "if", o programa acionará o Buzzer com dois bips iniciais
/// Diferenciando, de forma sonora, o tipo de "ritmo" do Buzzer

  if (digitalRead(Sensor.getTempCByIndex(0)) >= 26){
    digitalWrite (PIN_BUZZER, HIGH);
    delay(500);
    Serial.println("LIGANDO O BUZZER");
    digitalWrite (PIN_BUZZER, LOW);
    delay(500);
    digitalWrite (PIN_BUZZER, HIGH);
  }

  Serial.println("Iniciando o código completo...");

////// Aqui é onde a parte de rádio do arduino é ligado, maior consumo de bateria
  
  Serial.setTimeout(10000);
  pinMode(SIM800L_POWER, OUTPUT);
  digitalWrite(SIM800L_POWER, HIGH);
  Sensor.begin();
  
  Serial2.begin(9600, SERIAL_8N1, SIM800L_TX, SIM800L_RX);
  delay(2000);
  while (Serial2.available()) {
    Serial.write(Serial2.read());
  }
  delay(1000);

  /// Função que define a comunicação GPRS
  gsm_config_gprs();
  
}

else {

  ///// Caso o "if" principal não tenha sido acionado, o programa não ligará o rádio e entrará no modo Sleep
  

  Serial.println ("Não liguei o Rádio");
  Serial.println ("Entrando em Deep Sleep");
  esp_sleep_enable_ext0_wakeup(GPIO_NUM_35,1);
  esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP_01 * uS_TO_S_FACTOR);
  esp_deep_sleep_start();
  Serial.println ("Eu não deveria conseguir ler isso");
  
}
  
}

void loop() {

/// parâmetros de verificação e delay, o "void loop poderia estar vazio*"

  Sensor.begin();
  gsm_http_post("param=TestFromMySim800");
    delay(1000);
    
    
}

/// Dados que serão enviados pelo comando Post

void gsm_http_post( String postdata) {
  pinMode(VOLTAGE_PIN,INPUT);

/// Com os dados de data e hora que já foram gravados, vamos tratar esses dados e dividí-los em ano, mês, dia, hora, minuto, segundo. ////

    DateTime now = rtc.now();
    String ano = "";
    ano = now.year();
    String mes = "";
    mes = now.month();
    String dia = "";
    dia = now.day();

    

    String hora = "";
    hora = now.hour();
    String minuto = "";
    minuto = now.minute();
    String segundo = "";
    segundo = now.second();

    //// "if"s com a mesma intenção de organizar os dados como feito no setup ///

if (mes.length() < 2) {
      mes = "0"+mes;
    }
    

    if (dia.length() < 2) {
      dia = "0"+dia;
    }


    if (hora.length() < 2) {
      hora = "0"+hora;
    }

    if (minuto.length() < 2) {
      minuto = "0"+minuto;
    }

    if (segundo.length() < 2) {
      segundo = "0"+segundo;
    }
    String dataehora = "";
    String barra = "/";
    String espaco = " ";
    String doispontos = ":";

    /// String de data e hora formatado para o SQL Server
    dataehora = dia+barra+mes+barra+ano+espaco+hora+doispontos+minuto+doispontos+segundo;

    Serial.println(dataehora);

  Serial.println(" --- Start GPRS & HTTP --- ");
  String statusporta = "status";

  /// Transforma o nível lógico da porta em String
  
  if (digitalRead(PIN_PORTA) == HIGH){
    statusporta = "aberta";
  }
  if (digitalRead(PIN_PORTA) == LOW){
    statusporta = "fechada";
  }

/// mede a tensão da pilha e coloca esse valor na variável "volts"

float volts = 0.0;
volts = analogRead(15)*(5.0/1023.0);


///Faz a leitura do cartão SD, lê os valores de send.txt e os atribui na variável "sendpost"



arquivosend = SD.open("/send.txt", "r"); //read from file

    Serial.println("send.txt:");
    String sendpost;  //need to use Strings because of the ESP32 webserver
    while (arquivosend.available())
    {
      sendpost += arquivosend.readString();
    }
    
    arquivosend.close();
    Serial.println("");
  Serial.print("Conteúdo total:");
  Serial.println(sendpost);


  String temperatura;
  Sensor.begin();
  Sensor.requestTemperatures();
  temperatura = Sensor.getTempCByIndex(0);

  Serial.println("");
  Serial.print("Gravações: ");
  Serial.println(boot_count);
  Serial.println("");
  Serial.print("Tamanho da String: ");
  Serial.println(sendpost.length());
  
  /// O programa pode fazer até 2 envios do comando Post, 1 para a url e outro para a url2
  /// Cada url corresponde a um programa do Python
  /// url corresponde ao programa que gravará sempre os ultimos 5 conjuntos de dados
  /// url2 corresponde ao programa que gravará no SQL.

  /// Caso o arquivo send.txt tenha 5 gravações, o próximo "if" será acionado, dando início ao primeiro envio.
  /// Próximo if referente ao Envio 1 (com os 5 Registros)
  if (sendpost.length() == 185){
  gsm_send_serial("AT+CLTS=1");
  gsm_send_serial("AT+CCLK?");
  gsm_send_serial("AT+SAPBR=1,1");
  gsm_send_serial("AT+SAPBR=2,1");
  gsm_send_serial("AT+HTTPINIT");
  gsm_send_serial("AT+HTTPPARA=CID,1");
  gsm_send_serial("AT+HTTPPARA=URL," + url);
  gsm_send_serial("AT+HTTPPARA=CONTENT,application/x-www-form-urlencoded");
  gsm_send_serial("AT+HTTPDATA=192,5000"); 
  
  ///entre "<" para que o Python consiga identifcar qual parte do envio é relevante para se tratada
  
  gsm_send_serial("<"+sendpost+"<");
  gsm_send_serial(postdata);
  gsm_send_serial("AT+HTTPACTION=1");
  Serial.print("lugar2");
  gsm_send_serial("AT+HTTPREAD");
  gsm_send_serial("AT+HTTPTERM");
  gsm_send_serial("AT+SAPBR=0,1");
    
  }

  ///Este próximo envio, sempre será acionado uma vez que o "if" principal seja verdadeiro.
  ///Próximo IF, refere-se ao Envio 2.
  
  Serial.print("Enviando o Segundo Dado");

  gsm_send_serial("AT+CLTS=1");
  gsm_send_serial("AT+CCLK?");
  gsm_send_serial("AT+SAPBR=1,1");
  gsm_send_serial("AT+SAPBR=2,1");
  gsm_send_serial("AT+HTTPINIT");
  gsm_send_serial("AT+HTTPPARA=CID,1");
  gsm_send_serial("AT+HTTPPARA=URL," + url2);
  gsm_send_serial("AT+HTTPPARA=CONTENT,application/x-www-form-urlencoded");
  gsm_send_serial("AT+HTTPDATA=192,5000"); 
  ///entre "<" para que o Python consiga identifcar qual parte do envio é relevante para se tratada
  gsm_send_serial("<"+statusporta+"<"+temperatura+"<"+MEUID+"<"+volts+"<"+dataehora+"<x0");
  gsm_send_serial(postdata);
  gsm_send_serial("AT+HTTPACTION=1");
  Serial.print("lugar2");
  gsm_send_serial("AT+HTTPREAD");
  gsm_send_serial("AT+HTTPTERM");
  gsm_send_serial("AT+SAPBR=0,1");

///Desligando o Buzzer caso ele tenha sido acionado incialmente.
if (digitalRead(PIN_BUZZER) == HIGH) {
  digitalWrite(PIN_BUZZER,LOW);
}


///Declara as possibilidades e configurações do deepsleep. Podendo ser acordado quando a porta for aberta ou após 2 minutos.
esp_sleep_enable_ext0_wakeup(GPIO_NUM_35,1);
esp_sleep_enable_timer_wakeup(TIME_TO_SLEEP * uS_TO_S_FACTOR);

///Início do DeepSleep.
esp_deep_sleep_start();
  

}

/// função que define a ordem de envios dos comandos HTTP Post.
void gsm_config_gprs() {
  Serial.println(" --- CONFIG GPRS --- ");
  gsm_send_serial("AT+SAPBR=3,1,Contype,GPRS");
  gsm_send_serial("AT+SAPBR=3,1,APN," + apn);
  if (apn_u != "") {
    gsm_send_serial("AT+SAPBR=3,1,USER," + apn_u);
  }
  if (apn_p != "") {
    gsm_send_serial("AT+SAPBR=3,1,PWD," + apn_p);
  }
}


/// Função para configurar o que será mostrado no monitor Serial durante a ligação do rádio.

void gsm_send_serial(String command) {

  Serial.println("Send ->: " + command);
  Serial2.println(command);
  long wtimer = millis();
  while (wtimer + 2000 > millis()) {
    while (Serial2.available()) {
      Serial.write(Serial2.read());
    }
  }
  Serial.println();
  
}
