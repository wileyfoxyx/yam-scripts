import requests
import json

def get_top_artists():
    # Try multiple possible endpoints
    endpoints = [
        'https://api.music.yandex.net/personal/top/artists/month',
        'https://api.music.yandex.net/personal/top/artists',
        'https://api.music.yandex.net/users/me/top/artists'
    ]
    
    # Prompt user for their OAuth token
    token = input("Please enter your OAuth token: ")
    
    # Set up headers with user's token
    headers = {
        'Authorization': f'OAuth {token}',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for url in endpoints:
        try:
            response = requests.get(url, headers=headers)
            
            # Check if request was successful
            if response.status_code == 200:
                # Parse JSON response
                data = response.json()
                
                # Check if we got actual data
                if data and (data.get('result') or data.get('artists') or data.get('data')):
                    return data
                else:
                    continue
            else:
                continue
                
        except requests.exceptions.RequestException as e:
            continue
    
    return None

def main():
    # Get top artists
    top_artists = get_top_artists()
    
    # Process the response
    if top_artists:
        # Try different possible response structures
        artists_data = None
        if 'result' in top_artists:
            if isinstance(top_artists['result'], list):
                artists_data = top_artists['result']
            elif 'artists' in top_artists['result']:
                artists_data = top_artists['result']['artists']
            elif 'items' in top_artists['result']:
                artists_data = top_artists['result']['items']
        elif 'artists' in top_artists:
            artists_data = top_artists['artists']
        elif 'data' in top_artists:
            artists_data = top_artists['data']
        elif isinstance(top_artists, list):
            artists_data = top_artists
        
        if artists_data:
            print("Your top artists this month:")
            for i, artist in enumerate(artists_data[:10]):  # Limit to top 10
                # Handle different artist object structures
                if isinstance(artist, dict):
                    name = artist.get('name') or artist.get('title') or artist.get('artist', {}).get('name', 'Unknown')
                    plays = artist.get('playCount') or artist.get('plays') or ''
                    print(f"{i+1}. {name} {f'({plays} plays)' if plays else ''}")
                else:
                    print(f"{i+1}. {artist}")
        else:
            print("Could not find artists data in response structure")
    else:
        print("Failed to get top artists data")

if __name__ == "__main__":
    main()