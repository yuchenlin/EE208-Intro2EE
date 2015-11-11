#!/usr/bin/env python2
#coding=utf8
import sys, os
import jcc
import lucene
import threading, time
import urlparse
import codecs
from datetime import datetime

from lucene import QueryParser,\
                   IndexSearcher,\
                   WhitespaceAnalyzer,IndexWriter,\
                   SimpleFSDirectory,\
                   File, VERSION,\
                   initVM, Version,Document,Field,\
                   BooleanQuery,\
                   BooleanClause,LimitTokenCountAnalyzer,IndexWriterConfig,\
                   Term, WildcardQuery

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

        f = codecs.open('picIndex.txt','r',encoding='utf-8')
        picDict = {}
        for line in f.xreadlines():
            ls = line.split('seg^*')
            url = ls[0]
            title = ls[1] 
            src = ls[2]
            alt = ls[3]
            picDict[src] = [url,title,alt]
        f.close()
        for src in picDict:
            doc = Document()
            doc.add(Field("src", src,
                                 Field.Store.YES,
                                 Field.Index.NOT_ANALYZED))
            doc.add(Field("url", picDict[src][0],
                                 Field.Store.YES,
                                 Field.Index.NOT_ANALYZED))
            doc.add(Field("title", picDict[src][1],
                                 Field.Store.YES,
                                 Field.Index.NOT_ANALYZED))
            doc.add(Field("alt", picDict[src][2],
                                 Field.Store.YES,
                                 Field.Index.ANALYZED))
            writer.addDocument(doc)
if __name__ == '__main__': 
    lucene.initVM(vmargs=['-Djava.awt.headless=true'])

    print 'lucene', lucene.VERSION
    start = datetime.now()
    IndexFiles('txt', "image_index_v3", WhitespaceAnalyzer(Version.LUCENE_CURRENT))
    end = datetime.now()
    print end - start
