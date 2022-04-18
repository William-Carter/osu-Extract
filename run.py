import getSongs
import generateMP3
songsDirectory = ""
outputDirectory = ""

songs, unused = getSongs.getSongs(songsDirectory)
print(f"{len(unused)} items were ignored")
for item in unused:
    print("\t", item)

songsLen = len(songs)
count = 1
for song in songs:
    print("(%s of %s) Generating %s" % (count, songsLen, song.folder))
    generateMP3.generateMP3(song, outputDirectory)
    count += 1

