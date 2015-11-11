#!/usr/bin/env python
#coding=utf8
import sys
import jcc
from lucene import initVM,VERSION
from java.io import File
from org.apache.lucene.analysis.miscellaneous import LimitTokenCountAnalyzer

from org.apache.lucene.analysis.standard import StandardAnalyzer
from org.apache.lucene.document import Document, Field, FieldType
from org.apache.lucene.index import FieldInfo, IndexWriter, IndexWriterConfig,Term
from org.apache.lucene.store import SimpleFSDirectory
from org.apache.lucene.util import Version
from org.apache.lucene.search import IndexSearcher
from org.apache.lucene.index import DirectoryReader
from org.apache.lucene.queryparser.classic import QueryParser
from org.apache.lucene.search import BooleanQuery
from org.apache.lucene.search import WildcardQuery
from org.apache.lucene.search import BooleanClause


import jieba
from org.apache.lucene.analysis.core import WhitespaceAnalyzer


def parseCommand(command): 
    allowed_opt = ['title', 'url', 'site']
    command_dict = {}
    
    for i in command.split(' '):
        opt = 'contents'
        if ':' in i:
            opt, value = i.split(':')[:2]
            opt = opt.lower()
            if opt in allowed_opt and value != '':
                command_dict[opt] = command_dict.get(opt, '') + ' ' + value
        else:
            command_dict[opt] = command_dict.get(opt, '') + ' ' + ' '.join(jieba.cut(i))
    return command_dict



def run(searcher, analyzer):
    while True:
        print
        print "Hit enter with no input to quit."
        command = raw_input("Query:")
        command = unicode(command, 'UTF-8')
        if command == '':
            return

        print
        print "Searching for:", command #朱莉与茱莉娅

        # final = jieba.cut(command)
        # query = QueryParser(Version.LUCENE_CURRENT, "contents",
        #                     analyzer).parse(' '.join(final))
        
        querys = BooleanQuery()
        command_dict = parseCommand(command)
        for k,v in command_dict.iteritems():            
            if(k=='site'):
                t = Term('url','*'+v.strip()+'*')
                query = WildcardQuery(t)
            else:
                query = QueryParser(Version.LUCENE_CURRENT, k,analyzer).parse(v)
            querys.add(query, BooleanClause.Occur.MUST)
        
        scoreDocs = searcher.search(querys, 50).scoreDocs
        print "%s total matching documents." % len(scoreDocs)

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print '------------------------------------------'
            #print 'path:', doc.get("path"), 'name:', doc.get("name"),'site:', doc.get('site')
            print 'title:',doc.get('title'),
            print 'url:',doc.get('url')

if __name__ == '__main__':
    STORE_DIR = "index_lucene"
    initVM()
    print 'lucene', VERSION
    if VERSION[0]<'4':
        print 'Please read the pdf. This program only supports Lucene 4.x'
        sys.exit(1)
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(DirectoryReader.open(directory))
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    del searcher
