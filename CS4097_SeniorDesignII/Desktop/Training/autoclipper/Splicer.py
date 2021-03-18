#!/usr/bin/env python3
#Splicing Imports
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from random import choice
import argparse
#Tag Detection Imports
from PIL import Image
import cv2 as cv

CHARACTERS = [
    "Bowser",
    "Bowser Jr.",
    "Captain Falcon",
    "Chrom",
    "Cloud",
    "Corrin",
    "Daisy",
    "Dark Pit",
    "Dark Samus",
    "Diddy Kong",
    "Donkey Kong",
    "Dr. Mario",
    "Duck Hunt",
    "Falco",
    "Fox",
    "Ganondorf",
    "Greninja",
    "Hero",
    "Ice Climbers",
    "Ike",
    "Incineroar",
    "Inkling",
    "Isabelle",
    "Jigglypuff",
    "Joker",
    "Ken",
    "King Dedede",
    "King K. Rool",
    "Kirby",
    "Link",
    "Little Mac",
    "Lucario",
    "Lucas",
    "Lucina",
    "Luigi",
    "Mario",
    "Marth",
    "Mega Man",
    "Meta Knight",
    "Mewtwo",
    "Ness",
    "Olimar",
    "Pac-Man",
    "Palutena",
    "Peach",
    "Pichu",
    "Pikachu",
    "Pirahna Plant",
    "Pit",
    "Pkemon Trainer",
    #"Rob",
    "Richter",
    "Ridley",
    "Robin",
    #"Rosalina",
    "Roy",
    "Ryu",
    "Samus",
    "Sheik",
    "Shulk",
    "Simon",
    "Snake",
    "Sonic",
    "Toon Link",
    "Villager",
    "Wario",
    "Wolf",
    "Yoshi",
    "Young Link",
    "Zelda",
    "Zero Suit Samus"
]

def convertToSeconds(time):
    hours, minutes, seconds = [int(res) for res in time.split(':')]
    return ((hours * 3600) + (minutes * 60) + seconds)

def loadTimeline(filename=''):
    times = []
    names = []
    with open(filename, 'r') as f:
        for line in f.readlines():
            line = line.strip('\n')
            times.append(line.split(';')[0:2])
            names.append(line.split(';')[2:])
    return times, names

def splice(timelineFile, vodFile, outputDir):
    timeline, names = loadTimeline(timelineFile)
    for i, time in enumerate(timeline):
        start_time, end_time = time
        start_time = convertToSeconds(start_time)
        end_time = convertToSeconds(end_time)
        player_one, player_two = names[i]
        char_one = choice(CHARACTERS)
        char_two = choice(CHARACTERS)
        title = '%s_(%s)_vs_%s_(%s).mp4' % (player_one, char_one, player_two, char_two)
        ffmpeg_extract_subclip(args.input, int(start_time), int(end_time), targetname=args.output + title)
        print("Creating Match: %s -- From Vod: Potato Reads #9" % title.replace('_', ' '))

def main():
    pass 
if __name__== "__main__":
    main()
