import mysql.connector

# TODO: REPLACE THE VALUE OF VARIABLE team (EX. TEAM 1 --> team = 1)
team = 0


# Requirement1: create schema ( name: DMA_team## )
def requirement1(host, user, password):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')

    # TODO: WRITE CODE HERE
    print('Creating schema...')
    cursor.execute('DROP DATABASE IF EXISTS DMA_team%02d;' % team)
    cursor.execute('CREATE DATABASE IF NOT EXISTS DMA_team%02d;' % team)

    # TODO: WRITE CODE HERE
    cursor.close()


# Requierement2: create table
def requirement2(host, user, password):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')

    # TODO: WRITE CODE HERE
    print('Creating tables...')
    cursor.execute('USE DMA_team%02d;' % team)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS developer(
    id INT(11) NOT NULL,
    name VARCHAR(255) NOT NULL,
    profile_image TINYINT(1) default 0,
    profile_link INT(11) default 0,
    PRIMARY KEY (id) );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user(
    id INT(11) NOT NULL,
    name VARCHAR(255) NOT NULL,
    PRIMARY KEY (id) );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_follow(
    user_id INT(11) NOT NULL,
    follow_user_id INT(11) NOT NULL,
    follow_date DATETIME NOT NULL,
    PRIMARY KEY (user_id, follow_user_id) );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS app(
    id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    developer_id INT(11) NOT NULL,
    description INT(11) default 0,
    pricing_hint VARCHAR(255),
    PRIMARY KEY (id) );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS key_benefit(
    app_id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    description INT(11) default 0,
    PRIMARY KEY (app_id, title) );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS pricing_plan(
    id VARCHAR(255) NOT NULL,
    app_id VARCHAR(255) NOT NULL,
    title VARCHAR(255),
    price VARCHAR(255) NOT NULL,
    PRIMARY KEY (id) );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS category(
    id VARCHAR(255) NOT NULL,
    title VARCHAR(255) NOT NULL,
    unique (title),
    PRIMARY KEY (id) );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS category_user(
    category_id VARCHAR(255) NOT NULL,
    user_id INT(11) NOT NULL,
    PRIMARY KEY (category_id, user_id) );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS category_developer(
    category_id VARCHAR(255) NOT NULL,
    developer_id INT(11) NOT NULL,
    PRIMARY KEY (category_id, developer_id) );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS app_category(
    app_id VARCHAR(255) NOT NULL,
    category_id VARCHAR(255) NOT NULL,
    PRIMARY KEY (app_id, category_id) );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS message(
    id INT(11) NOT NULL,
    recipient_id INT(11) NOT NULL,
    sent_date DATETIME NOT NULL,
    PRIMARY KEY (id) );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS message_app(
    message_id INT(11) NOT NULL,
    app_id VARCHAR(255) NOT NULL,
    PRIMARY KEY (message_id, app_id) );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS review(
    id INT(11) NOT NULL,
    app_id VARCHAR(255) NOT NULL,
    user_id INT(11) NOT NULL,
    rating INT(11) default 0,
    body INT(11) default 0,
    helpful_count INT(11) default 0,
    posted_date DATETIME NOT NULL,
    PRIMARY KEY (id) );
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS reply(
    id INT(11) NOT NULL,
    review_id INT(11) NOT NULL,
    developer_id INT(11) NOT NULL,
    content INT(11) default 0,
    posted_date DATETIME NOT NULL,
    PRIMARY KEY (id) );
    ''')

    # TODO: WRITE CODE HERE
    cursor.close()


# Requirement3: insert data
def requirement3(host, user, password, directory):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')

    # TODO: WRITE CODE HERE
    print('Inserting data...')
    cursor.execute('USE DMA_team%02d;' % team)
    table_name = ['developer', 'user', 'user_follow', 'app', 'key_benefit', 'pricing_plan', 'category',
                  'category_user', 'category_developer', 'app_category', 'message', 'message_app',
                  'review', 'reply']


    for table in table_name:
        print(table)
        filepath = directory + '/' + table + '.csv'
        with open(filepath, 'r', encoding='utf-8') as csv_data:
            next(csv_data, None)  # skip the headers
            if table in ['developer', 'pricing_plan']:
                for row in csv_data:
                    # Change the null data
                    row = row.strip().split(sep=',')
                    if '' in row:
                        temp = []
                        for item in row:
                            if item == '':
                                item = None
                            temp.append(item)
                        row = temp
                    cursor.execute('INSERT INTO ' + table + ' VALUES (%s,%s,%s,%s)', row)
                    cnx.commit()

            elif table in ['user', 'category', 'category_user', 'category_developer', 'app_category', 'message_app']:
                for row in csv_data:
                    # Change the null data
                    row = row.strip().split(sep=',')
                    if '' in row:
                        temp = []
                        for item in row:
                            if item == '':
                                item = None
                            temp.append(item)
                        row = temp
                    cursor.execute('INSERT INTO ' + table + ' VALUES (%s,%s)', row)
                    cnx.commit()

            elif table in ['user_follow', 'message', 'key_benefit']:
                for row in csv_data:
                    # Change the null data
                    row = row.strip().split(sep=',')
                    if '' in row:
                        temp = []
                        for item in row:
                            if item == '':
                                item = None
                            temp.append(item)
                        row = temp
                    cursor.execute('INSERT INTO ' + table + ' VALUES (%s,%s,%s)', row)
                    cnx.commit()

            elif table in ['app', 'reply']:
                for row in csv_data:
                    # Change the null data
                    row = row.strip().split(sep=',')
                    if '' in row:
                        temp = []
                        for item in row:
                            if item == '':
                                item = None
                            temp.append(item)
                        row = temp
                    cursor.execute('INSERT INTO ' + table + ' VALUES (%s,%s,%s,%s,%s)', row)
                    cnx.commit()

            elif table == 'review':
                for row in csv_data:
                    # Change the null data
                    row = row.strip().split(sep=',')
                    if '' in row:
                        temp = []
                        for item in row:
                            if item == '':
                                item = None
                            temp.append(item)
                        row = temp
                    cursor.execute('INSERT INTO ' + table + ' VALUES (%s,%s,%s,%s,%s,%s,%s)', row)
                    cnx.commit()

    # TODO: WRITE CODE HERE
    cursor.close()


# Requirement4: add constraint (foreign key)
def requirement4(host, user, password):
    cnx = mysql.connector.connect(host=host, user=user, password=password)
    cursor = cnx.cursor()
    cursor.execute('SET GLOBAL innodb_buffer_pool_size=2*1024*1024*1024;')

    # TODO: WRITE CODE HERE
    print('Adding constraints...')
    cursor.execute('USE DMA_team%02d;' % team)
    cursor.execute('ALTER TABLE review ADD CONSTRAINT FOREIGN KEY (app_id) REFERENCES app(id);')
    print("constraint 1 added")

    cursor.execute('ALTER TABLE review ADD CONSTRAINT FOREIGN KEY (user_id) REFERENCES user(id);')
    print("constraint 2 added")

    cursor.execute('ALTER TABLE reply ADD CONSTRAINT FOREIGN KEY (developer_id) REFERENCES developer(id);')
    print("constraint 3 added")

    cursor.execute('ALTER TABLE reply ADD CONSTRAINT FOREIGN KEY (review_id) REFERENCES review(id);')
    print("constraint 4 added")

    cursor.execute('ALTER TABLE app ADD CONSTRAINT FOREIGN KEY (developer_id) REFERENCES developer(id);')
    print("constraint 5 added")

    cursor.execute('ALTER TABLE app_category ADD CONSTRAINT FOREIGN KEY (app_id) REFERENCES app(id);')
    print("constraint 6 added")

    cursor.execute('ALTER TABLE app_category ADD CONSTRAINT FOREIGN KEY (category_id) REFERENCES category(id);')
    print("constraint 7 added")

    cursor.execute('ALTER TABLE user_follow ADD CONSTRAINT FOREIGN KEY (user_id) REFERENCES user(id);')
    print("constraint 8 added")

    cursor.execute('ALTER TABLE user_follow ADD CONSTRAINT FOREIGN KEY (follow_user_id) REFERENCES user(id);')
    print("constraint 9 added")

    cursor.execute('ALTER TABLE key_benefit ADD CONSTRAINT FOREIGN KEY (app_id) REFERENCES app(id);')
    print("constraint 10 added")

    cursor.execute('ALTER TABLE pricing_plan ADD CONSTRAINT FOREIGN KEY (app_id) REFERENCES app(id);')
    print("constraint 11 added")

    cursor.execute('ALTER TABLE category_user ADD CONSTRAINT FOREIGN KEY (category_id) REFERENCES category(id);')
    print("constraint 12 added")

    cursor.execute('ALTER TABLE category_user ADD CONSTRAINT FOREIGN KEY (user_id) REFERENCES user(id);')
    print("constraint 13 added")

    cursor.execute('ALTER TABLE category_developer ADD CONSTRAINT FOREIGN KEY (category_id) REFERENCES category(id);')
    print("constraint 14 added")

    cursor.execute('ALTER TABLE category_developer ADD CONSTRAINT FOREIGN KEY (developer_id) REFERENCES developer(id);')
    print("constraint 15 added")

    cursor.execute('ALTER TABLE message ADD CONSTRAINT FOREIGN KEY (recipient_id) REFERENCES user(id);')
    print("constraint 16 added")

    cursor.execute('ALTER TABLE message_app ADD CONSTRAINT FOREIGN KEY (message_id) REFERENCES message(id);')
    print("constraint 17 added")

    cursor.execute('ALTER TABLE message_app ADD CONSTRAINT FOREIGN KEY (app_id) REFERENCES app(id);')
    print("constraint 18 added")

    # TODO: WRITE CODE HERE
    cursor.close()


# TODO: REPLACE THE VALUES OF FOLLOWING VARIABLES
host = 'localhost'
user = 'root'
password = ''
directory_in = ''

requirement1(host=host, user=user, password=password)
requirement2(host=host, user=user, password=password)
requirement3(host=host, user=user, password=password, directory=directory_in)
requirement4(host=host, user=user, password=password)
print('Done!')

