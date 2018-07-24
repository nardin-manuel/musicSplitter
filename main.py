#import eyed3
from pydub import AudioSegment
import argparse
import os
import gc

def parseFile(filePath, delimiter, numberOfDelimiters=2):
	songList=[dict(zip(['startTime', 'artist', 'title'], line.strip().split(delimiter, numberOfDelimiters))) for line in open(filePath,'r')]
	for i in range(len(songList)-1):
		songList[i]['stopTime']=songList[i+1]['startTime']
	return songList
		
		

#################MAIN#########

parser=argparse.ArgumentParser()
parser.add_argument("inputMusicFile", help="Big file with long downloaded music")
parser.add_argument("inputTextFile", help="File where music titled is indexed. Format: {StartTime} - {Title} - {Artist}")
parser.add_argument("outputFolder", help="Folder where single songs will saved. If the folder does not exist it will be created automatically")
parser.add_argument("-d", "--delimiter", help="Delimiter between attributes")
args=parser.parse_args()
songList=parseFile(os.path.abspath(args.inputTextFile), args.delimiter)

print("Audio file is loading...")
compilation=AudioSegment.from_mp3(os.path.abspath(args.inputMusicFile))
print("Audio file imported...")

for songInfo in songList:
	
	millisecondStart=sum(int(x) * 60 ** i for i,x in enumerate(reversed(songInfo['startTime'].split(":"))))*1000
	if 'stopTime' in songInfo:
		millisecondStop=sum(int(x) * 60 ** i for i,x in enumerate(reversed(songInfo['stopTime'].split(":"))))*1000
		song=compilation[millisecondStart:millisecondStop]
		print("Stop time found")
	else:
		song=compilation[millisecondStart:]
		print("stop time not found!")
	print("songInfo export")
	print(os.path.join(os.path.abspath(args.outputFolder), songInfo['title'])+".mp3")
	song.export(os.path.join(os.path.abspath(args.outputFolder), songInfo['title']+'.mp3'), bitrate="192k", format="mp3", tags={key:songInfo[key] for key in['artist','title']})
	#song.export("test.mp3",format="mp3")
	
	del songInfo
	gc.collect()
	
