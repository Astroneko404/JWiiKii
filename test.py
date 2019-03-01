import Mykytea


def showTags(t, outfile):
    for word in t:
        out = word.surface + "\t"
        for t1 in word.tag:
            for t2 in t1:
                for t3 in t2:
                    out = out + "/" + str(t3)
                out += "\t"
            out += "\t"
        outfile.write(out+'\n')


infile = open('data/in.txt', 'r', encoding='utf-8')
outfile = open('data/out.txt', 'w+', encoding='utf-8')

opt = "-model model/full_svm.mod"
mk = Mykytea.Mykytea(opt)

while True:
    line = infile.readline()
    if not line:
        break
    print(line)
    tag = mk.getTags(line)
    showTags(tag, outfile)
