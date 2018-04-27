#!/usr/bin/python2
import os
import shutil
import xml.etree.ElementTree as ET
import sys
from updateLatest import downloadZip, extractMeta

TEMP_DIR = "urlresolver_tmp"
PLUGIN_NAME = "script.module.urlresolver"
LATEST_ZIP = "https://github.com/tvaddonsco/script.module.urlresolver/archive/master.zip"

def extractVersion(xmlPath):
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    return root.attrib['version']

def main():

    if os.path.isdir(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.mkdir(TEMP_DIR)

    # resolve zip path
    tmpZip = "%s/master.zip" % (TEMP_DIR)

    downloadZip(LATEST_ZIP, tmpZip)
    extractMeta("./%s" % TEMP_DIR, tmpZip)

    # Get latest tag
    latestVersion = extractVersion("./%s/addon.xml" % TEMP_DIR)
    zipName = "%s-%s.zip" % (PLUGIN_NAME, latestVersion)
    targetZip = os.path.join(PLUGIN_NAME, zipName)

    if os.path.isfile(targetZip):
        shutil.rmtree(TEMP_DIR)
        print 'Already has latest (%s)' % (latestVersion)
        return 0

    os.rename(tmpZip, os.path.join(TEMP_DIR, zipName))
    shutil.rmtree(PLUGIN_NAME)
    os.rename(TEMP_DIR, PLUGIN_NAME)

    print 'Updated to latest (%s)' % latestVersion

    sys.path.append(os.path.join(os.path.split(__file__)[0], "kodi-addons"))
    from addons_xml_generator import Generator
    Generator()
    return 0

if __name__ == "__main__":
    main()

