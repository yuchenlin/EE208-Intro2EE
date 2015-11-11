#!/usr/bin/env python
#coding=utf8
import sys
import jcc
from lucene import initVM,VERSION
from lucene import QueryParser,\
                   IndexSearcher,\
                   WhitespaceAnalyzer,\
                   SimpleFSDirectory,\
                   File, VERSION,\
                   initVM, Version,\
                   BooleanQuery,\
                   BooleanClause,LimitTokenCountAnalyzer,\
                   Term, WildcardQuery,WhitespaceAnalyzer,StandardAnalyzer


import jieba 

"""
This script is loosely based on the Lucene (java implementation) demo class 
org.apache.lucene.demo.SearchFiles.  It will prompt for a search query, then it
will search the Lucene index in the current directory called 'index' for the
search query entered against the 'contents' field.  It will then display the
'path' and 'name' fields for each of the hits it finds in the index.  Note that
search.close() is currently commented out because it causes a stack overflow in
some cases.
"""


def parseCommand(command): 
    allowed_opt = ['title', 'url', 'site']
    command_dict = {}
    
    for i in command.split(' '):
        opt = 'alt'
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
        print "Searching for:", command 
        querys = BooleanQuery()
        command_dict = parseCommand(command)
        for k,v in command_dict.iteritems():
            query = QueryParser(Version.LUCENE_CURRENT, k,
                                analyzer).parse(v)
            querys.add(query, BooleanClause.Occur.MUST)

        scoreDocs = searcher.search(querys, 50).scoreDocs
        print "%s total matching documents." % len(scoreDocs)

        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print '------------------------------------------------'
            print 'title:',doc.get('title')
            print 'url:',doc.get('url')
            print 'src:',doc.get('src')


if __name__ == '__main__':
    STORE_DIR = "image_index_v3"
    initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', VERSION
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(directory, True)
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    searcher.close()
