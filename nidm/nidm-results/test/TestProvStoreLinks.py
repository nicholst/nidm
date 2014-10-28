#!/usr/bin/env python
'''Test thats link to example files on the Prov Store are up to date

@author: Camille Maumet <c.m.j.maumet@warwick.ac.uk>, Satrajit Ghosh
@copyright: University of Warwick 2014
'''
import unittest
from rdflib.graph import Graph
from TestCommons import *
import logging
import re

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

RELPATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

class TestProvStoreLinks(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestProvStoreLinks, self).__init__(*args, **kwargs)

        self.provstore_url = dict()
        self.ttl_from_provn_file_url = dict()
        self.ttl_file = dict()
        for example_file in example_filenames:
            # Read provn
            provn_file = os.path.join(RELPATH, example_file)
            # Get corresponding turtle            
            ttl_from_provn_file_url = get_turtle(provn_file)
            self.ttl_from_provn_file_url[example_file] = ttl_from_provn_file_url
            self.ttl_file[example_file] = provn_file.replace(".provn", ".ttl")

            # Read README
            readme_file = os.path.join(RELPATH, os.path.dirname(example_file), 'README.md')
            readme_fid = open(readme_file)
            readme_txt = readme_fid.read()
            readme_fid.close()
            provstore_url_index = re.search("https://provenance.ecs.soton.ac.uk/store/documents/[^/]*/", readme_txt)
            # Get corresponding turtle on Prov Store            
            if provstore_url_index:
                provstore_url = readme_txt[provstore_url_index.start():provstore_url_index.end()-1]+".ttl"
            else:
                provstore_url = None

            # Save URL to Prov Store document
            self.provstore_url[example_file] = provstore_url        

    def setUp(self):
        logger.info("Test: TestProvStoreLinks")

    def test_provstore_links(self):
        error_msg = list()

        for example_file in example_filenames:
            
            if self.provstore_url[example_file]:
                logger.info('\tProv store URL: '+self.provstore_url[example_file])
                found_difference = compare_ttl_documents(self.ttl_from_provn_file_url[example_file], self.provstore_url[example_file], True)

                if found_difference:
                    error_msg.append(example_file+": Prov store link outdated, please update README.md using nidm/nidm-results/scripts/UpdateExampleReadmes.py")
            else:
                error_msg.append(example_file+': No document URL found in README.')

            if self.ttl_file[example_file]:
                if os.path.isfile(self.ttl_file[example_file]):
                    found_difference = compare_ttl_documents(self.ttl_from_provn_file_url[example_file], self.ttl_file[example_file], True)

                    if found_difference:
                        error_msg.append(example_file+": Turtle file outdated, please update using nidm/nidm-results/scripts/UpdateExampleReadmes.py")
                else:
                    error_msg.append(example_file+": No turtle file.")
            else:
                error_msg.append(example_file+': No turle file.')

        # Raise errors
        if error_msg:
            raise Exception("\n".join(error_msg))

if __name__ == '__main__':
    unittest.main()
