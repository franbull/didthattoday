from base import BaseTestCase
from didthattoday.models import User
from didthattoday.models import Group
from didthattoday.models import groupfinder

class TestUser(BaseTestCase):
    def test_create(self):
        u = User(login='woo', password='hoo')
        self.session.add(u)
        self.session.flush()
        assert(u.id is not None)

        u_from_db = User.from_login('woo')
        assert('woo' == u_from_db.login)
        # because it should be hashed
        assert('hoo' != u_from_db.password)
        assert(u_from_db.validate_password('hoo'))

class TestGroup(BaseTestCase):
    def test_create(self):
        g = Group(name='admin')
        u1 = User(login='admin1', password='a', groups=[g])
        u2 = User(login='admin2', password='a', groups=[g])
        u3 = User(login='normal', password='a')

        self.session.add_all([g, u1, u2, u3])
        self.session.flush()
        assert(groupfinder(u1.id, None) == ['admin'])
        assert(groupfinder(u2.id, None) == ['admin'])
        assert(groupfinder(u3.id, None) == [])
