import yaml
import requests
import pymysql
from config import host, user, password, db_name


# response = requests.get('http://example.com/toys', params={'updated_after':'2017-01-01', 'updated_before':'2019-01-01'})

# with open('toys.yaml') as file:
#     data = yaml.load(file, Loader=yaml.FullLoader)
#
# toys_repair = []
# for toy in data['toys']:
#     if toy['status'] == 'broken':
#         for game in toy['games']:
#             toys_repair.append((toy['id'], game['note']))

# toys_games = []
# for toy in data['toys']:
#     for game in toy['games']:
#         toys_games.append((game['id'], toy['id'], game['note']))

# toys = []
# for toy in data['toys']:
#     toys.append((toy['id'], toy['name'], toy['status'], toy['status_updated']))
#
# with open('games.yaml') as file:
#     data = yaml.load(file, Loader=yaml.FullLoader)
#
# games = []
# for game in data['games']:
#     games.append((game['id'], game['name'], game['date']))




try:
    # connect to database
    connection = pymysql.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )

    print ('connect ok')

    try:
        # CREATE TABLES
        with connection.cursor() as cursor:
            create_table_toys = """CREATE TABLE IF NOT EXISTS`toys`(
                                `id` int NOT NULL AUTO_INCREMENT,
                                `toy_id` int,
                                `name` varchar (50),
                                `status` varchar (255),
                                `status_updated` date,
                                PRIMARY KEY (`id`));"""

            create_table_games = """CREATE TABLE IF NOT EXISTS `games`(
                                `id` int NOT NULL AUTO_INCREMENT,
                                `game_id` int,
                                `name` varchar (50),
                                `date` date,
                                PRIMARY KEY (`id`));"""

            create_table_toys_games = """CREATE TABLE IF NOT EXISTS `toys_games` (
                                    `id` int NOT NULL AUTO_INCREMENT,
                                    `game_id` int,
                                    `toy_id` int,
                                    `note` varchar (255),
                                    PRIMARY KEY (`id`));"""

            create_table_toys_repair = """CREATE TABLE IF NOT EXISTS `toys_repair` (
                                    `id` int NOT NULL AUTO_INCREMENT,
                                    `toy_id` int,
                                    `issue_description` varchar (255),
                                    PRIMARY KEY (`id`));"""

            cursor.execute(create_table_toys)
            cursor.execute(create_table_games)
            cursor.execute(create_table_toys_games)
            cursor.execute(create_table_toys_repair)

        # INSERT
        # with connection.cursor() as cursor:
        #     insert_query = """INSERT INTO `toys` (toy_id, name, status, status_updated) VALUES (%s, %s, %s, %s);"""
        #     cursor.executemany(insert_query, toys)
        #     connection.commit()
        #
        # with connection.cursor() as cursor:
        #     insert_query = """INSERT INTO `games` (game_id, name, date) VALUES (%s, %s, %s);"""
        #     cursor.executemany(insert_query, games)
        #     connection.commit()

        # with connection.cursor() as cursor:
        #     insert_query = """INSERT INTO `toys_games` (game_id, toy_id, note) VALUES (%s, %s, %s);"""
        #     cursor.executemany(insert_query, toys_games)
        #     connection.commit()

        # with connection.cursor() as cursor:
        #     insert_query = """INSERT INTO `toys_repair` (toy_id, issue_description) VALUES (%s, %s);"""
        #     cursor.executemany(insert_query, toys_repair)
        #     connection.commit()

        # SELECT for question 4
        print('Question 4', '#' * 100)
        with connection.cursor() as cursor:
            select = """SELECT toys.toy_id, toys.name, status, status_updated, games.name, date, note
                    FROM toys, games , toys_games
                    WHERE status_updated >= CURDATE() - INTERVAL 1 YEAR AND 
                        toys.toy_id = toys_games.toy_id AND
                        games.game_id = toys_games.game_id;
                    """
            cursor.execute(select)
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        print('#' * 100)

        # SELECT for question 5
        print('Question 5', '#' * 100)
        with connection.cursor() as cursor:
            select = """SELECT DISTINCT name 
                        FROM toys, toys_repair
                        WHERE toys.toy_id <> toys_repair.toy_id;
                        """
            cursor.execute(select)
            rows = cursor.fetchall()
            print ([row['name'] for row in rows])
        print('#' * 100)

        # SELECT for question 3.a
        with connection.cursor() as cursor:
            select = """SELECT * FROM `games`
                        WHERE date >= CURDATE() - INTERVAL 7 DAY ;
                        """
            cursor.execute(select)
            rows = cursor.fetchall()
            new_games = [{'games':[row for row in rows]}]

        # created a.yaml
        with open ('a.yaml', 'w') as file:
            data = yaml.dump(new_games)
            file.write(data)

        # SELECT for question 3.b
        with connection.cursor() as cursor:
            select = """SELECT * FROM `toys`
                        WHERE status_updated >= CURDATE() - INTERVAL 7 DAY ;
                        """
            cursor.execute(select)
            rows = cursor.fetchall()
            new_toys = [{'toys':[row for row in rows]}]

        # created b.yaml
        with open ('b.yaml', 'w') as file:
            data = yaml.dump(new_toys)
            file.write(data)

        # SELECT for question 3.c
        with connection.cursor() as cursor:
            select = """SELECT * FROM `toys_repair` ;"""
            cursor.execute(select)
            rows = cursor.fetchall()
            toys_repair = [{'toys_repair':[row for row in rows]}]

        # created c.yaml
        with open ('c.yaml', 'w') as file:
            data = yaml.dump(toys_repair)
            file.write(data)

    finally:
        connection.close()

except Exception as ex:
    print('Except:', ex)
