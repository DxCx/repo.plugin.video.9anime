#!/usr/bin/python2
import os
import shutil
import xml.etree.ElementTree as ET
import sys
from updateLatest import downloadZip, extractMeta

DEP_MAP = {
    "script.module.urlresolver":
    "https://github.com/tvaddonsco/script.module.urlresolver/archive/master.zip",
}

TEMP_DIR = "dep_temp"

def extractVersion(xmlPath):
    tree = ET.parse(xmlPath)
    root = tree.getroot()
    return root.attrib['version']

def procecss_dep(plugin_name, latest_zip):

    if os.path.isdir(TEMP_DIR):
        shutil.rmtree(TEMP_DIR)
    os.mkdir(TEMP_DIR)

    # resolve zip path
    tmpZip = "%s/master.zip" % (TEMP_DIR)

    downloadZip(latest_zip, tmpZip)
    extractMeta("./%s" % TEMP_DIR, tmpZip)

    # Get latest tag
    latestVersion = extractVersion("./%s/addon.xml" % TEMP_DIR)
    zipName = "%s-%s.zip" % (plugin_name, latestVersion)
    targetZip = os.path.join(plugin_name, zipName)

    if os.path.isfile(targetZip):
        shutil.rmtree(TEMP_DIR)
        print '%s Already has latest (%s)' % (plugin_name, latestVersion)
        return False

    os.rename(tmpZip, os.path.join(TEMP_DIR, zipName))
    shutil.rmtree(plugin_name)
    os.rename(TEMP_DIR, plugin_name)

    print 'Updated %s to latest (%s)' % (plugin_name, latestVersion)
    return True

def main():
    if not any([procecss_dep(plugin_name, latest_zip)
            for plugin_name, latest_zip in DEP_MAP.iteritems()]):
        # Nothing to do.
        return 0

    sys.path.append(os.path.join(os.path.split(__file__)[0], "kodi-addons"))
    from addons_xml_generator import Generator
    Generator()
    return 0

if __name__ == "__main__":
    main()

