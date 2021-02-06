
sequence_File = open("uniprot_IDs_and_their_corresponding_sequences.txt", "r")
sequences = []
i = 0
for line in sequence_File:
    if (i % 2 == 1):
        sequences.append(line.split()[0])
    i += 1

_counter = {}
_counter['less_than_500'] = 0
_counter['Greater_than_500'] = 0
_counter['Greater_than_800'] = 0
_counter['Greater_than_1000'] = 0

for x in sequences:
    if len(x) > 1000:
        _counter['Greater_than_1000'] += 1
    elif len(x) > 800:
        _counter['Greater_than_800'] += 1
    elif len(x) > 500:
        _counter['Greater_than_500'] += 1
    else:
        _counter['less_than_500'] += 1

print('Greater_than_1000', '\t', _counter['Greater_than_1000'])
print('Greater_than_800', '\t', _counter['Greater_than_800'])
print('Greater_than_500', '\t', _counter['Greater_than_500'])
print('less_than_500', '\t', _counter['less_than_500'])