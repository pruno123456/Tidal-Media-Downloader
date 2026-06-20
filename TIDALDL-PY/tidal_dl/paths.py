#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
@File    :  paths.py
@Date    :  2022/06/10
@Author  :  Yaronzz
@Version :  1.0
@Contact :  yaronhuang@foxmail.com
@Desc    :
"""
import os
import aigpy
import datetime

from tidal import *
from settings import *


def __fixPath__(name: str):
    return aigpy.path.replaceLimitChar(name, '-').strip()


def __getYear__(releaseDate: str):
    if releaseDate is None or releaseDate == '':
        return ''
    return aigpy.string.getSubOnlyEnd(releaseDate, '-')


def __getDurationStr__(seconds):
    time_string = str(datetime.timedelta(seconds=seconds))
    if time_string.startswith('0:'):
        time_string = time_string[2:]
    return time_string


def __getExtension__(stream: StreamUrl):
    if '.flac' in stream.url:
        return '.flac'
    if '.mp4' in stream.url:
        if 'ac4' in stream.codec or 'mha1' in stream.codec:
            return '.mp4'
        elif 'flac' in stream.codec:
            return '.flac'
        return '.m4a'
    return '.m4a'


def getAlbumPath(album):
    artistName = __fixPath__(TIDAL_API.getArtistsName(album.artists))
    albumArtistName = __fixPath__(album.artist.name) if album.artist is not None else ""

    # album folder pre: [ME]
    flag = TIDAL_API.getFlag(album, Type.Album, True, "")
    if SETTINGS.audioQuality != AudioQuality.Master and SETTINGS.audioQuality != AudioQuality.Max:
        flag = flag.replace("M", "")
    if flag != "":
        flag = "[" + flag + "] "

    # album and addyear
    albumName = __fixPath__(album.title)
    year = __getYear__(album.releaseDate)

    # retpath
    retpath = SETTINGS.albumFolderFormat
    if retpath is None or len(retpath) <= 0:
        retpath = SETTINGS.getDefaultAlbumFolderFormat()
    retpath = retpath.replace(R"{ArtistName}", artistName)
    retpath = retpath.replace(R"{AlbumArtistName}", albumArtistName)
    retpath = retpath.replace(R"{Flag}", flag)
    retpath = retpath.replace(R"{AlbumID}", str(album.id))
    retpath = retpath.replace(R"{AlbumYear}", year)
    retpath = retpath.replace(R"{AlbumTitle}", albumName)
    retpath = retpath.replace(R"{AudioQuality}", album.audioQuality)
    retpath = retpath.replace(R"{DurationSeconds}", str(album.duration))
    retpath = retpath.replace(R"{Duration}", __getDurationStr__(album.duration))
    retpath = retpath.replace(R"{NumberOfTracks}", str(album.numberOfTracks))
    retpath = retpath.replace(R"{NumberOfVideos}", str(album.numberOfVideos))
    retpath = retpath.replace(R"{NumberOfVolumes}", str(album.numberOfVolumes))
    retpath = retpath.replace(R"{ReleaseDate}", str(album.releaseDate))
    retpath = retpath.replace(R"{RecordType}", album.type)
    retpath = retpath.replace(R"{None}", "")
    retpath = retpath.strip()
    return f"{SETTINGS.downloadPath}/{retpath}"

def getPlaylistPath(playlist):
    playlistName = __fixPath__(playlist.title)

    # retpath
    retpath = SETTINGS.playlistFolderFormat
    if retpath is None or len(retpath) <= 0:
        retpath = SETTINGS.getDefaultPlaylistFolderFormat()
    retpath = retpath.replace(R"{PlaylistUUID}", str(playlist.uuid))
    retpath = retpath.replace(R"{PlaylistName}", playlistName)
    return f"{SETTINGS.downloadPath}/{retpath}"


def getTaggedCollectionBasePath(track):
    artist = __fixPath__(track.artist.name) if track.artist is not None else __fixPath__(TIDAL_API.getArtistsName(track.artists))

    title = __fixPath__(track.title)
    if not aigpy.string.isNull(track.version):
        title += f' ({__fixPath__(track.version)})'

    album = __fixPath__(track.album.title) if track.album is not None else ''

    return f"/Users/oli/Music/Tagged Collection/{artist}/{title} - {album}"


def getTrackPathNoExt(track, album=None, playlist=None):
    return getTaggedCollectionBasePath(track)


def getTrackPath(track, stream, album=None, playlist=None):
    extension = __getExtension__(stream)
    return getTaggedCollectionBasePath(track) + extension


def getVideoPath(video, album=None, playlist=None):
    base = SETTINGS.downloadPath + '/Video/'
    if album is not None and album.title is not None:
        base = getAlbumPath(album)
    elif playlist is not None:
        base = getPlaylistPath(playlist)

    # get number
    number = str(video.trackNumber).rjust(2, '0')

    # get artist
    artists = __fixPath__(TIDAL_API.getArtistsName(video.artists))
    artist = __fixPath__(video.artist.name) if video.artist is not None else ""

    # explicit
    explicit = "(Explicit)" if video.explicit else ''

    # title and year and extension
    title = __fixPath__(video.title)
    year = __getYear__(video.releaseDate)
    extension = ".mp4"

    retpath = SETTINGS.videoFileFormat
    if retpath is None or len(retpath) <= 0:
        retpath = SETTINGS.getDefaultVideoFileFormat()
    retpath = retpath.replace(R"{VideoNumber}", number)
    retpath = retpath.replace(R"{ArtistName}", artist)
    retpath = retpath.replace(R"{ArtistsName}", artists)
    retpath = retpath.replace(R"{VideoTitle}", title)
    retpath = retpath.replace(R"{ExplicitFlag}", explicit)
    retpath = retpath.replace(R"{VideoYear}", year)
    retpath = retpath.replace(R"{VideoID}", str(video.id))
    retpath = retpath.strip()
    return f"{base}/{retpath}{extension}"


def __getHomePath__():
    if "XDG_CONFIG_HOME" in os.environ:
        return os.environ['XDG_CONFIG_HOME']
    elif "HOME" in os.environ:
        return os.environ['HOME']
    elif "HOMEDRIVE" in os.environ and "HOMEPATH" in os.environ:
        return os.environ['HOMEDRIVE'] + os.environ['HOMEPATH']
    else:
        return os.path.abspath("./")

def getLogPath():
    return __getHomePath__() + '/.tidal-dl.log'

def getTokenPath():
    return __getHomePath__() + '/.tidal-dl.token.json'

def getProfilePath():
    return __getHomePath__() + '/.tidal-dl.json'
