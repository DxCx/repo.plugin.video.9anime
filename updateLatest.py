#!/usr/bin/python
import urllib2
import os
import json
import shutil
from zipfile import ZipFile

PLUGIN_NAME = "plugin.video.9anime"
TAGS_FEED_URL = "https://api.github.com/repos/DxCx/plugin.video.9anime/tags"

def fetchTags():
    resp = urllib2.urlopen(TAGS_FEED_URL)
    return json.loads(resp.read())

def downloadZip(url, targetPath):
    resp = urllib2.urlopen(url)
    with open(targetPath, 'wb') as f:
        f.write(resp.read())

def extractMeta(pluginPath, latestZip):
    extractFiles = {
        'addon.xml': pluginPath,
        'icon.png': os.path.join(pluginPath, 'resources'),
        'fanart.jpg': os.path.join(pluginPath, 'resources'),
    }
    filesLeft = extractFiles.keys()
    tmpDir = './tmp'
    os.mkdir(tmpDir)
    for dirName in extractFiles.values():
        if not os.path.exists(dirName):
            os.mkdir(dirName)

    z = ZipFile(latestZip)
    for f in z.namelist():
        for match in filesLeft:
            if f.endswith(match):
                z.extract(f, tmpDir)
                os.rename(os.path.join(tmpDir, f),
                          os.path.join(extractFiles[match], match))
                filesLeft.remove(match)
                break

        if not len(filesLeft):
            break

    shutil.rmtree(tmpDir)

def main():
    # Get latest tag
    tags = fetchTags()
    latest = tags[0]
    latestVersion = latest['name'][1:]

    # resolve zip path
    targetZip = "%s/%s-%s.zip" % (PLUGIN_NAME, PLUGIN_NAME, latestVersion)

    if os.path.isfile(targetZip):
        raise Exception('Already has latest')

    # Cleanup for the older versions
    # TODO: Just delete the whole directory and rebuild.
    shutil.rmtree(PLUGIN_NAME)
    os.mkdir(PLUGIN_NAME)

    # Download latest
    downloadZip(latest['zipball_url'], targetZip)

    # Extracts metadata
    extractMeta("./%s" % PLUGIN_NAME, targetZip)

    print latestVersion

if __name__ == "__main__":
    main()
