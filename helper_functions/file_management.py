# a simple function that strips all extra white spaces from uploaded files
def trim_text_file(input_file_path):
    fd = open(input_file_path, "r+")
    text = fd.read().strip()
    fd.seek(0)
    fd.truncate()
    fd.write(text)
    fd.close()
