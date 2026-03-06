#!/usr/bin/env python3

import os, sys
from subprocess import Popen, PIPE

class ReleaseNotes(object):
    def __init__(self,fp):
        self.__fp = fp

    def __get_ref(self):
        ref = os.getenv("GITHUB_REF_NAME")
        if ref is None:
            raise Exception("undefined 'GITHUB_REF_NAME'")
        return ref

    def __get_tags(self,ref):
        cmd = ["git","tag","--sort=creatordate","--format=%(refname:strip=2)"]
        p = Popen(args=cmd,stdout=PIPE,stderr=PIPE)
        (odata,edata) = p.communicate()
        if p.returncode != 0:
            raise Exception("'{0}' command failed: {1}".format(" ".join(cmd),edata.decode().strip()))
        lines = odata.decode().strip().split("\n")
        idx = lines.index(ref)
        if idx < 0:
            raise Exception("cannot find '{0}' tag".format(ref))
        if idx == 0:
            return [lines[idx]]
        return [lines[idx],lines[idx-1]]

    def __get_tag_msg(self,tag):
        cmd = ["git","for-each-ref","--format=%(contents)","refs/tags/{0}".format(tag)]
        p = Popen(args=cmd,stdout=PIPE,stderr=PIPE)
        (odata,edata) = p.communicate()
        if p.returncode != 0:
            raise Exception("'{0}' command failed: {1}".format(" ".join(cmd),edata.decode().strip()))
        return odata.decode().strip().split("\n")

    def __get_log(self,tags):
        log_range = tags[0] if len(tags) < 2 else "{0}..{1}".format(tags[1],tags[0])
        cmd = ["git","log",log_range,"--pretty=format:- %H %s (%ai)"]
        p = Popen(args=cmd,stdout=PIPE,stderr=PIPE)
        (odata,edata) = p.communicate()
        if p.returncode != 0:
            raise Exception("'{0}' command failed: {1}".format(" ".join(cmd),edata.decode().strip()))
        return odata.decode().strip().split("\n")

    def run(self):
        ref = self.__get_ref()
        tags = self.__get_tags(ref)
        tag_msg = self.__get_tag_msg(tags[0])
        log_lines = self.__get_log(tags)
        notes = tag_msg[:]
        notes.extend(["","## Changelog",""])
        notes.extend(log_lines)
        self.__fp.write("\n".join(notes))

def main():
    fp = sys.stdout
    if len(sys.argv) > 1:
        fp = open(sys.argv[1],"w")
    ReleaseNotes(fp).run()

if __name__ == "__main__":
    main()
