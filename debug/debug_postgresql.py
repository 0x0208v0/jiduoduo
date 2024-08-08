# pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com psycopg2-binary==2.9.9

import psycopg2


def main():
    host = ''
    database = ''
    user = ''
    password = ''
    port = 5432
    conn = psycopg2.connect(
        database=database,
        host=host,
        user=user,
        password=password,
        port=port,
    )

    print(f'server_version={conn.info.server_version}')


if __name__ == "__main__":
    main()
