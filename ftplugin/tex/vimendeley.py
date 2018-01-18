import os
import sys
import sqlite3
import vim
import webbrowser

mendeley_dir = os.path.expanduser("~/.local/share/data/Mendeley Ltd./Mendeley Desktop")

def query_db(query, args=(), one=False):
    try:
        for f in os.listdir(mendeley_dir):
            if '@' in f:
                if f.split("@")[-1] == "www.mendeley.com.sqlite":
                    mendeley_db = os.path.join(mendeley_dir, f)
    except:
        print "Could not find Mendeley directory"
        return None

    if mendeley_db is None:
        print "Could not find Mendeley database"
        return None

    cur = sqlite3.connect(mendeley_db).cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv


def printAbstract():
    key = vim.eval('expand("<cword>")')

    try:
        title, abstract, year = query_db(
            "SELECT title, abstract, year FROM Documents WHERE citationKey == ? LIMIT 1",(key,),True)
    except:
        return

    print(title    + "\n----------------------------")
    print(abstract + "\n----------------------------")

def openPDF():
    key = vim.eval('expand("<cword>")')

    try:
        documentId = query_db("SELECT id FROM Documents WHERE citationKey == ? LIMIT 1", (key,), True)[0]
        hash = query_db("SELECT hash FROM DocumentFiles WHERE documentId == ?", (documentId,), True)[0]
        file = query_db("SELECT localUrl FROM Files WHERE hash = ?" , (hash,), True)[0]
    except:
        return

    os.system("/usr/bin/xdg-open '%s' 2> /dev/null &" % file)

def openWeb():
    key = vim.eval('expand("<cword>")')
    doi = query_db("SELECT doi FROM Documents WHERE citationKey == ? LIMIT 1",(key,),True)[0]
    if doi:
        webbrowser.open("http://doi.org/"+doi)

