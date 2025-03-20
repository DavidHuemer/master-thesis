from helper.files.jsonFileHelper import JsonFileHelper


def main():
    print("JML:")
    jml_content = JsonFileHelper.read_json_file("jml-results/1.json")
    for jml_key in jml_content:
        print(jml_key)
        print(jml_content[jml_key])


if __name__ == "__main__":
    main()
