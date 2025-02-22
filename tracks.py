import asyncio
import re
from typing import Optional
from yandex_music import ClientAsync
from yandex_music.track.track import Track
from yandex_music.exceptions import NetworkError

class YandexMusicTrackFetcher:
    def __init__(self, token: str):
        self.token = token
        self.client = None

    async def connect(self):
        self.client = ClientAsync(self.token)
        await self.client.init()

    @staticmethod
    def extract_track_id(url: str) -> str:
        if not url:
            raise ValueError("Track ID or URL cannot be empty")

        # Pattern to match Yandex Music track URLs
        pattern = r'music\.yandex\.(ru|com|by|kz)/album/\d+/track/(\d+)'
        match = re.search(pattern, url)
        
        return match.group(2) if match else url

    async def fetch_track(self, track_id: str) -> Optional[dict]:
        try:
            if not self.client:
                await self.connect()

            track = await self.client.tracks(track_id)
            track = track[0]  # Get the first track from the list

            label_name = 'N/A'
            if hasattr(track, 'albums') and track.albums and hasattr(track.albums[0], 'labels') and track.albums[0].labels:
                label_name = ', '.join([label.name for label in track.albums[0].labels])

            major_name = "Unknown Distributor"
            if hasattr(track, 'major') and track.major:
                major_name = track.major.name
            elif hasattr(track, 'albums') and track.albums and hasattr(track.albums[0], 'major') and track.albums[0].major:
                major_name = track.albums[0].major.name

            distributor_mapping = {
                "UNIVERSAL_MUSIC": "Universal Music Group",
                "UNIVERSAL_YANGO": "Universal Music Group (in Israel and Middle East)",
                "UNIKOP": "Universal Music Group (stolen releases in Russia)",
                "BELIEVE_DIGITAL": "Believe Digital",
                "TUNECORE": "TuneCore",
                "SONY": "Sony Music Entertainment",
                "WARNER": "Warner Music Group",
                "BROMA16": "Broma16",
                "BEGGARS": "Beggars Group",
                "SYMPHONIC": "Symphonic Distribution",
                "DISTROKID": "DistroKid",
                "FRESH_TUNES": "FreshTunes",
                "LABEL_ENGINE": "Label Engine",
                "ORCHARD": "The Orchard",
                "ONERPM": "ONErpm",
                "WORX": "LabelWorx",
                "RESERVOIR": "Reservoir Media",
                "IIP_DDS": "IIP-DDS"
            }
            
            if major_name in distributor_mapping:
                major_name = distributor_mapping[major_name]

            release_date = track.albums[0].release_date[:10] if hasattr(track.albums[0], 'release_date') and track.albums[0].release_date else "Unknown Date"
            
            artists = []
            if hasattr(track, 'artists'):
                artists = ', '.join([artist.name for artist in track.artists])

            available_countries = track.albums[0].regions if hasattr(track.albums[0], 'regions') else []

            return {
                'title': getattr(track, 'title', 'Unknown'),
                'version': getattr(track, 'version', None),
                'year': getattr(track.albums[0], 'year', 'N/A'),
                'label': label_name,
                'major': major_name,
                'release_date': release_date,
                'artists': artists,
                'duration_ms': getattr(track, 'duration_ms', 0),
                'available_countries': available_countries,
                'content_warning': getattr(track, 'content_warning', 'None'),
                'type': getattr(track, 'type', 'Unknown'),
                'track_sharing_flag': getattr(track, 'track_sharing_flag', False),
                'track_source': getattr(track, 'track_source', 'Unknown')
            }
        except NetworkError as e:
            if 'Parameters requirements are not met' in str(e):
                raise ConnectionError("Network error: The provided parameters do not meet the requirements.")
            raise ConnectionError(f"Network error: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to fetch track: {e}")

    def format_track_info(self, track_data: dict) -> str:
        output = []
        title = track_data['title']
        if track_data['version']:
            title += f" ({track_data['version']})"
        output.append(f"Track Title: {title}")
        output.append(f"Artist: {track_data['artists']}")
        output.append(f"Release Date: {track_data['year']}")
        output.append(f"Release Date: {track_data['release_date']}")
        
        duration_min = track_data['duration_ms'] // 60000
        duration_sec = (track_data['duration_ms'] % 60000) // 1000
        output.append(f"Duration: {duration_min}:{duration_sec:02d}")
        
        output.append(f"\n℗ {track_data['year']} {track_data['label']}")
        if track_data['available_countries']:
            output.append(f"Available in: {', '.join(track_data['available_countries'])}")
        output.append(f"Distributed by {track_data['major']}")
        output.append(f"Content Warning: {track_data['content_warning']}")
        output.append(f"Type: {track_data['type']}")
        output.append(f"Track Sharing Flag: {track_data['track_sharing_flag']}")
        output.append(f"Track Source: {track_data['track_source']}")
        
        return '\n'.join(output)

async def main():
    while True:
        try:
            track_input = input("Enter the Yandex Music track ID or URL: ").strip()
            if not track_input:
                print("Input cannot be empty. Please enter a valid track ID or URL.")
                continue

            if track_input.lower() in ['exit', 'quit', 'leave']:
                print("Exiting the program.")
                break

            if not re.match(r'^\d+$', track_input) and not re.match(r'^https?://', track_input):
                print("Invalid input. Please enter a valid track ID or URL.")
                continue
            
            token = "YOUR_TOKEN"

            fetcher = YandexMusicTrackFetcher(token)
            track_id = fetcher.extract_track_id(track_input)
            track_data = await fetcher.fetch_track(track_id)
            print("\n" + fetcher.format_track_info(track_data))

        except (ValueError, ConnectionError, RuntimeError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            break

        try_again = input("Do you want to try again? (yes/no): ").strip().lower()
        if try_again in ['yes', 'y']:
            continue
        else:
            break

if __name__ == "__main__":
    asyncio.run(main())