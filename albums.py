import asyncio
import re
from typing import Optional
from yandex_music import ClientAsync
from yandex_music.album.album import Album
from yandex_music.exceptions import NetworkError


class YandexMusicFetcher:
    def __init__(self, token: str):
        self.token = token
        self.client = None

    async def connect(self):
        self.client = ClientAsync(self.token)
        await self.client.init()

    @staticmethod
    def extract_album_id(url: str) -> str:
        if not url:
            raise ValueError("Album ID or URL cannot be empty")

        pattern = r'music\.yandex\.(ru|com|by|kz)/album/(\d+)(?:/track/\d+)?'
        match = re.search(pattern, url)
        
        return match.group(2) if match else url

    async def fetch_album(self, album_id: str) -> Optional[dict]:
        try:
            if not self.client:
                await self.connect()

            album = await self.client.albums_with_tracks(album_id)
            
            label_name = 'N/A'
            if hasattr(album, 'labels') and album.labels:
                label_name = ', '.join([label.name for label in album.labels])

            major_name = album.volumes[0][0].major.name if album.volumes and album.volumes[0] and album.volumes[0][0].major else "Unknown"

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

            release_date = album.release_date[:10] if hasattr(album, 'release_date') and album.release_date else "Unknown Date"
            
            artists = []
            if hasattr(album, 'artists'):
                artists = ', '.join([artist.name for artist in album.artists])

            available_countries = album.regions if hasattr(album, 'regions') else []

            return {
                'title': getattr(album, 'title', 'Unknown'),
                'version': getattr(album, 'version', None),
                'year': getattr(album, 'year', 'N/A'),
                'label': label_name,
                'major': major_name,
                'release_date': release_date,
                'artists': artists,
                'volumes': getattr(album, 'volumes', []) if hasattr(album, 'volumes') else [],
                'available_countries': available_countries
            }
        except NetworkError as e:
            raise ConnectionError(f"Network error: {e}")
        except Exception as e:
            raise RuntimeError(f"Failed to fetch album: {e}")

    def format_album_info(self, album_data: dict) -> str:
        output = []
        title = album_data['title']
        if album_data['version']:
            title += f" ({album_data['version']})"
        output.append(f"Release Title: {title}")
        output.append(f"Artist: {album_data['artists']}")
        output.append(f"Release Date: {album_data['year']}")
        output.append(f"Release Date: {album_data['release_date']}")
        output.append("\nTracklist:")

        volumes = album_data.get('volumes', [])
        if volumes:
            if len(volumes) > 1:
                for volume_idx, volume in enumerate(volumes):
                    output.append(f"\nMedium {volume_idx + 1}:")
                    for idx, track in enumerate(volume):
                        artists = ', '.join([artist.name for artist in track.artists])
                        duration_min = track.duration_ms // 60000
                        duration_sec = (track.duration_ms % 60000) // 1000
                        version_text = f" ({track.version})" if track.version else ""
                        output.append(f"{idx + 1}. {track.title}{version_text} - {artists} ({duration_min}:{duration_sec:02d})")
            else:
                volume = volumes[0]
                for idx, track in enumerate(volume):
                    artists = ', '.join([artist.name for artist in track.artists])
                    duration_min = track.duration_ms // 60000
                    duration_sec = (track.duration_ms % 60000) // 1000
                    version_text = f" ({track.version})" if track.version else ""
                    output.append(f"{idx + 1}. {track.title}{version_text} - {artists} ({duration_min}:{duration_sec:02d})")
        else:
            output.append("No tracklist available.")
        
        output.append(f"\n℗ {album_data['year']} {album_data['label']}")
        if album_data['available_countries']:
            output.append(f"Available in: {', '.join(album_data['available_countries'])}")
        output.append(f"Distributed by {album_data['major']}")
        
        return '\n'.join(output)


async def main():
    while True:
        try:
            album_input = input("Enter the Yandex Music album ID or URL: ").strip()

            if not album_input:
                print("Input cannot be empty. Please enter a valid album ID or URL.")
                continue

            if album_input.lower() in ['exit', 'quit', 'leave']:
                print("Exiting the program.")
                break

            if not re.match(r'^\d+$', album_input) and not re.match(r'^https?://', album_input):
                print("Invalid input. Please enter a valid album ID or URL.")
                continue

            token = "YOUR_TOKEN"

            fetcher = YandexMusicFetcher(token)
            album_id = fetcher.extract_album_id(album_input)
            album_data = await fetcher.fetch_album(album_id)
            print("\n" + fetcher.format_album_info(album_data))

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