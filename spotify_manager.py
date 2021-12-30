import spotipy
from spotipy.oauth2 import SpotifyOAuth
import logging

class TrackData():
    def __init__(self, track_data = {}):
        self._track_data = track_data

    def set_track_data(self, new_track_data):
        self._track_data = new_track_data
    
    def get_track_progress(self) -> int:
        try:
            return self._track_data['progress_ms']
        except:
            return 0
    
    def get_track_length(self) -> int:
        try:
            return self._track_data['item']['duration_ms']
        except:
            return 0

    def get_track_progress_percent(self) -> float:
        length = self.get_track_length()
        progress = self.get_track_progress()

        if length == 0:
            return 0

        return progress / length

    def get_track_name(self) -> str:
        try:
            return self._track_data['item']['name']
        except:
            return 'None'

    def get_track_artists(self) -> str:
        artists_str = str()
        try:
            for artist in self._track_data['item']['artists']:
                if len(artists_str) == 0:
                    artists_str = artist['name']
                else:
                    artists_str += ' / ' + artist['name']
            return artists_str
        except:
            return 'None'

    def get_track_album(self) -> str:
        try:
            return self._track_data['item']['album']['name']
        except: 
            return 'None'

    def is_currently_playing(self) -> bool:
        try:
            return self._track_data['is_playing']
        except:
            return False

    def __eq__(self, other) -> bool:
        if isinstance(other, TrackData):
            return (self.get_track_album() == other.get_track_album()) and (self.get_track_artists() == other.get_track_artists()) and (self.get_track_name() == other.get_track_name()) 
        return False

    def __str__(self) -> str:
        return '{0} by {1} from {2}'.format(self.get_track_name(), self.get_track_artists(), self.get_track_album())
    

class SpotifyManager():
    def __init__(self, track_changed_callback) -> None:
        self._spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
            scope='user-read-currently-playing',
            open_browser=False
        ))
        self._currently_played = TrackData()
        self._last_played = TrackData()
        self._track_changed_callback = track_changed_callback
    
    def update_data(self) -> None:
        try:
            api_data = self._spotify.currently_playing('PL')
        except Exception as ex:
            ex_type = str(type(ex).__name__)
            ex_msg = str(ex.message if hasattr(ex, 'message') else ex)
            logging.error(f'{ex_type} happened while fetching data from Spotify API: {ex_msg}')
            return
        current_track = TrackData(api_data)

        if current_track != self._last_played:
            self._last_played = current_track
            self._currently_played = current_track
            self._track_changed_callback(current_track)
        else:
            self._currently_played = current_track

    def get_current_track(self) -> TrackData:
        return self._currently_played