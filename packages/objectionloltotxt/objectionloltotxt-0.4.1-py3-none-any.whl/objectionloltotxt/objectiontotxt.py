import base64
import json


def objection_data_to_readable_file(filename, json_pretty_output=False):
    """
    Opens the specified .objection file and converts it to prettyprint json. It will create the
    file to the directory of the file that is passed
    """
    assert filename.endswith(
        ".objection"), "the file you provided isn't a .objection file, if it is please make the file extension " \
                       ".objection "

    if json_pretty_output:
        file_extension = "_pretty.json"
        python_json_dict = process_objection_data(filename, file_extension)
        with open(filename.replace(".objection", file_extension), "w") as output_file:
            json.dump(python_json_dict, output_file, sort_keys=True, indent=0)
            output_file.close()
    else:
        file_extension = "_readable.txt"
        python_json_dict = process_objection_data(filename, file_extension)
        with open(filename.replace(".objection", file_extension), "w") as output_file:
            try:
                for frame in python_json_dict["frames"]:
                    output_file.write(frame["username"] + ": " + frame["text"] + "\n\n")
            except TypeError:
                try:
                    for frame in python_json_dict:
                        output_file.write(frame["username"] + ": " + frame["text"] + "\n\n")
                except KeyError:
                    raise KeyError("The objection file got no username key, most likely not a court recording")

            output_file.close()


def process_objection_data(filename, file_extension):
    """
    Creates the output file before the readable output is inserted
    """
    with open(filename, "r") as input_file, open(filename.replace(".objection", file_extension), "w") as output_file:
        output_file.close()
        try:
            base64_decoded_input = base64.b64decode(input_file.read()).decode()
            json_input = json.loads(base64_decoded_input)
        except:
            json_input = json.loads(input_file)
        input_file.close()
        return json_input
