#!/bin/bash
OLD_PLUGIN=plugin.video.9anime
PLUGIN=plugin.video.wonderfulsubs

function update() {
	local ADDON=$1
	local NEW_VERSION

	git checkout master
	git remote update origin
	git reset --hard origin/master

	if ! NEW_VERSION=$(python2 updateLatest.py ${ADDON}); then
		return;
	fi

	local BRANCH_NAME=version-${ADDON}-${NEW_VERSION}

	git checkout -b ${BRANCH_NAME}
	python2 kodi-addons/addons_xml_generator.py
	git add ${ADDON}
	git add addons.xml
	git add addons.xml.md5

	git commit -m "chore(addons): update ${ADDON} to version ${NEW_VERSION}"
	git push -u origin ${BRANCH_NAME}
	git checkout master

	echo "Done: https://github.com/DxCx/repo.plugin.video.9anime/compare/${BRANCH_NAME}?expand=1"
	exit 0
}

update ${OLD_PLUGIN}
update ${PLUGIN}
exit 1
