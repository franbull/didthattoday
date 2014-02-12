from base import BaseTestCase
from didthattoday.models import Habit

class TestHabit(BaseTestCase):
    def test_create(self):
        h = Habit(name='woo', description='hoo')
        self.session.add(h)
        self.session.flush()
        assert(h.id is not None)

        h_from_db = self.session.query(Habit).get(h.id)
        # h and h_from_db are actually the same object in memory right now
        assert('woo' == h_from_db.name)
        assert('hoo' == h_from_db.description)
