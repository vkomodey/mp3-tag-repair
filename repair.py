# -*- coding: utf-8 -*-
import os

TAGS_FILENAME = 'tags.info'
BROKEN_TAGS_FILENAME = 'broken-tags.info'


def russian_alphabet():
    alph = []
    FIRST_RUSSIAN_SYMBOL_CODE = 1040
    LAST_RUSSIAL_SYMBOL_CODE = 1104

    return [chr(i) for i in range(FIRST_RUSSIAN_SYMBOL_CODE, LAST_RUSSIAL_SYMBOL_CODE)]


rus_alph = russian_alphabet()

def is_russian(string):
    encoded = bytes(string, 'utf-8').decode('utf-8')

    for symbol in rus_alph:
        if symbol in encoded:
            return True
    
    return False


def read_tags(filename):
    tag_file = open(filename)
    song_tags = [];
    current_song = {}
    prev_line = ""

    for line in tag_file:
        if prev_line == "\n":
            song_tags.append(current_song)
            current_song = {}
        if line != "\n":
            splitted = line.split(": ")
            current_song[splitted[0]] = splitted[1]
        prev_line = line
    tag_file.close()

    return song_tags

def write_broken(filename, broken_songs):
    file = open(filename, 'a')

    for song in broken_songs:
        file.write(song["File"])

    file.close()


def generate_tags(filename):
    os.system("id3 '*.mp3' > {}".format(filename))

def replace_tags(fname):
    # Delete all corrupted tags
    os.system("cat {} | xargs -I % id3 -d '%'".format(fname))
    # Add new title tag which is equal to filename
    os.system("cat {} | xargs -I % id3 -2 -t '%' '%'".format(fname))

def clear_outputs(*args):
    for filename in args:
        if os.path.isfile(filename):
            os.remove(filename)

def get_broken(songs):
    broken = []
    TITLE = "Title"
    ARTIST = "Artist"
    ALBUM = "Album"
    GENRE = "Genre"
    FILENAME = "File"

    for song in songs:
        cond1 = TITLE in song and not is_russian(song[TITLE])
        cond2 = ARTIST in song and not is_russian(song[ARTIST])
        cond3 = ALBUM in song  and not is_russian(song[ALBUM])
        cond4 = GENRE in song and not is_russian(song[GENRE])

        if cond1 or cond2 or cond3 or cond4:
            broken.append(song)

    return broken

generate_tags(TAGS_FILENAME)
all_songs = read_tags(TAGS_FILENAME)
broken_songs = get_broken(all_songs)
write_broken(BROKEN_TAGS_FILENAME, broken_songs)
replace_tags(BROKEN_TAGS_FILENAME)
clear_outputs(TAGS_FILENAME, BROKEN_TAGS_FILENAME)

print("Len of broken songs = {}".format(len(broken_songs)))
