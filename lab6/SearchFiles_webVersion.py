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
 
STORE_DIR = None
directory = None 
searcher = None
analyzer = None
vm_env = None

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



def run(command,pageindex=1,pagesize=15):
    global searcher, analyzer,old_command,old_res_list
    global STORE_DIR,directory,searcher,analyzer
    if command == '':
        return

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
    
    scoreDocs = searcher.search(querys, 4000).scoreDocs
    print "%s total matching documents." % len(scoreDocs)
    
    res_list = []
    simpleHTMLFormatter = SimpleHTMLFormatter("<font_forblank_color='red'>", "</font>")

    queryToHigh = QueryParser(Version.LUCENE_CURRENT,"contents",analyzer).parse(command_dict['contents'])

    hlter = Highlighter(simpleHTMLFormatter,QueryScorer(queryToHigh))
    hlter.setTextFragmenter(SimpleFragmenter(200))
    start = (pageindex-1)*pagesize
    end = start+pagesize
    for scoreDoc in scoreDocs[start:end+1]:
        doc = searcher.doc(scoreDoc.doc)
        res = []
        res.append(doc.get('title'))
        res.append(doc.get('url'))
        output = hlter.getBestFragment(analyzer,"contents",clear(doc.get('contents')))
        res.append(output)
        res_list.append(res) 
    return res_list,len(scoreDocs)

def init():
    global STORE_DIR,directory,searcher,analyzer,vm_env
    STORE_DIR = "index_lucene_v3_highlight"
    if(vm_env==None):
        vm_env = initVM(vmargs=['-Djava.awt.headless=true'])
    print 'lucene', VERSION
    directory = SimpleFSDirectory(File(STORE_DIR))
    searcher = IndexSearcher(directory, True)
    analyzer = WhitespaceAnalyzer(Version.LUCENE_CURRENT)
    
def closeSercher():
    global searcher
    searcher.close()

