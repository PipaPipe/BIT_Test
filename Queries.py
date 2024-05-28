import enum


# Модуль для работы с запросами, каждые запросы разбиты на отдельные
# перечисления, откуда мы можем взять нужный нам запрос

class UserQueries(enum.Enum):
    add_user = '''INSERT INTO Users (address_id, first_name, last_name) VALUES (?, ?, ?);'''
    delete_user = '''DELETE FROM Users WHERE id = (?);'''
    update_user = '''UPDATE Users SET address_id = ?, first_name = ?, last_name = ? WHERE id = ?;'''


class AddressQueries(enum.Enum):
    add_address = '''INSERT INTO Addresses (city_name, street_name) VALUES (?,?);'''
    delete_address = '''DELETE FROM Addresses WHERE id = (?);'''
    update_address = '''UPDATE Addresses SET city_name = ?, street_name = ? WHERE id = ?;'''


class AuthorsQueries(enum.Enum):
    add_author = '''INSERT INTO Authors (name) VALUES (?);'''
    delete_author = '''DELETE FROM Authors WHERE id = (?);'''
    update_author = '''UPDATE Authors SET name = ? WHERE id = ?;'''


class GenresQueries(enum.Enum):
    add_genre = '''INSERT INTO Genres(name) VALUES (?);'''
    delete_genre = '''DELETE FROM Genres WHERE id = (?);'''
    update_genre = '''UPDATE Genres SET name = ? WHERE id = ?;'''


class BookQueries(enum.Enum):
    add_book = '''INSERT INTO Books (title, author_id, genre_id) VALUES (?, ?, ?);'''
    delete_book = '''DELETE FROM Books WHERE id = ?;'''
    update_book = '''UPDATE Books SET author_id = ?, genre_id = ?, title = ? WHERE id = ?;'''


class DistributionQueries(enum.Enum):
    check_book = '''
    SELECT book_id, user_id
    FROM Distribution
    WHERE return_date is NULL and book_id = ?
    '''
    give_book = '''
    INSERT INTO
    Distribution (book_id, user_id, load_date, return_date, expected_return_date) 
    VALUES (?, ?, date('now'), NULL, date('now', '14 days')); '''
    return_book = '''UPDATE Distribution SET return_date = DATE() WHERE book_id = ? AND user_id = ?;'''


class StatsQueries(enum.Enum):
    select_all_addresses = '''SELECT * FROM Addresses'''
    select_all_books = '''SELECT * FROM Books'''
    select_all_users = '''SELECT * FROM Users'''
    select_count_of_all_taken_books = '''
    SELECT 
        us.first_name as user_name,
        COUNT(book_id) as count
    FROM
        Distribution d
        LEFT JOIN Users us ON us.id = d.user_id
    GROUP BY 
        us.id    
    ORDER BY us.first_name;
    '''
    select_user_taken_books = '''
    SELECT 
    	us.id,
        us.first_name || ' ' || us.last_name as user_name,
        COUNT(d.book_id) as taken_books
    FROM 
        Distribution d
        LEFT JOIN Users us ON us.id = d.user_id
    WHERE d.return_date is NULL
    GROUP BY us.id
    ORDER BY us.first_name;
    '''
    select_last_visit_date = '''
    SELECT user_name, last_visit_date
    FROM
    (select user_name, last_visit_date, ROW_NUMBER() OVER (PARTITION BY user_name ORDER BY last_visit_date DESC) as rn
    FROM
    (SELECT 
            us.first_name as user_name,
        CASE
            WHEN bd.return_date is NULL
                THEN bd.load_date
            WHEN bd.return_date is not NULL
                THEN bd.return_date
        END AS last_visit_date
        FROM
            Distribution bd
            LEFT JOIN Users us ON us.id = bd.user_id) res) res2
    WHERE rn = 1
    '''
    select_most_readable_author = '''
    SELECT 
        au.author_name as author_name,
        (COUNT(b.id) * 100.0 / (SELECT COUNT(bd.book_id) FROM Distribution bd)) as author_rating
    FROM
        Distribution bd
        LEFT JOIN Books b ON b.id = bd.book_id
        LEFT JOIN Authors au ON au.id = b.author_id
    GROUP BY  
        au.id
    ORDER BY author_rating DESC;
    '''
    select_favourite_genre = '''
    SELECT user_name, genre_name
    FROM
    (SELECT user_name, genre_name, rating, ROW_NUMBER() OVER(PARTITION BY user_name) as rn
    FROM
        (SELECT 
            us.first_name || " " || us.last_name as user_name,
            g.genre_name as genre_name,
            COUNT(bd.book_id) OVER(PARTITION BY us.id, g.id)* 100.0 / COUNT(bd.book_id) OVER(PARTITION BY us.id) as rating
        FROM
            Distribution bd
            LEFT JOIN Books b ON bd.book_id = b.id
            LEFT JOIN Genres g ON b.genre_id = g.id
            LEFT JOIN Users us ON bd.user_id = us.id
         ORDER BY rating DESC, genre_name) res) res1
     where rn = 1
    '''
    select_most_readable_genre = '''
    SELECT 
        g.genre_name as genre_name,
        (COUNT(g.id) * 100.0 / (SELECT COUNT(db.book_id) FROM Distribution db)) as genre_rating
    FROM 
        Distribution bd
        LEFT JOIN Books b ON bd.book_id = b.id
        LEFT JOIN Genres g ON g.id = b.genre_id
    GROUP BY
         g.id
    ORDER BY genre_rating DESC;
    '''
    select_book_expired_info = '''
    SELECT b.title, u.first_name || " " || u.last_name as user_name, d.return_date - d.expected_return_date as overdue
    from Distribution d 
    left join Users u ON u.id = d.user_id 
    left join Books b ON b.id = d.book_id 
    Where d.return_date > d.expected_return_date and d.return_date is not null
    '''
    select_taken_book_location = '''
    SELECT a.city_name, a.street_name
    from Distribution d 
    left join Users u on u.id = d.user_id
    left join Addresses a on u.address_id = a.id
    where return_date is NULL
    '''
