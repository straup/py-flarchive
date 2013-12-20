# py-flarchive

## What is this?

py-flarchive is a very simple Python library for archiving the metadata for the
Flickr photos for a user. For all a user's photos the library will try to
download and store the raw API output for the following methods:

* [flickr.photos.getInfo](http://www.flickr.com/services/api/flickr.photos.getInfo)
* [flickr.photos.getSizes](http://www.flickr.com/services/api/flickr.photos.getSizes)
* [flickr.photos.comments.getList](http://www.flickr.com/services/api/flickr.photos.comments.getList)
* [flickr.photos.getAllContexts]http://www.flickr.com/services/api/flickr.photos.getAllContexts)
* [flickr.photos.getExif](http://www.flickr.com/services/api/flickr.photos.getExif)

For example:

	INFO:root:process photo ID 11331441996
	DEBUG:root:calling flickr.photos.getInfo
	DEBUG:root:creating ./data/16870059@N04/113/314/419/96
	DEBUG:root:writing ./data/16870059@N04/113/314/419/96/11331441996-i.json
	DEBUG:root:calling flickr.photos.getExif
	DEBUG:root:writing ./data/16870059@N04/113/314/419/96/11331441996-e.json
	DEBUG:root:calling flickr.photos.getSizes
	DEBUG:root:writing ./data/16870059@N04/113/314/419/96/11331441996-s.json
	DEBUG:root:calling flickr.photos.getAllContexts
	DEBUG:root:writing ./data/16870059@N04/113/314/419/96/11331441996-ctx.json
	DEBUG:root:calling flickr.photos.comments.getList
	DEBUG:root:writing ./data/16870059@N04/113/314/419/96/11331441996-c.json

## Usage

	import flarchive

	apikey='1234567'
	authtoken=None
	datadir='/where/to/write/files'

	fl = flarchive.flickr(apikey, authtoken, datadir)
	fl.archive_user()        

Or you can just call the flarchive `__init__.py` library from the command line:

	$> python ./flarchive/__init__.py -v -a <APIKEY> -n <NSID> -d <DATA>

There are also a few helper `make` commands included with this with package:

	$> make user APIKEY=<APIKEY> NSID=<NSID>

	$> make list-commons APIKEY=<APIKEY>

## TO DO

* Pagination for photo comments
* Packaging, setup scripts and general spit and polish

## See also

* [Flickr.API](https://pypi.python.org/pypi/Flickr.API)
