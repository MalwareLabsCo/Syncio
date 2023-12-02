import json



def getConfigurations():
    try:
        f = open("./CONFIG.json", "r")
        data = f.read()
        f.close()

        parsed_data = json.loads(data)

        # get the folders to be backed up
        folders_value = parsed_data["folders"]
        folders_list = folders_value.split(", ")
        return folders_list
    except:
        return "ERROR"


def editConfigurations(folders):

    f = open("./CONFIG.json", "w")
    data = f.write('{"folders": "'+folders+'"}')
    f.close()
    return True