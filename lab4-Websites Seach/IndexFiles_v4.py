#!/usr/bin/env python2
#coding=utf8
import sys, os
import jcc
import lucene
import threading, time
import urlparse
import codecs
from datetime import datetime

from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer
from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.analysis.core import WhitespaceAnalyzer

from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
"""
This class is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.IndexFiles.  It will take a directory as an argument
and will index all of the files in that directory and downward recursively.
It will index on the file path, the file name and the file contents.  The
resulting Lucene index will be placed in the current directory and called
'index'.
"""

class Ticker(object):

    def __init__(self):
        self.tick = True

    def run(self):
        while self.tick:
            sys.stdout.write('.')
            sys.stdout.flush()
            time.sleep(1.0)

class IndexFiles(object):
    """Usage: python IndexFiles <doc_directory>"""

    def __init__(self, root, storeDir, analyzer):

        if not os.path.exists(storeDir):
            os.mkdir(storeDir)
        store = SimpleFSDirectory(File(storeDir))

        analyzer = LimitTokenCountAnalyzer(analyzer, 1048576)
        config = IndexWriterConfig(Version.LUCENE_CURRENT, analyzer)
        config.setOpenMode(IndexWriterConfig.OpenMode.CREATE)

        writer = IndexWriter(store, config)

        self.indexDocs(root, writer)
        ticker = Ticker()
        print(  'optimizing index' ),
        threading.Thread(target=ticker.run).start()
        writer.commit()
        writer.close()
        ticker.tick = False
        print(  'done' )

    def indexDocs(self, root, writer):

        f = codecs.open('infoIndex.txt','r',encoding='utf-8')
        files = {}
        for line in f.xreadlines():
            ls = line.split()
            files[ls[0]+'.txt'] = [ls[1],ls[2]]
        f.close()

        for root, dirnames, filenames in os.walk(root):
            for filename in filenames:
                if not filename.endswith('.txt'):
                    continue
                print(  "adding" ), filename
                # try:
                path = os.path.join(root, filename)
                file = open(path)
                contents = unicode(file.read(), 'utf-8')
                file.close()
                doc = Document()
                doc.add(Field("name", filename,
                                     Field.Store.YES,
                                     Field.Index.NOT_ANALYZED))
                doc.add(Field("path", path,
                                     Field.Store.YES,
                                     Field.Index.NOT_ANALYZED))
                url = files[filename][0]
                doc.add(Field("url", url,
                                     Field.Store.YES,
                                     Field.Index.NOT_ANALYZED))
                domin = urlparse.urlsplit(url)[1].split(':')[0]
                doc.add(Field("site", domin,
                                     Field.Store.YES,
                                     Field.Index.NOT_ANALYZED))
                title = files[filename][1]
                doc.add(Field("title", title ,
                                     Field.Store.YES,
                                     Field.Index.NOT_ANALYZED))
                print filename,path,url,domin,title
                if len(contents) > 0:
                    doc.add(Field("contents", contents,
                                         Field.Store.NO,
                                         Field.Index.ANALYZED))
                else:
                    print ("warning: no content in %s" % filename)
                writer.addDocument(doc)
                # except Exception, e:
                    # print "Failed in indexDocs:", e

if __name__ == '__main__':
    lucene.initVM() #
    print 'lucene', lucene.VERSION

    if lucene.VERSION[0]<'4':
        print 'Please read the pdf. This program only supports Lucene 4.x'
        sys.exit(1) 
    start = datetime.now()
    IndexFiles('txt', "index_lucene", WhitespaceAnalyzer(Version.LUCENE_CURRENT))
    end = datetime.now()
    print end - start
