import shutil
import os
from mutagen import File
from mutagen.mp3 import MP3
from mutagen.easyid3 import EasyID3
from mutagen.id3 import ID3, APIC, ID3NoHeaderError
import getAlbumArt
dirPath = os.path.dirname(os.path.realpath(__file__))
def generateMP3(songObject, outputFolder):
    filename = songObject.metadata["Artist"]+" - "+songObject.metadata["Title"]+".mp3"
    shutil.copy(songObject.mp3, outputFolder+"/"+filename)

    # Copy over metadata if it's missing from the mp3
    try:
        newAudio = EasyID3(outputFolder+"/"+filename)
    except ID3NoHeaderError:
        newAudio = File(outputFolder+"/"+filename, easy=True)
        newAudio.add_tags()

    try:
        newAudio["title"]
    except:
        newAudio["title"] = songObject.metadata["Title"]
    try:
        newAudio["artist"]
    except:
        newAudio["artist"] = songObject.metadata["Artist"]
    newAudio.save()

    newAudio = MP3(outputFolder+"/"+filename, ID3=ID3)
    if not hasAlbumArt(newAudio):
        if not songObject.metadata["Background"] == "":
            getAlbumArt.getAlbumArt(songObject)
            newAudio.tags.add(
                APIC(
                    encoding=3,
                    mime='image/jpeg',
                    type=3,
                    desc=u'Cover',
                    data=open(dirPath+"/temp/%s.jpg" % songObject.metadata["Title"], "rb").read()
                )
            )
            newAudio.save()
            os.remove(dirPath+"/temp/%s.jpg" % songObject.metadata["Title"])

    
def hasAlbumArt(audio):
    try: 
        x = audio.pictures
        if x:
            return True
    except Exception:
        pass  
    if 'covr' in audio or 'APIC:' in audio:
        return True
    return False
