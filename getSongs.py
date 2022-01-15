import os
from sys import maxsize

class Song:
    def __init__(self, songFolder):
        if self.Useable(songFolder):
            self.folder = songFolder
            self.mdFile = self.getMetadata(self.folder)
            self.metadata = self.parseMetaData(self.mdFile)
            self.mp3 = self.getMp3(self.folder)
            self.unuseable = False
        else:
            self.unuseable = True

    def Useable(self, folder):
        useable = True
        osucount = 0
        mp3count = 0
        for item in os.listdir(folder):
            if ".osu" in item:
                osucount += 1
            if ".mp3" in item:
                mp3count += 1
        if osucount == 0:
            useable = False
        if mp3count == 0:
            useable = False

        return useable

    

    
    def getMetadata(self, folder):
        items = os.listdir(folder)
        osus = []

        # Get all the files that end in mp3
        for item in items:
            splitItem = item.split(".")
            if splitItem[-1] == "osu":
                osus.append(item)

        

        return folder+"/"+osus[0]


    def parseMetaData(self, mdFile):
        metaData = {}
        with open(mdFile, "r", encoding='utf8') as f:
            raw = f.read()

        l1 = raw.split("[General]\n")[1].split("\n")[0].split(": ")
        metaData[l1[0]] = l1[1]
        
        # This is a monstrous bit of code, it grabs everything from between the Metadata and Difficulty tags
        l2 = raw.split("[Metadata]\n")[1].split("\n[Difficulty]")[0].split("\n")
        
        for item in l2:
            pair = item.split(":")
            if len(pair) > 1:
                metaData[pair[0]] = pair[1]
            else:
                metaData[pair[0]] = ""



        

        # These are illegal characters in windows filenames, but might be present in the .osu file
        for item in metaData.keys():
            metaData[item] = metaData[item].replace("\\", "-")
            metaData[item] = metaData[item].replace("/", "-")
            metaData[item] = metaData[item].replace(":", "-")
            metaData[item] = metaData[item].replace("*", "-")
            metaData[item] = metaData[item].replace("?", "-")
            metaData[item] = metaData[item].replace("\"", "-")
            metaData[item] = metaData[item].replace("<", "-")
            metaData[item] = metaData[item].replace(">", "-")
            metaData[item] = metaData[item].replace("|", "-")

        try:
            l3 = raw.split("[Events]\n")[1].split("0,0,")[1].split("\"")[1]
            metaData["Background"] = self.folder+"/"+l3
        except IndexError:
            metaData["Background"] = ""
        


        return metaData


    def getMp3(self, folder):
        return folder+"/"+self.metadata["AudioFilename"]

def getSongs(songsFolder):
    songs = []
    many = len(os.listdir(songsFolder))
    count = 1
    for item in os.listdir(songsFolder):

        print("(%s of %s) Viewing %s" % (count, many, item))
        if not os.path.isfile(item):
            workingSong = Song(songsFolder+"/"+item)
            if not workingSong.unuseable:
                songs.append(workingSong)
        count += 1


    return songs

