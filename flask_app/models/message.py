from flask_app.config.mysqlconnection import connectToMySQL


class Message:
    def __init__(self, data:dict):
        self.id = data.get('id')
        self.content = data.get('content')
        self.recipient_id = data.get('recipient_id')
        self.author = data.get('author')
        self.minutes_since_message = data.get('minutes_since_message')

    @classmethod
    def get_message_to_user(cls, data:dict) -> list:
        query = """SELECT 
                    messages_to_users.id, 
                    messages_to_users.author_id as auth_id,
                    content, 
                    CONCAT_WS(' ', users.first_name, users.last_name) AS author,
                    TIMESTAMPDIFF(MINUTE, messages_to_users.created_at, NOW()) AS minutes_since_message 
                    FROM messages_to_users 
                    JOIN users ON author_id = users.id WHERE recipient_id = %(id)s
                    ORDER BY minutes_since_message;"""
        results = connectToMySQL('private-wall').query_db(query, data)
        messages = []

        for message in results:
            messages.append(cls(message))
        return messages

    @classmethod
    def find_message_by_id(cls, data:dict) -> object:
        query = "SELECT * FROM messages_to_users WHERE id = %(id)s;"
        result = connectToMySQL('private-wall').query_db(query, data)
        return cls(result[0])

    @classmethod
    def delete_message(cls, data:dict) -> None:
        query = "DELETE FROM messages_to_users WHERE id = %(id)s;"
        connectToMySQL('private-wall').query_db(query, data)

    @classmethod
    def create_message(cls, data:dict) -> None:
        query = """INSERT INTO messages_to_users (content, author_id, recipient_id)
                    VALUES (%(content)s, %(author_id)s, %(recipient_id)s);"""
        return connectToMySQL('private-wall').query_db(query, data)