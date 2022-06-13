import pandas as pd
from io import StringIO

def read_tsv(message):
    data = pd.read_csv(StringIO(message.decode('UTF-8')), sep="\t")
    for message in data['message']:
        print(message)
        return message

def read_csv(message):
    pd.options.display.max_rows = 9999
    data = pd.read_csv(StringIO(message.decode('UTF-8')))
    for message in data['message']:
        print(message)
        return message


def write_csv(output):
    print(output)
    csv_data = "id,message,topic\r\n"
    line = ""

    for message in output["messages"]:
        for key, value in message.items():
            #data += "{},{},{}\r\n".format(key, value["message"], value["exp"])
            line += str(value) + ","
        csv_data += line + "\r\n"
        line = ""
    return csv_data

def write_tsv(output):
    # print(output)
    tsv_data = "id\tmessage\ttopic\r\n"
    line = ""

    for message in output["messages"]:
        for key, value in message.items():
            #data += "{},{},{}\r\n".format(key, value["message"], value["exp"])
            line += str(value) + "\t"
        tsv_data += line + "\r\n"
        line = ""
    return tsv_data
    return tsv_data