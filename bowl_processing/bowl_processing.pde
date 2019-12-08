import processing.video.*;
import processing.serial.*;

final int MaxVideo = 5; // 0..5
Movie current_video;
Movie videos[];
int video_number = 0;
int last_signal = 0;
int moving_since = 0;
final int ChangeEvery =  10000;// msecs, change video every...
final int Timeout = 5000; // msecs, they stopped moving
Serial usb;

void setup() {
  size(1920, 1080);
  // find the usb,
  usb = connectUSBSerial(9600);

  videos = new Movie [  MaxVideo ];
  for (int i=0; i<MaxVideo; i++) {
    videos[i] =  new Movie(this, "Video" + String.valueOf(i) + ".mp4");

    // preload videos
    //print("Preloading " + String.valueOf(i));
    //videos[i].play();
    //delay(10);
    //videos[i].stop();
  }

  videos[0].play();
}

void draw() {
  // watch for "1" on usb (from itsybitsy)
  if ( usb.available() > 1) {
    if (usb.readChar() == '*' ) {
      last_signal = millis();
      if (moving_since == 0) {
        // keep track of how long they are moving
        moving_since = millis();
      }
    }
  }

  // how long they have been moving (if they have been)
  int duration = millis() - moving_since;

  // they stopped moving, reset
  if (moving_since != 0) {

    // check for stopped moving
    if ( millis() - last_signal > Timeout) {
      moving_since  = 0;
      change_video(0);
    }
  }

  // decide if we need to change video
  if (moving_since != 0) {
    // every 2 seconds, change to the next video (+1)
    int next_video = (duration / ChangeEvery);
    // force to 0..5
    next_video = Math.min( next_video, MaxVideo - 1);

    if (next_video != video_number) {
      change_video(next_video);
    }
  }
}

void change_video(int new_video_number) {
  video_number = new_video_number;
  current_video.stop();
  current_video = videos[ video_number ];
  current_video.play();
}


void movieEvent(Movie m) {
  m.read();
}
