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

        pattern = r'music\.yandex\.(ru|com|by|kz)/album/\d+/track/(\d+)'
        match = re.search(pattern, url)
        
        return match.group(2) if match else url
    
    async def fetch_track_videos(self, track_id: str) -> Optional[dict]:
        try:
            if not self.client:
                await self.connect()

            track = await self.client.tracks(track_id)
            track = track[0]

            if not track.background_video_uri:
                raise ValueError("No video found for this track")

            # Get the first artist's name
            artist_name = track.artists[0].name if track.artists else "Unknown Artist"

            return [{
                'title': track.title,
                'cover_uri': track.cover_uri,
                'artist': artist_name,
                'embed_url': track.background_video_uri,
                'provider_video_id': None
            }]

        except NetworkError as e:
            raise ConnectionError(f"Network error: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to fetch video data: {e}")

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

            token = "YOUR_TOKEN"
            fetcher = YandexMusicTrackFetcher(token)
            track_id = fetcher.extract_track_id(track_input)
            videos = await fetcher.fetch_track_videos(track_id)

            print("\nFound videos:")
            for video in videos:
                print(f"\nTitle: {video['title']}")
                print(f"Artist: {video['provider']}")
                print(f"Video URL: {video['embed_url']}")

        except ValueError as e:
            print(f"Error: {e}")
        except (ConnectionError, RuntimeError) as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nOperation cancelled by user")
            break

        try_again = input("\nDo you want to try again? (yes/no): ").strip().lower()
        if try_again not in ['yes', 'y']:
            break

if __name__ == "__main__":
    asyncio.run(main())
