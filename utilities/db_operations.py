import sqlite3
from sqlite3 import Error


def create_transfer_events_table(db_file="db/bat_details.sqlite"):
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('CREATE TABLE TRANSFER_EVENTS (TRANSACTION_HASH VARCHAR PRIMARY KEY, TO_ADDRESS VARCHAR, FROM_ADDRESS VARCHAR, TIMESTAMP NUMBER, DATA_HEX VARCHAR, DATA_INT VARCHAR, DATA_FLOAT REAL, BLOCK_NUMBER NUMBER, TRANSACTION_INDEX VARCHAR, BLOCK_HASH VARCHAR, LOG_INDEX VARCHAR)')
        conn.commit()
        conn.close()
    except Error:
        raise

def create_create_events_table(db_file="db/bat_details.sqlite"):
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('CREATE TABLE CREATE_EVENTS (TRANSACTION_HASH VARCHAR PRIMARY KEY, TO_ADDRESS VARCHAR, FROM_ADDRESS VARCHAR, TIMESTAMP NUMBER, DATA_HEX VARCHAR, DATA_INT VARCHAR, DATA_FLOAT REAL, BLOCK_NUMBER NUMBER, TRANSACTION_INDEX VARCHAR, BLOCK_HASH VARCHAR, LOG_INDEX VARCHAR)')
        conn.commit()
        conn.close()
    except Error:
        raise


def create_block_details_table(db_file="db/bat_details.sqlite"):
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('CREATE TABLE BLOCK_DETAILS (BLOCK_NUMBER VARCHAR PRIMARY KEY, DIFFICULTY VARCHAR, EXTRA_DATA VARCHAR, GAS_LIMIT VARCHAR, GAS_USED VARCHAR, HASH VARCHAR, MINER VARCHAR, MIX_HASH VARCHAR, NONCE VARCHAR, PARENT_HASH VARCHAR, RECEIPTS_ROOT VARCHAR, SIZE VARCHAR, STATE_ROOT VARCHAR, TIMESTAMP VARCHAR, TOTAL_DIFFICULTY VARCHAR, TRANSACTIONS_ROOT VARCHAR)')
        conn.commit()
        conn.close()
    except Error:
        raise


def drop_table(table_name, db_file="db/bat_details.sqlite"):
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('DROP TABLE {}'.format(table_name))
        conn.commit()
        conn.close()
    except Error:
        raise


def truncate_table(table_name, db_file="db/bat_details.sqlite"):
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute('DELETE FROM {}'.format(table_name))
        conn.commit()
        conn.close()
    except Error:
        raise


def show_tables(db_file="db/bat_details.sqlite"):
    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()
        c.execute("SELECT NAME as TABLE_NAME FROM sqlite_master where type='table'")
        rows = c.fetchall()
        print(rows)
        conn.close()
    except Error:
        raise


def insert_records_batch(table_name, data, columns, db_file="db/bat_details.sqlite"):
    count = 0

    try:
        conn = sqlite3.connect(db_file)
        c = conn.cursor()

        c.execute('BEGIN TRANSACTION')

        query = "INSERT OR IGNORE INTO " + table_name + " VALUES " + str(tuple(["?"]*columns)).replace("'", "")

        # print("\n"+query)
        for row in data:
            c.execute(query, row)
            count += 1

        c.execute('COMMIT')
        conn.close()
    except Error:
        print("\n", data[count], "Count = ", count)
        raise


# UPDATE QUERIES:
# UPDATE CREATE_EVENTS
# SET TIMESTAMP = (SELECT TIMESTAMP FROM BLOCK WHERE BLOCK.BLOCKNUMBER = CREATE_EVENTS.BLOCK_NUMBER)
# WHERE EXISTS (SELECT TIMESTAMP FROM BLOCK WHERE BLOCK.BLOCKNUMBER = CREATE_EVENTS.BLOCK_NUMBER);


if __name__ == "__main__":
    db_file_main = "../db/blockchain.db"
    operation = 4
    if operation == 1:
        create_transfer_events_table(db_file_main)
    elif operation == 2:
        create_create_events_table(db_file_main)
    elif operation == 3:
        create_block_details_table(db_file_main)
    elif operation == 4:
        truncate_table("CREATE_EVENTS", db_file_main)
    elif operation == 5:
        show_tables(db_file_main)
    elif operation == 6:
        drop_table("CREATE_EVENTS", db_file_main)
