import csv
"save and open files"


def save(data, file):
    with open(file, 'w', newline='') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in data:
            csv_writer.writerow(row)


def load(file):
    file_content = open(file, "r")
    data = list(csv.reader(file_content, delimiter=","))
    file_content.close()
    return data
