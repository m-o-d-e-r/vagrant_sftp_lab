import sys
from os import environ


def extract_servers_ip() -> list[str]:
    raw_server_list = environ.get("SFTP_SERVER_LIST", "")

    print("SFTP_SERVER_LIST got from environments")

    server_list: list[str] = list(
        filter(
            lambda x: x,
            raw_server_list.split(" ")
        )
    )
    if not server_list:
        print("variable SFTP_SERVER_LIST should be provided")
        sys.exit(0)

    print(server_list)
    return server_list
