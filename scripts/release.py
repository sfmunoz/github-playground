#!/usr/bin/env python3

import os
from subprocess import Popen, PIPE

class Release(object):
    def __init__(self) -> None:
        pass

    def get_tags(self,ref):
        cmd = ["git","tag","--sort=-creatordate","--format=%(refname:strip=2)"]
        p = Popen(args=cmd,stdout=PIPE,stderr=PIPE)
        (odata,edata) = p.communicate()
        if p.returncode != 0:
            raise Exception("'{0}' command failed: {1}".format(" ".join(cmd),edata.decode().strip()))
        tags = []
        found = False
        for line in odata.decode().strip().split("\n"):
            if line == ref:
                tags.append(line)
                found = True
                continue
            if found:
                tags.append(line)
                break
        if not found:
            raise Exception("cannot find '{0}' tag".format(ref))
        return tags

    def get_log(self,tags):
        log_range = tags[0] if len(tags) < 2 else "{0}..{1}".format(tags[1],tags[0])
        cmd = ["git","log",log_range,"--pretty=format:- %H %s (%ai)"]
        p = Popen(args=cmd,stdout=PIPE,stderr=PIPE)
        (odata,edata) = p.communicate()
        if p.returncode != 0:
            raise Exception("'{0}' command failed: {1}".format(" ".join(cmd),edata.decode().strip()))
        for line in odata.decode().strip().split("\n"):
            print(line)

    def run(self) -> None:
        ref = os.getenv("GITHUB_REF_NAME")
        if ref is None:
            raise Exception("undefined 'GITHUB_REF_NAME'")
        tags = self.get_tags(ref)
        self.get_log(tags)

if __name__ == "__main__":
    Release().run()
