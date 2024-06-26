from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TPE1, TALB, TIT2, error
import os

def get_mp3_files(directory):
    mp3_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.mp3'):
                mp3_files.append(os.path.join(root, file))
    return mp3_files

def main(directory, album, cover_artist):
    mp3_files = get_mp3_files(directory)
    album_cover = os.path.join(directory, "cover.png")
    for mp3_file in mp3_files:
        audio = MP3(mp3_file, ID3=ID3)

        # adding ID3 tag if it is not present
        try:
            audio.add_tags()
        except error:
            pass

        audio.tags.add(APIC(mime='image/png', type=3, desc=u'Cover', data=open(album_cover, 'rb').read()))
        audio.tags.add(TPE1(encoding=3, text=cover_artist))
        audio.tags.add(TALB(encoding=3, text=album))
        audio.tags.add(TIT2(encoding=3, text=os.path.basename(mp3_file)[:-4]))  # Add song title
        audio.save(v2_version=3, v1=2)
        print("Added album cover, artist, album, and title to " + mp3_file)

if __name__ == "__main__":
    directory = input("Enter the directory of the mp3 files (it will be the album name too): ")
    cover_artist = input("Enter the cover artist name: ")
    main(directory, directory, cover_artist)