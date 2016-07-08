# -*- coding: utf-8 -*-

import subprocess, os


if __name__ == "__main__":
    a = os.listdir('../py3/texts')
    for d in a:
        b = os.listdir('../py3/texts/' + d)
        for f in b:
            # output = subprocess.Popen("./runTagger.sh --output-format conll ../py3/texts/" + d + "/" + f, stdout=subprocess.PIPE).communicate()[0]
            print "./runTagger.sh --output-format conll ../py3/texts/" + d + "/" + f
            p = subprocess.Popen(["./runTagger.sh", "--output-format", "conll", "../py3/texts/" + d + "/" + f], shell=False, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            #p.stdin.write("../py3/texts/" + d + "/" + f)
            output, err = p.communicate()
            print output
            with open("../ark-results/" + str(f) + ".txt", "w") as f:
                f.write(output)
