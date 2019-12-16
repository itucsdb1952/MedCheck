def checkbox_to_bool(checkbox_value: str) -> bool:
    checkbox_value = checkbox_value.lower()
    if checkbox_value == 'on' or checkbox_value == 'true':
        return True
    else:
        return False


def convert_to_like(column_value: str) -> str:
    """
    It takes a string and converts like query.
    Eg: "357" -> "%3%5%7%"
    """
    like_query = "%".join(column_value)
    like_query = "%" + like_query + "%"
    return like_query


def check_where_exist(query: str, column: object, condition: str, like: bool = False) -> str:
    """
    It checks query has "WHERE", if it, query added with "AND (COLUMN = VALUE)" else, query added with "WHERE (COLUMN = VALUE)
    """

    if column is not None:
        if like:
            column = convert_to_like(column)
        condition = condition.format(column)
        if "WHERE" in query:
            new_query = f" AND ({condition}) "
            new_query = f" AND ({condition}) "
        else:
            new_query = f" WHERE ({condition}) "
        return new_query
    return ""


def create_where(args):
    initial = "WHERE ({});"
