#include <Arduino.h>
#include <SD.h>
#include <M5Unified.h>
#include <esp_log.h>
#include <CSV_Parser.h>

static constexpr const gpio_num_t SDCARD_CSPIN = GPIO_NUM_4;
static constexpr const gpio_num_t PROBE_PIN = GPIO_NUM_7;

static constexpr const char exp_wave_filename[32] = "/explosion.wav";
static constexpr const char ranking_filename[32] = "/ranking.csv";

static int32_t wave_data_len;
static constexpr const size_t buf_num = 1;
static constexpr const size_t buf_size = 1024*45;
static uint8_t wav_data[buf_num][buf_size];
static constexpr const int32_t WAVE_PLAY_TIME = 2000;
static constexpr const int32_t DISPLY_BLINK_TIME = 1000;
static constexpr const int32_t SKIP_PLAY_TIME = 2000;
static constexpr const int32_t CRASH_CHATTERING_TIME = 1000;
static constexpr const int32_t CRASH_RATE_SEC = 2;


M5GFX display;
M5Canvas canvas_timer(&display);
M5Canvas canvas_crash(&display);
M5Canvas canvas_ranking(&display);
int16_t canvas_timer_width;
int16_t canvas_timer_height;
int16_t canvas_timer_x;
int16_t canvas_timer_y;
int16_t canvas_crash_width;
int16_t canvas_crash_height;
int16_t canvas_crash_x;
int16_t canvas_crash_y;
int16_t canvas_ranking_width;
int16_t canvas_ranking_height;
int16_t canvas_ranking_x;
int16_t canvas_ranking_y;
  


bool is_btn_pressed = false;
bool is_display_blink = true;
int32_t wall_crash_cnt = 0;
unsigned long prev_time = 0;
unsigned long cur_time = 0;
unsigned long prev_bomb_time = 0;
unsigned long prev_crash_time = 0;
unsigned long prev_display_blink_time = 0;
unsigned long maze_processing_time = 0;
long maze_time = 0;
int32_t cur_ranking_num = -1;
bool is_1st_sort = true;


#define RANKING_LIST_MAX 20
struct __attribute__((packed)) ranking_list_t
{
  int32_t min_num;
  int32_t sec_num;
  int32_t ms_num;
  int32_t crash_num;
  int32_t rate;
};
ranking_list_t ranking_list[RANKING_LIST_MAX];





enum diplay_status_e {
  INIT,
  START,
  PROCESSING,
  STOP,
  RESET
};
enum diplay_status_e diplay_status;

struct __attribute__((packed)) subddddd_t
{
  char identifier[4];
  uint32_t chunk_size;
  uint8_t data[1];
};



struct __attribute__((packed)) wav_header_t
{
  char RIFF[4];
  uint32_t chunk_size;
  char WAVEfmt[8];
  uint32_t fmt_chunk_size;
  uint16_t audiofmt;
  uint16_t channel;
  uint32_t sample_rate;
  uint32_t byte_per_sec;
  uint16_t block_size;
  uint16_t bit_per_sample;
};
static wav_header_t wav_data_header;

struct __attribute__((packed)) sub_chunk_t
{
  char identifier[4];
  uint32_t chunk_size;
  uint8_t data[1];
};

static bool loadSdWav(const char* filename, int32_t* ret_data_len, wav_header_t* wav_header)
{
  auto file = SD.open(filename);

  if (!file) { return false; }

  file.read((uint8_t*)wav_header, sizeof(wav_header_t));

  ESP_LOGD("wav", "RIFF           : %.4s" , wav_header->RIFF          );
  ESP_LOGD("wav", "chunk_size     : %d"   , wav_header->chunk_size    );
  ESP_LOGD("wav", "WAVEfmt        : %.8s" , wav_header->WAVEfmt       );
  ESP_LOGD("wav", "fmt_chunk_size : %d"   , wav_header->fmt_chunk_size);
  ESP_LOGD("wav", "audiofmt       : %d"   , wav_header->audiofmt      );
  ESP_LOGD("wav", "channel        : %d"   , wav_header->channel       );
  ESP_LOGD("wav", "sample_rate    : %d"   , wav_header->sample_rate   );
  ESP_LOGD("wav", "byte_per_sec   : %d"   , wav_header->byte_per_sec  );
  ESP_LOGD("wav", "block_size     : %d"   , wav_header->block_size    );
  ESP_LOGD("wav", "bit_per_sample : %d"   , wav_header->bit_per_sample);

  if ( memcmp(wav_header->RIFF,    "RIFF",     4)
    || memcmp(wav_header->WAVEfmt, "WAVEfmt ", 8)
    || wav_header->audiofmt != 1
    || wav_header->bit_per_sample < 8
    || wav_header->bit_per_sample > 16
    || wav_header->channel == 0
    || wav_header->channel > 2
    )
  {
    file.close();
    return false;
  }

  file.seek(offsetof(wav_header_t, audiofmt) + wav_header->fmt_chunk_size);
  sub_chunk_t sub_chunk;

  file.read((uint8_t*)&sub_chunk, 8);

  ESP_LOGD("wav", "sub id         : %.4s" , sub_chunk.identifier);
  ESP_LOGD("wav", "sub chunk_size : %d"   , sub_chunk.chunk_size);

  while(memcmp(sub_chunk.identifier, "data", 4))
  {
    if (!file.seek(sub_chunk.chunk_size, SeekMode::SeekCur)) { break; }
    file.read((uint8_t*)&sub_chunk, 8);

    ESP_LOGD("wav", "sub id         : %.4s" , sub_chunk.identifier);
    ESP_LOGD("wav", "sub chunk_size : %d"   , sub_chunk.chunk_size);
  }

  if (memcmp(sub_chunk.identifier, "data", 4))
  {
    file.close();
    return false;
  }

  int32_t data_len = sub_chunk.chunk_size;
  *ret_data_len = data_len;
  bool flg_16bit = (wav_header->bit_per_sample >> 4);

  size_t idx = 0;
  while (data_len > 0) {
    size_t len = data_len < buf_size ? data_len : buf_size;
    len = file.read(wav_data[idx], len);
    data_len -= len;
    idx = idx < (buf_num - 1) ? idx + 1 : 0;
  }
  file.close();

  return true;
}

static bool playWav(int idx, int32_t data_len, wav_header_t* wav_header)
{
  bool flg_16bit = (wav_header->bit_per_sample >> 4);
  if (flg_16bit) {
    M5.Speaker.playRaw((const int16_t*)wav_data[idx], data_len >> 1, wav_header->sample_rate, wav_header->channel > 1, 1, 0);
  } else {
    M5.Speaker.playRaw((const uint8_t*)wav_data[idx], data_len, wav_header->sample_rate, wav_header->channel > 1, 1, 0);
  }
  return true;
}

void display_time_and_crash(int min_num, int sec_num, int ms_num, int wall_crash_cnt) {
  canvas_timer.setTextSize(2.5);
  canvas_timer.printf("%02d:", min_num);
  canvas_timer.setTextSize(3);
  canvas_timer.printf("%02d\n", sec_num);
  canvas_timer.setTextSize(2);
  canvas_timer.printf("    .%03d", ms_num);
  canvas_crash.printf("  %d 回", wall_crash_cnt);
}
void display_ranking_line(int ranking_rank, int min_num, int sec_num, int ms_num, int crash_num) {
  canvas_ranking.printf("%2d位\n", ranking_rank);
  canvas_ranking.printf("  %02d:%02d.%03d %2d回\n", min_num, sec_num, ms_num, crash_num);
}
void display_ranking_list(int ranking_rank) {
  for(int i = 0; i < RANKING_LIST_MAX; i++) {
    if(ranking_rank == i) {
      canvas_ranking.setTextColor(RED);
      if(is_display_blink) {
        display_ranking_line(i+1, ranking_list[i].min_num, ranking_list[i].sec_num, ranking_list[i].ms_num, ranking_list[i].crash_num);
      } else {
        canvas_ranking.println(" ");
        canvas_ranking.println(" ");
      }
      canvas_ranking.setTextColor(WHITE);
    } else {
      display_ranking_line(i+1, ranking_list[i].min_num, ranking_list[i].sec_num, ranking_list[i].ms_num, ranking_list[i].crash_num);
    }
  }
}



int cal_ranking_rate(int32_t min_num, int32_t sec_num, int32_t ms_num, int32_t crash_num);
void write_ranking_data(int32_t min_num, int32_t sec_num, int32_t ms_num, int32_t crash_num);
int sort_ranking_list(int32_t min_num, int32_t sec_num, int32_t ms_num, int32_t crash_num);

void init_ranking_list() {
  int32_t min_num = 59;
  int32_t sec_num = 59;
  int32_t ms_num = 999;
  int32_t crash_num = 99;
  for(int i = 0; i < RANKING_LIST_MAX; i++) {
    ranking_list[i].min_num = min_num;
    ranking_list[i].sec_num = sec_num;
    ranking_list[i].ms_num = ms_num;
    ranking_list[i].crash_num = crash_num;
    ranking_list[i].rate = cal_ranking_rate(min_num, sec_num, ms_num, crash_num);
  }
}

void write_ranking_data(int32_t min_num, int32_t sec_num, int32_t ms_num, int32_t crash_num) {
  File ranking_file = SD.open(ranking_filename, FILE_APPEND);
  ranking_file.printf("%d,%d,%d,%d\n",min_num, sec_num, ms_num, crash_num);
  ranking_file.flush();
  ranking_file.close();
  delay(100);
}

int cal_ranking_rate(int32_t min_num, int32_t sec_num, int32_t ms_num, int32_t crash_num) {
  int32_t rate = 0;
  int32_t total_sec = 0;

  total_sec += min_num * 60;
  total_sec += sec_num;
  total_sec += CRASH_RATE_SEC * crash_num;

  rate = ms_num + (total_sec * 1000);

  return rate;
}

int sort_ranking_list(int32_t min_num, int32_t sec_num, int32_t ms_num, int32_t crash_num) {
  int ranking_num = -1;
  int32_t cur_rate = cal_ranking_rate(min_num, sec_num, ms_num, crash_num);

  for(int i = 0; i < RANKING_LIST_MAX; i++) {
    if(cur_rate <= ranking_list[i].rate) {
      ranking_num = i;
      for(int j = RANKING_LIST_MAX-1; j >= i; j--) {
        ranking_list[j].min_num = ranking_list[j-1].min_num;
        ranking_list[j].sec_num = ranking_list[j-1].sec_num;
        ranking_list[j].ms_num = ranking_list[j-1].ms_num;
        ranking_list[j].crash_num = ranking_list[j-1].crash_num;
        ranking_list[j].rate = ranking_list[j-1].rate;
      }
      ranking_list[ranking_num].min_num = min_num;
      ranking_list[ranking_num].sec_num = sec_num;
      ranking_list[ranking_num].ms_num = ms_num;
      ranking_list[ranking_num].crash_num = crash_num;
      ranking_list[ranking_num].rate = cur_rate;
      break;
    }
  }

  return ranking_num;
}

void load_ranking_list() {
  int32_t min_num = 59;
  int32_t sec_num = 59;
  int32_t ms_num = 999;
  int32_t crash_num = 99;

  if(!SD.exists(ranking_filename)) {
    File ranking_file = SD.open(ranking_filename, FILE_WRITE);
    ranking_file.printf("%d,%d,%d,%d\n",min_num, sec_num, ms_num, wall_crash_cnt);
    ranking_file.close();
    delay(100);
  }
//  CSV_Parser cp(/*format*/ "cccc", /*has_header*/ false);
  CSV_Parser cp(/*format*/ "ssss", /*has_header*/ false);
  File ranking_file = SD.open(ranking_filename, FILE_READ);
  delay(100);
  while(ranking_file.available()) {
    cp << (char)ranking_file.read();
  }
  ranking_file.close();
  delay(100);
  char **col0 = (char**)cp[0];
  char **col1 = (char**)cp[1];
  char **col2 = (char**)cp[2];
  char **col3 = (char**)cp[3];

  for(int row = 0; row < cp.getRowsCount(); row++) {
    min_num = atoi(col0[row]);
    sec_num = atoi(col1[row]);
    ms_num = atoi(col2[row]);
    crash_num = atoi(col3[row]);
    sort_ranking_list(min_num, sec_num, ms_num, crash_num);
  }

}



void setup() {
  auto cfg = M5.config();
  M5.begin(cfg);  

  prev_time = millis();
  prev_bomb_time = millis();
  prev_crash_time = millis();
  prev_display_blink_time = millis();

  if(SD.begin(SDCARD_CSPIN, SPI, 1000000)) {
    if(loadSdWav(exp_wave_filename, &wave_data_len, &wav_data_header)) {
      exit;
    }
    // 起動音
    playWav(0, wave_data_len, &wav_data_header);
    init_ranking_list();
    load_ranking_list();
  }
  M5.Speaker.setVolume(255);
  
  display.begin();
  display.fillScreen(TFT_BLACK);
  diplay_status = INIT;
  canvas_timer_width = (float)display.width() * 3.0f/5.0f;
  canvas_timer_height = (float)display.height() * 2.0f/3.0f;
  canvas_timer_x = 0;
  canvas_timer_y = 0;

  canvas_crash_width = canvas_timer_width;
  canvas_crash_height = display.height() - canvas_timer_height;
  canvas_crash_x = 0;
  canvas_crash_y = canvas_timer_height;

  canvas_ranking_width = display.width() - canvas_timer_width - 10;
  canvas_ranking_height = display.height();
  canvas_ranking_x = canvas_timer_width + 10;
  canvas_ranking_y = 0;

  pinMode(PROBE_PIN, INPUT_PULLUP);

}

void loop() {
  M5.update();

  canvas_timer.startWrite();
  canvas_crash.startWrite();
  canvas_ranking.startWrite();
  canvas_timer.createSprite(canvas_timer_width, canvas_timer_height);
  canvas_crash.createSprite(canvas_crash_width, canvas_crash_height);
  canvas_ranking.createSprite(canvas_ranking_width, canvas_ranking_height);


  canvas_timer.setCursor(0, 0);
  canvas_timer.setTextSize(1);
  canvas_timer.setFont(&fonts::lgfxJapanGothic_24);
  canvas_timer.println("経過時間");
  canvas_timer.setTextSize(2);

  canvas_crash.setCursor(0, 0);
  canvas_crash.setTextSize(1);
  canvas_crash.setFont(&fonts::lgfxJapanMincho_24);
  canvas_crash.println("壁にあたった回数");
  canvas_crash.setTextSize(2);

  canvas_ranking.setCursor(0, 0);
  canvas_ranking.setTextSize(1);
  canvas_ranking.setFont(&fonts::lgfxJapanGothic_24);
  canvas_ranking.println("順位");
  canvas_ranking.setTextSize(0.5);



  cur_time = millis();
  if(diplay_status == PROCESSING) {
    maze_time = cur_time - maze_processing_time;
  }
  int32_t ms_num = maze_time % 1000;
  int32_t ms_q = maze_time / 1000;
  int32_t sec_num = ms_q % 60;
  int32_t sec_q = ms_q / 60;
  int32_t min_num = sec_q % 60;
  int32_t min_q = sec_q / 60;


  if(M5.Touch.isEnabled()) {
    auto t = M5.Touch.getDetail();
    if(is_btn_pressed) {
      if(t.isReleased()) {
        switch(diplay_status) {
          case INIT:
            diplay_status = START;
            break;
          case START:
            diplay_status = PROCESSING;
            maze_processing_time = millis();
            wall_crash_cnt = 0;
            break;
          case PROCESSING:
            diplay_status = STOP;
            break;
          case STOP:
            diplay_status = RESET;
            break;
          case RESET:
            diplay_status = START;
            break;
        }
        is_btn_pressed = false;
      }
    } else {
      is_btn_pressed = t.isPressed();
    }
  }

  switch(diplay_status) {
    case START:
      if((long)(cur_time - prev_display_blink_time) > DISPLY_BLINK_TIME) {
        prev_display_blink_time = millis();
        if(is_display_blink) {
          is_display_blink = false;
        } else {
          is_display_blink = true;
        }
      }
      if(is_display_blink) {
        display_time_and_crash(0, 0, 0, 0);
      } else {
        canvas_timer.printf("");
        canvas_crash.printf("");
      }
      display_ranking_list(-1);
      break;
    case PROCESSING:
      if(!digitalRead(PROBE_PIN)) {
        if((long)(cur_time - prev_bomb_time) > WAVE_PLAY_TIME) {
          prev_bomb_time = cur_time;
          playWav(0, wave_data_len, &wav_data_header);
        }
        if((long)(cur_time - prev_crash_time) > CRASH_CHATTERING_TIME) {
          prev_crash_time = cur_time;
          wall_crash_cnt++;
        }
        delay(100);
      }
      display_time_and_crash(min_num, sec_num, ms_num, wall_crash_cnt);
      display_ranking_list(-1);
      break;
    case STOP:
      // プレイ時間が短すぎた場合はスキップする
      if((long)(cur_time - prev_display_blink_time) > DISPLY_BLINK_TIME) {
        prev_display_blink_time = cur_time;
        if(is_display_blink) {
          is_display_blink = false;
        } else {
          is_display_blink = true;
        }
      }
      if(is_display_blink) {
        display_time_and_crash(min_num, sec_num, ms_num, wall_crash_cnt);
      } else {
        canvas_timer.print("");
        canvas_crash.printf("");
      }

      // ランキング表示
      if(maze_time >= SKIP_PLAY_TIME && is_1st_sort) {
        cur_ranking_num = sort_ranking_list(min_num, sec_num, ms_num, wall_crash_cnt);
        write_ranking_data(min_num, sec_num, ms_num, wall_crash_cnt);
        is_1st_sort = false;
      }
      display_ranking_list(cur_ranking_num);

      break;
    case INIT:
    default:
      diplay_status = START;
    case RESET:
      prev_display_blink_time = millis();
      display_time_and_crash(0, 0, 0, 0);
      display_ranking_list(-1);
      is_1st_sort = true;
      break;
  }



  // end
  canvas_timer.pushSprite(canvas_timer_x, canvas_timer_y);
  canvas_crash.pushSprite(canvas_crash_x, canvas_crash_y);
  canvas_ranking.pushSprite(canvas_ranking_x, canvas_ranking_y);
  canvas_timer.endWrite();
  canvas_crash.endWrite();
  canvas_ranking.endWrite();

  delay(10);
  return;

}
