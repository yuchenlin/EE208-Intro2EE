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

STORE_DIR=None
directory=None
searcher=None
analyzer=None


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



def run(command, pageindex,pagesize):
    global searcher,analyzer

    print "Searching for:", command 
    querys = BooleanQuery()
    command_dict = parseCommand(command)
    for k,v in command_dict.iteritems():
        query = QueryParser(Version.LUCENE_CURRENT, k,
                            analyzer).parse(v)

        querys.add(query, BooleanClause.Occur.MUST)

    scoreDocs = searcher.search(querys, 6000).scoreDocs
    print "%s total matching documents." % len(scoreDocs)
    start = (pageindex - 1) * pagesize
    end = start + pagesize
    res = []
    for scoreDoc in scoreDocs[start:end+1]:
        doc = searcher.doc(scoreDoc.doc)
        r = []
        r.append(doc.get('title'))
        r.append(doc.get('url'))
        r.append(doc.get('src'))
        r.append(doc.get('alt').replace(' ',''))
        res.append(r)
    return res,len(scoreDocs)
    


def init():
    global STORE_DIR,directory,searcher,analyzer
    STORE_DIR = "image_index_v3"
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(directory, True)
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    
