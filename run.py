import getSongs
import generateMP3
songsDirectory = "D:\\Downloads\\osu!\\Songs"
outputDirectory = "D:\\osuSongsExtract\\out"

songs = getSongs.getSongs(songsDirectory)
for song in songs:
    print("Generating %s" % song.folder)
    generateMP3.generateMP3(song, outputDirectory)


    