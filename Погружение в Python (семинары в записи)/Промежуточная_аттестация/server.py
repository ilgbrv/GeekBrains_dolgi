import socket
import logging

logging.basicConfig(
    filename="server_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def start_server(host="127.0.0.1", port=12345):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    logging.info(f"Запуск сервера на {host}:{port}")
    server.bind((host, port))
    server.listen(5)
    logging.info(f"Сервер успешно запущен на {host}:{port}")
    print(f"Сервер запущен на {host}:{port}")

    while True:
        client, addr = server.accept()
        logging.info(f"Подключение от {addr}")
        print(f"Подключение от {addr}")

        while True:
            message = client.recv(1024).decode()
            if not message:
                break

            logging.info(f"Получено сообщение от {addr}: {message}")
            print(f"Сообщение от {addr}: {message}")

            client.send("Сообщение получено!".encode())
            logging.info(f"Сообщение отправлено обратно клиенту {addr}")

        client.close()
        logging.info(f"Подключение с {addr} завершено")


if __name__ == "__main__":
    start_server()
