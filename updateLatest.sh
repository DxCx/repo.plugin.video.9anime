#!/bin/bash
set -e

git checkout master
git remote update origin
git reset --hard origin/master

NEW_VERSION=`python updateLatest.py`
BRANCH_NAME=version-${NEW_VERSION}

git checkout -b ${BRANCH_NAME}
python kodi-addons/addons_xml_generator.py
git add plugin.video.9anime
git add addons.xml
git add addons.xml.md5

git commit -m "chore(addons): update plugin.video.9anime to version ${NEW_VERSION}"
git push -u origin ${BRANCH_NAME}
git checkout master
echo "Done: https://github.com/DxCx/repo.plugin.video.9anime/compare/${BRANCH_NAME}?expand=1"
