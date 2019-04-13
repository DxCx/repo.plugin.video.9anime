#!/usr/bin/python2
import urllib2
import os
import json
import shutil
import sys
from zipfile import ZipFile

TAGS_FEED_URL = lambda p: "https://api.github.com/repos/DxCx/%s/tags" % p

def fetchTags(pluginName):
    resp = urllib2.urlopen(TAGS_FEED_URL(pluginName))
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

def main(pluginName):
    # Get latest tag
    tags = fetchTags(pluginName)
    latest = tags[0]
    latestVersion = latest['name'][1:]

    # resolve zip path
    targetZip = "%s/%s-%s.zip" % (pluginName, pluginName, latestVersion)

    if os.path.isfile(targetZip):
        raise Exception('Already has latest')

    # Cleanup for the older versions
    # TODO: Just delete the whole directory and rebuild.
    if os.path.isdir(pluginName):
        shutil.rmtree(pluginName)
    os.mkdir(pluginName)

    # Download latest
    downloadZip(latest['zipball_url'], targetZip)

    # Extracts metadata
    extractMeta("./%s" % pluginName, targetZip)

    print latestVersion

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print "Usage: %s <Plugin name>" % sys.argv[0]
        sys.exit(1)

    main(sys.argv[1])
    sys.exit(0)
