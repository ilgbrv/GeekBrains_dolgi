import socket
import logging

logging.basicConfig(
    filename="client_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def start_client(host="127.0.0.1", port=12345):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    logging.info(f"Подключение к серверу {host}:{port}")
    client.connect((host, port))
    logging.info(f"Успешно подключено к серверу {host}:{port}")
    print("Подключено к серверу.")

    while True:
        msg = input("Введите сообщение (или 'exit' для выхода): ")
        if msg.lower() == "exit":
            logging.info("Клиент закрыл соединение.")
            break

        client.send(msg.encode())
        logging.info(f"Сообщение отправлено: {msg}")

        response = client.recv(1024).decode()
        print("Ответ сервера:", response)
        logging.info(f"Ответ от сервера: {response}")

    client.close()
    logging.info("Соединение закрыто.")


if __name__ == "__main__":
    start_client()
