* Any changes in `/addons.xml` require a recalculation of the md5 hash if this file stored in `/addons.xml.md5` (otherwise the repository updates wont get visible in kodi)
* To add a new version of 9anime, store the zip archiv as `/plugin.video.9anime/plugin.video.9anime-x.x.x.zip` where x is the version number
	* If the version number of the `/addons.xml` is less the version of the plugin itself (the addons.xml in the plugins archiv), kodi will always show an available update despite having installed the latest
* To update the repository itself (new links or other addons), increment the version number in `/addons.xml` and in `/repo.plugin.video.9anime/addon.xml` equally (attention: in / the file is called addon**s**.xml and in /repo.plugin.video.9anime/ its addon.xml without the **s** )
