import time

import pandas as pd

import Queries
import tools
from DBConnection import DBConnection


def main():
    conn = DBConnection('/Users/maksimsadkov/Bib')
    flag = True
    while flag:
        # Выбор действий
        ask = input(
            '\nВыберите действие, чтобы продолжить:\n'
            '(1) Работа с пользователями\n'
            '(2) Работа с книгами\n'
            '(3) Получить статистику\n'
            '(4) Добавить Факт взятия/возврата книги\n'
            '(5) Работа с адресами\n'
            '\n'
            '(6) Выйти\n')
        # Действия с пользователем
        if ask == '1':
            action = str(input(
                '\nЧто вы хотите сделать с пользователем\n'
                '(A) Добавить нового пользователя\n'
                '(U) Изменить пользователя\n'
                '(D) Удалить пользователя\n'
                '\n'
                '(X) Вернуться назад\n'))
            if action == 'A' or action == 'a':
                params = input(
                    '\nВведите ID адреса, имя пользователя и его фамилию через пробел\n').split()
                res = conn.query(Queries.UserQueries.add_user.value, params)
                tools.print_success_or_not(res[0])
            elif action == 'U' or action == 'u':
                params = input('\nВведите новый ID адреса, новое имя, новую фамилию и ID пользователя, которого '
                               'хотите изменить, '
                               'через пробел\n').split()
                res = conn.query(Queries.UserQueries.update_user.value, params)
                tools.print_success_or_not(res[0])
            elif action == 'D' or action == 'd':
                params = input('\nВведите ID пользователя, которого вы хотите удалить\n')
                res = conn.query(Queries.UserQueries.delete_user.value, params)
                tools.print_success_or_not(res[0])
            else:
                continue
        # Действия с книгами
        elif ask == '2':
            action = str(input(
                '\nЧто вы хотите сделать с книгой\n'
                '(A) Добавить новую книгу\n'
                '(U) Изменить книгу\n'
                '(D) Удалить книгу\n'
                '\n'
                '(X) Вернуться назад\n'))
            if action == 'A' or action == 'a':
                book_name = str(input('\nВведите название книги\n'))
                author_id = str(input('\nВведите ID автора\n'))
                genre_id = str(input('\nВведите ID жанра\n'))
                params = [book_name, author_id, genre_id]
                res = conn.query(Queries.BookQueries.add_book.value, params)

                tools.print_success_or_not(res[0])
            elif action == 'U' or action == 'u':

                author_id = str(input('\nВведите ID нового автора\n'))
                genre_id = str(input('\nВведите ID нового жанра\n'))
                book_name = str(input('\nВведите новое название книги\n'))
                book_id = str(input('\nВведите ID книги, которую хотите изменить\n'))

                params = [author_id, genre_id, book_name, book_id]
                res = conn.query(Queries.BookQueries.update_book.value, params)

                tools.print_success_or_not(res[0])
            elif action == 'D' or action == 'd':
                params = input('\nВведите ID книги, которую вы хотите удалить\n')
                res = conn.query(Queries.BookQueries.delete_book.value, params)

                tools.print_success_or_not(res[0])
            else:
                continue
        # Действия с отчетами
        elif ask == '3':
            action = str(input(
                '\nКакую статистику вы хотите получить\n'
                '(1) Кол-во книг\n'
                '(2) Кол-во читателей\n'
                '(3) Сколько книг брал каждый читатель за все время\n'
                '(4) Сколько книг сейчас находится на руках у каждого читателя\n'
                '(5) Дата последнего посещения читателем библиотеки\n'
                '(6) Самый читаемый автор\n'
                '(7) Самый предпочитаемые читателями жанры по убыванию\n'
                '(8) Любимый жанр каждого читателя\n'
                '(9) Вывести данные о просроченных возвратах\n'
                '(10) Вывести данные о геопозиции взятых книг\n'
                '\n'
                '(X) Вернуться назад\n'))
            if action == '1':
                df = pd.read_sql(Queries.StatsQueries.select_all_books.value, conn.get_connection())
                df.to_csv('./Reports/all_books.csv')
                print('Отчет успешно сформирован')
                time.sleep(2)
            elif action == '2':
                df = pd.read_sql(Queries.StatsQueries.select_all_users.value, conn.get_connection())
                df.to_csv('./Reports/all_users.csv')
                print('Отчет успешно сформирован')
                time.sleep(2)
            elif action == '3':
                df = pd.read_sql(Queries.StatsQueries.select_count_of_all_taken_books.value, conn.get_connection())
                df.to_csv('./Reports/all_taken_books.csv')
                print('Отчет успешно сформирован')
                time.sleep(2)
            elif action == '4':
                df = pd.read_sql(Queries.StatsQueries.select_user_taken_books.value, conn.get_connection())
                df.to_csv('./Reports/user_taken_books.csv')
                print('Отчет успешно сформирован')
                time.sleep(2)
            elif action == '5':
                df = pd.read_sql(Queries.StatsQueries.select_last_visit_date.value, conn.get_connection())
                df.to_csv('./Reports/last_visit_date.csv')
                print('Отчет успешно сформирован')
                time.sleep(2)
            elif action == '6':
                df = pd.read_sql(Queries.StatsQueries.select_most_readable_author.value, conn.get_connection())
                df.to_csv('./Reports/most_readable_author.csv')
                print('Отчет успешно сформирован')
                time.sleep(2)
            elif action == '7':
                df = pd.read_sql(Queries.StatsQueries.select_most_readable_genre.value, conn.get_connection())
                df.to_csv('./Reports/most_readable_genre.csv')
                print('Отчет успешно сформирован')
                time.sleep(2)
            elif action == '8':
                df = pd.read_sql(Queries.StatsQueries.select_favourite_genre.value, conn.get_connection())
                df.to_csv('./Reports/favourite_genre.csv')
                print('Отчет успешно сформирован')
                time.sleep(2)
            elif action == '9':
                df = pd.read_sql(Queries.StatsQueries.select_book_expired_info.value, conn.get_connection())
                df.to_csv('./Reports/book_expired_info.csv')
                print('Отчет успешно сформирован')
                time.sleep(2)

            elif action == '10':
                df = pd.read_sql(Queries.StatsQueries.select_taken_book_location.value, conn.get_connection())
                curr_list = []
                for index, row in df.iterrows():
                    try:
                        location = tools.get_location(row['city_name'], row['street_name'])
                        coordinates = tools.get_coordinates(location)
                        curr_list.append({'lat': coordinates[0], 'lon': coordinates[1]})
                    except:
                        continue
                main_df = pd.DataFrame(curr_list)

                tools.df_to_geojson(main_df)
                print('Отчет успешно сформирован')
                time.sleep(2)
            else:
                continue
        # Работа с фактами
        elif ask == '4':
            action = str(input('\nЧто вы хотите сделать с фактами\n'
                               '(A) Добавить взятие книги\n'
                               '(R) Добавить возврат книги\n'
                               '\n'
                               '(X) Вернуться назад\n'))
            if action == 'A' or action == 'a':
                params = input('\nВведите ID книги, ID пользователя через пробел\n').split()
                book_id = params[0]
                res = conn.query(Queries.DistributionQueries.check_book.value, book_id)
                if len(res[1]) == 0:
                    res = conn.query(Queries.DistributionQueries.give_book.value, params)
                    tools.print_success_or_not(res[0])
                else:
                    print("Данной книги нет в наличии!")
                    time.sleep(2)
                    continue
            elif action == 'R' or action == 'r':
                params = input('\nВведите ID Возвращаемой книги и ID пользователя через пробел\n').split()
                res = conn.query(Queries.DistributionQueries.return_book.value, params)
                tools.print_success_or_not(res[0])
                time.sleep(2)
            else:
                continue
        # Работа с адресами
        elif ask == '5':
            action = input('\nЧто вы хотите сделать с адресом\n'
                           '(A) Добавить адрес\n'
                           '(U) Изменить адрес\n'
                           '(D) Удалить адрес\n'
                           '\n'
                           '(X) Вернуться назад\n')
            if action == 'A' or action == 'a':
                city_name = input('\nВведите название города пользователя\n')
                street_name = input('\nВведите название и номер улицы пользователя\n')
                city_params = [city_name, street_name]
                res = conn.query(Queries.AddressQueries.add_address.value, city_params)
                tools.print_success_or_not(res[0])

            elif action == 'U' or action == 'u':
                city_name = input('\nВведите новое название города пользователя\n')
                street_name = input('\nВведите новое название и номер улицы пользователя\n')
                addr_id = input('\nВведите ID адреса, который вы хотите изменить\n')
                params = [city_name, street_name, addr_id]
                res = conn.query(Queries.AddressQueries.update_address.value, params)
                tools.print_success_or_not(res[0])
                time.sleep(2)
            elif action == 'D' or action == 'd':
                addr_id = input('\nВведите ID адреса, который вы хотите удалить\n')
                res = conn.query(Queries.AddressQueries.update_address.value, addr_id)
                tools.print_success_or_not(res[0])
                time.sleep(2)
            else:
                continue

        else:
            break


if __name__ == "__main__":
    main()
