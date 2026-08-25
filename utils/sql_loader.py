def load_sql(file_path):
    """
    Read and return the contents of a SQL file.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()