def create_connection(db_file):
    conn = None

    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_specific_card(conn, cardid):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param priority:
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT cardid FROM allowed_users WHERE cardid = %s" %  (cardid))

    rows = cur.fetchall()

    if not rows:
        print ("NO USER FOUND")
        PlayAccessDenied()
    else:
        print ("USER FOUND")
        for row in rows:
            print("User:")
            print(row)
        PlayAccessGranted()
