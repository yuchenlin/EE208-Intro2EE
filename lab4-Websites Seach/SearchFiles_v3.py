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
                   Term, WildcardQuery,WhitespaceAnalyzer,StandardAnalyzer,\
                   SimpleHTMLFormatter,Highlighter,QueryScorer,SimpleFragmenter



import jieba

def clear(text):
    todelete = ['\n','\r','\t']
    for i in todelete:
        text = text.replace(i,'')
    return text
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
        scoreDocs = searcher.search(querys, 10).scoreDocs
        
        print "%s total matching documents." % len(scoreDocs)
        simpleHTMLFormatter = SimpleHTMLFormatter("<font color='red'>", "</font>")

        queryToHigh = QueryParser(Version.LUCENE_CURRENT,"contents",analyzer).parse(command_dict['contents'])

        hlter = Highlighter(simpleHTMLFormatter,QueryScorer(queryToHigh))
        hlter.setTextFragmenter(SimpleFragmenter(500))
        for scoreDoc in scoreDocs:
            doc = searcher.doc(scoreDoc.doc)
            print '------------------------------------------'
            #print 'path:', doc.get("path"), 'name:', doc.get("name"),'site:', doc.get('site')
            print 'title:',doc.get('title'),
            print 'url:',doc.get('url')
            ori_text = clear(doc.get('contents'))
            output = hlter.getBestFragment(analyzer,"contents",ori_text)
            print output
        #scoreDocs = searcher.searchAfter(querys,1,50).scoreDocs

if __name__ == '__main__':
    STORE_DIR = "index_lucene_v3_highlight"
    initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', VERSION
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(directory, True)
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    run(searcher, analyzer)
    searcher.close()
