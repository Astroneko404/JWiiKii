infile = open('trim', 'r', encoding='utf-8')
dir = 'data/text_rip/'
outfile_count = 0
line_count = 0
buff = 50000

outfile_dir = dir + 'part_' + str(outfile_count) + '.txt'
outfile = open(outfile_dir, 'w+', encoding='utf-8')

while True:
    line = infile.readline()
    if not line:
        break

    if line_count == buff:
        print('part_' + str(outfile_count) + ' finished')
        outfile.close()
        line_count = 0
        outfile_count += 1
        outfile_dir = dir + 'part_' + str(outfile_count) + '.txt'
        outfile = open(outfile_dir, 'w+', encoding='utf-8')

    outfile.write(line)
    line_count += 1
