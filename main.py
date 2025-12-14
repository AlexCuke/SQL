import psycopg2

conn = psycopg2.connect(database="alexdb", user="postgres", password="1")


def create_db():
    with conn, conn.cursor() as cur:
        # На всякий случай удалим, если уже есть
        cur.execute("""
            DROP TABLE IF EXISTS phones;
        """)
        cur.execute("""
            DROP TABLE IF EXISTS clients;
        """)
        # Создаем таблицы
        cur.execute("""
            CREATE TABLE clients (
                id          SERIAL PRIMARY KEY,
                first_name  VARCHAR(50) NOT NULL,
                last_name   VARCHAR(50) NOT NULL,
                email       VARCHAR(100) UNIQUE NOT NULL
            );
        """)
        cur.execute("""
            CREATE TABLE phones (
                id          SERIAL PRIMARY KEY,
                client_id   INTEGER NOT NULL REFERENCES clients(id) ON DELETE CASCADE,
                phone       VARCHAR(30) NOT NULL
            );
        """)


def create_client(first_name, last_name, email):
    with conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO clients(first_name, last_name, email)
            VALUES (%s, %s, %s)
            RETURNING id;
        """, (first_name, last_name, email))
        client_id = cur.fetchone()[0]
        return client_id


def add_phone(client_id, phone):
    with conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO phones(client_id, phone)
            VALUES (%s, %s);
        """, (client_id, phone))


def update_client(client_id, first_name=None, last_name=None, email=None):
    with conn, conn.cursor() as cur:
        fields = []
        params = []

        if first_name is not None:
            fields.append("first_name = %s")
            params.append(first_name)
        if last_name is not None:
            fields.append("last_name = %s")
            params.append(last_name)
        if email is not None:
            fields.append("email = %s")
            params.append(email)

        if not fields:
            return  # ничего не обновляем

        query = f"""
            UPDATE clients
            SET {', '.join(fields)}
            WHERE id = %s
            RETURNING id, first_name, last_name, email;
        """
        params.append(client_id)

        cur.execute(query, tuple(params))
        return cur.fetchone()


def delete_phone(client_id, phone):
    """Удалить конкретный телефон клиента."""
    with conn, conn.cursor() as cur:
        cur.execute("""
            DELETE FROM phones
            WHERE client_id = %s AND phone = %s
            RETURNING id, client_id, phone;
        """, (client_id, phone))
        return cur.fetchone()  # вернет удаленную строку или None


def del_client(client_id, first_name=None, last_name=None, email=None):
    with conn, conn.cursor() as cur:
        conditions = ["id = %s"]
        params = [client_id]

        if first_name is not None:
            conditions.append("first_name = %s")
            params.append(first_name)
        if last_name is not None:
            conditions.append("last_name = %s")
            params.append(last_name)
        if email is not None:
            conditions.append("email = %s")
            params.append(email)

        query = f"""
            DELETE FROM clients
            WHERE {' AND '.join(conditions)}
            RETURNING id, first_name, last_name, email;
        """

        cur.execute(query, tuple(params))
        return cur.fetchone()  # вернёт удалённого клиента или None


def find_client(first_name=None, last_name=None, email=None, phone=None):
    with conn, conn.cursor() as cur:
        query = """
            SELECT c.id, c.first_name, c.last_name, c.email, p.phone
            FROM clients c
            LEFT JOIN phones p ON p.client_id = c.id
            WHERE 1=1
        """
        params = []

        if first_name is not None:
            query += " AND c.first_name = %s"
            params.append(first_name)

        if last_name is not None:
            query += " AND c.last_name = %s"
            params.append(last_name)

        if email is not None:
            query += " AND c.email = %s"
            params.append(email)

        if phone is not None:
            query += " AND p.phone = %s"
            params.append(phone)

        cur.execute(query, tuple(params))
        return cur.fetchall()  # список кортежей (клиент + телефон)


# ===== Демонстрация работы =====
if __name__ == "__main__":
    # Создаем структуру БД
    create_db()

    # Добавляем клиентов
    client_id1 = create_client('Иван', 'Иванов', 'ivan@example.com')
    client_id2 = create_client('Петр', 'Петров', 'petr@example.com')

    print("Создан клиент 1 с id:", client_id1)
    print("Создан клиент 2 с id:", client_id2)

    # Добавляем телефоны клиентам
    add_phone(client_id1, "+7-900-111-11-11")
    add_phone(client_id1, "+7-900-222-22-22")
    add_phone(client_id2, "+7-900-333-33-33")

    # Ищем по имени
    print("Поиск по имени Иван:")
    for row in find_client(first_name="Иван"):
        print(row)

    # Ищем по телефону
    print("Поиск по телефону +7-900-333-33-33:")
    for row in find_client(phone="+7-900-333-33-33"):
        print(row)

    # Обновляем данные клиента
    print("Обновление клиента Иванов -> Сидоров:")
    updated = update_client(client_id1, last_name="Сидоров", email="ivan.sidorov@example.com")
    print("После обновления:", updated)

    # Удаляем один телефон клиента 1
    print("Удаляем телефон +7-900-222-22-22 у клиента 1")
    deleted_phone = delete_phone(client_id1, "+7-900-222-22-22")
    print("Удален телефон:", deleted_phone)

    # Проверяем, какие телефоны остались у клиента 1
    print("Телефоны клиента 1 после удаления телефона:")
    for row in find_client(email="ivan.sidorov@example.com"):
        print(row)

    # Удаляем клиента 2 целиком (его телефоны удалятся каскадно)
    print("Удаляем клиента 2:")
    deleted_client = del_client(client_id2)
    print("Удален клиент:", deleted_client)

    # Проверяем, что клиента 2 больше нет
    print("Пробуем найти клиента 2 по email petr@example.com:")
    print(find_client(email="petr@example.com"))

    conn.close()