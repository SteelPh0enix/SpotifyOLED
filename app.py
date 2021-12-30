from display import Display, TextRow
from display_text_manager import DisplayTextManager
from progress_bar_manager import ProgressBarManager
from spotify_manager import SpotifyManager, TrackData
import schedule
import time
import logging

DISPLAY_WIDTH = 126
DISPLAY_HEIGHT = 64
DISPLAY_ADDRESS = 0x3C

display = Display(DISPLAY_WIDTH, DISPLAY_HEIGHT, DISPLAY_ADDRESS)
text_manager = DisplayTextManager(display)
progress_bar = ProgressBarManager(display,
                                  (5, display.row_position(TextRow.FOURTH) + 2),
                                  (display.width() - 10, display.char_height()))

def update_track_info_on_change(track: TrackData):
    logging.info(f'Track changed to {track.get_track_name()} by {track.get_track_artists()} from {track.get_track_album()}')
    text_manager.set_text(track.get_track_name(), TextRow.FIRST)
    text_manager.set_text(track.get_track_artists(), TextRow.SECOND)
    text_manager.set_text(track.get_track_album(), TextRow.THIRD)
    update_display()
    
spotify = SpotifyManager(update_track_info_on_change)

def update_track_info():
    track = spotify.get_current_track()
    progress = track.get_track_progress_percent()
    length_ms = track.get_track_length()
    progress_ms = track.get_track_progress()
    is_playing = track.is_currently_playing()
    
    length_min = length_ms // (1000 * 60)
    length_sec = (length_ms // 1000) - (length_min * 60)

    progress_min = progress_ms // (1000 * 60)
    progress_sec = (progress_ms // 1000) - (progress_min * 60)
    
    playing_str = 'PLAYING' if is_playing else 'PAUSED'

    topbar_text = '{0:02}:{1:02}/{2:02}:{3:02} {4}'.format(progress_min, progress_sec, length_min, length_sec, playing_str)

    text_manager.set_text(topbar_text, TextRow.TOPBAR)
    progress_bar.set_progress(progress)

def update_display_and_spotify():
    spotify.update_data()
    update_display()

def update_display():
    update_track_info()
    display.clear()
    text_manager.loop_texts()
    text_manager.update_display()
    progress_bar.draw()
    display.show()

def main():
    logging.info('Application started!')
    display.clear()
    text_manager.update_display()
    progress_bar.draw()
    display.show()

    schedule.every(1).seconds.do(update_display_and_spotify)

    logging.info('Everything set up, starting main loop!')
    while True:
        try:
            schedule.run_pending()
            time.sleep(0.5)
        except KeyboardInterrupt:
            logging.info('Keyboard interrupt detected, exiting...')
            exit(0)

if __name__ == '__main__':
    logging.basicConfig(filename='spotify_display.log',
                        encoding='utf-8',
                        level=logging.INFO,
                        format='[%(levelname)s] <%(asctime)s> %(message)s')
    main()