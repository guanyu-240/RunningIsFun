import pandas


FILE_DELIMITER = "\t"
DATE_COLUMN = "Date"
TYPE_COLUMN = "Type"
SUBTYPE_COLUMN = "SubType"


def loadTable(fileName, header=None):
    """
    Load data file into table
    """
    table = pandas.read_table("log.txt", sep="\t", header=header)
    return table


def allRecords(table, startDate, endDate=None):
    """
    All records in a given time range
    """
    exp = "{DATE_COLUMN} >= {startDate}"
    if not endDate:
        exp += " and {DATE_COLUMN} <= {endDate}"
    return table.query(exp)
