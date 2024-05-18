from jiduoduo.app import app
from jiduoduo.models import User
from jiduoduo.models import VPS
from jiduoduo.models import db


def create_test_data():
    with app.app_context():
        db.drop_all()
        db.create_all()

        user = User(email='a@a.com')
        user.password = 'a'
        db.session.add(user)
        db.session.flush()

        objs = [
            VPS(
                user_id=user.id,
                name='🐔老大（纯测试用）',
                host='192.168.1.101',
                port=10001,
                user='jihaoda',
                password='jiduoduo1_password',
                identify_key='jiduoduo1_pkey',
            ),
            VPS(
                user_id=user.id,
                name='🐔老二（纯测试用）',
                host='192.168.1.102',
                port=10002,
                user='jihaoer',
                password='jiduoduo2_password',
                identify_key='jiduoduo2_pkey',
            ),
            VPS(
                user_id=user.id,
                name='🐔老三（纯测试用）',
                host='192.168.1.103',
                port=10003,
                user='jihaosan',
                password='jiduoduo3_password',
                identify_key='jiduoduo3_pkey',
            ),
        ]
        db.session.add_all(objs)
        db.session.flush()
        db.session.commit()


if __name__ == '__main__':
    create_test_data()
    app.run(debug=True, threaded=False, host='localhost', port=15000)
