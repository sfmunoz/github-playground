#!/usr/bin/env python3

import os
from subprocess import Popen, PIPE

class Release(object):
    def __init__(self) -> None:
        pass

    def get_ref(self):
        ref = os.getenv("GITHUB_REF_NAME")
        if ref is None:
            raise Exception("undefined 'GITHUB_REF_NAME'")
        return ref

    def get_tags(self,ref):
        cmd = ["git","tag","--sort=-creatordate","--format=%(refname:strip=2)"]
        p = Popen(args=cmd,stdout=PIPE,stderr=PIPE)
        (odata,edata) = p.communicate()
        if p.returncode != 0:
            raise Exception("'{0}' command failed: {1}".format(" ".join(cmd),edata.decode().strip()))
        lines = odata.decode().strip().split("\n")
        idx = lines.index(ref)
        if idx < 0:
            raise Exception("cannot find '{0}' tag".format(ref))
        if idx < len(lines)-1:
            return [lines[idx],lines[idx+1]]
        return [lines[idx]]

    def get_tag_msg(self,tag):
        cmd = ["git","for-each-ref","--format=%(contents)","refs/tags/{0}".format(tag)]
        p = Popen(args=cmd,stdout=PIPE,stderr=PIPE)
        (odata,edata) = p.communicate()
        if p.returncode != 0:
            raise Exception("'{0}' command failed: {1}".format(" ".join(cmd),edata.decode().strip()))
        return odata.decode().strip().split("\n")

    def get_log(self,tags):
        log_range = tags[0] if len(tags) < 2 else "{0}..{1}".format(tags[1],tags[0])
        cmd = ["git","log",log_range,"--pretty=format:- %H %s (%ai)"]
        p = Popen(args=cmd,stdout=PIPE,stderr=PIPE)
        (odata,edata) = p.communicate()
        if p.returncode != 0:
            raise Exception("'{0}' command failed: {1}".format(" ".join(cmd),edata.decode().strip()))
        return odata.decode().strip().split("\n")

    def run(self) -> None:
        ref = self.get_ref()
        tags = self.get_tags(ref)
        tag_msg = self.get_tag_msg(tags[0])
        log_lines = self.get_log(tags)
        for line in tag_msg:
            print(line)
        print()
        print("## Changelog")
        print()
        for line in log_lines:
            print(line)

if __name__ == "__main__":
    Release().run()
