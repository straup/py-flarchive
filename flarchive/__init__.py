#!/usr/bin/env python

import sys
import os
import os.path
import Flickr.API
import json
import logging
import pprint

class flickr:

    def __init__ (self, apikey, authtoken, datadir):

        self.api = Flickr.API.API(apikey, authtoken)
        self.datadir = datadir

        self.meta = {
            'i': 'flickr.photos.getInfo',
            's': 'flickr.photos.getSizes',
            'c': 'flickr.photos.comments.getList',
            'ctx': 'flickr.photos.getAllContexts',
            'e': 'flickr.photos.getExif',
        }

    def archive_user(self, nsid):

        logging.debug("archive %s" % nsid)

        method = 'flickr.photos.search'

        args = {
            'user_id': nsid,
        }
        
        pages = None
        total = None
        page = 1

        # TO DO: check to see if this is hitting Vepsa and the 4K limit

        while not pages or page <= pages:

            args['page'] = page
            # args['per_page'] = 1

            try:
                rsp = self.api_call(method, args)
            except Exception, e:
                logging.error("failed to call %s: %s" % (method, e))

            if not pages:
                pages = rsp['photos']['pages']
                total = rsp['photos']['total']

                logging.debug("%s photos (%s pages) for %s" % (total, pages, nsid))

            for ph in rsp['photos']['photo']:
                self.archive_photo(ph)

            page += 1

    def archive_photo(self, ph):

        logging.info("process photo ID %s" % ph['id'])

        paths = {}
        meta = {}
        
        for suffix, method in self.meta.items():

            fname = "%s-%s.json" % (ph['id'], suffix)

            safedirs = self.id2safedirs(ph['id'])
            root = os.path.join(self.datadir, ph['owner'], *safedirs)
            
            path = os.path.join(root, fname)

            if not os.path.exists(path):
                paths[suffix] = path
                meta[suffix] = method

        if len(meta.keys()) == 0:
            logging.info("all meta files for photo ID %s have been collected" % ph['id'])
            return

        logging.debug("fetch meta for %s" % ", ".join(meta.values()))

        for details in self.fetch_meta(ph, meta):

            suffix, meta = details

            path = paths[suffix]
            root = os.path.dirname(path)
            
            if not os.path.exists(root):
                logging.debug("creating %s" % root)
                os.makedirs(root)

            logging.debug("writing %s" % path)

            fh = open(path, 'w')
            json.dump(meta, fh)

    # NOTE: this yields its results rather than returning a single list

    def fetch_meta(self, ph, what):

        # TO DO: pagination on comments

        photo_id = ph['id']
        
        args = {
            'photo_id': photo_id
        }
        
        for suffix, method in what.items():

            try:
                rsp = self.api_call(method, args)
            except Exception, e:
                logging.error("failed to call %s: %s" % (method, e))
                continue

            yield (suffix, rsp)

    def api_call(self, method, args):

        logging.debug("calling %s" % method)

        args['method'] = method
        args['format'] = 'json'
        args['nojsoncallback'] = 1

        rsp = self.api.execute_method(method=method, args=args, sign=False)
        return json.load(rsp)

    def id2safedirs(self, id):

        tmp = str(id)
        parts = []

        while len(tmp) > 3:
            parts.append(tmp[0:3])
            tmp = tmp[3:]

        if len(tmp):
            parts.append(tmp)

        return parts

class commons(flickr):

    def commons_institutions(self):

        method = 'flickr.commons.getInstitutions'
        args = {}

        try:
            rsp = self.api_call(method, args)
        except Except, e:
            logging.error("Yahoo says NO: %s" % e)
            return None

        commons = {}

        for inst in rsp['institutions']['institution']:
            name = inst['name']['_content']
            nsid = inst['nsid']

            commons[nsid] = name

        return commons

    def list_commons(self):

        commons = self.commons_institutions()

        if not commons:
            return False

        for nsid, name in commons.items():
            print "%s\t%s" % (nsid, name)

    def archive_commons(self):

        commons = self.commons_institutions()

        if not commons:
            return False

        for nsid, name in commons.items():

            logging.debug("archive %s (%s)" % (name, nsid))
            self.archive_user(nsid)
    
if __name__ == '__main__':

    import optparse

    parser = optparse.OptionParser()

    parser.add_option('-a', '--api-key', dest='apikey', action='store', help='A valid Flickr API key')
    parser.add_option('--commons', dest='commons', action='store_true', default=False, help='...')
    parser.add_option('-l', '--list', dest='list', action='store_true', default=False, help='...')
    parser.add_option('-n', '--nsid', dest='nsid', action='store', default=None, help='...')
    parser.add_option('-d', '--data', dest='datadir', action='store', default=None, help='...')
    parser.add_option('-v', '--verbose', dest='verbose', action='store_true', default=False, help='be chatty (default is false)')
                
    options, args = parser.parse_args()

    if options.verbose:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.INFO)

    # TO DO: lookup user (nsid) by username

    # Commons specific stuff

    if options.commons:

        cm = commons(options.apikey, None, options.datadir)

        if options.list:
            cm.list_commons()
            sys.exit()

        if not options.datadir:
            logging.error("You forgot to specify a data directory")
            sys.exit()

        if options.nsid:
            cm.archive_user(options.nsid)    
        else:
            cm.archive_commons()                          

        sys.exit()

    # Any old user

    if not options.nsid:
        logging.error("You forgot to specify a user ID")
        sys.exit()

    if not options.datadir:
        logging.error("You forgot to specify a data directory")
        sys.exit()

    fl = flickr(options.apikey, None, options.datadir)
    fl.archive_user(options.nsid)
    sys.exit()
