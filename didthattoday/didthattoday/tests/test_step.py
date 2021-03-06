from base import BaseTestCase
from didthattoday.models import Step
from didthattoday.models import Habit
from didthattoday.models import User

class TestStep(BaseTestCase):
    def test_create(self):
        u = User('a', 'b')
        self.session.add(u)
        self.session.flush()
        h = Habit(name='woo', description='hoo', userid=u.id)
        s = Step(habit=h)
        self.session.add(h)
        self.session.add(s)
        self.session.flush()
        assert(h.id is not None)
        assert(s.id is not None)
        assert(s.habit_id == h.id)

        assert(s.comment is None)
        assert(s.happened_at is not None)
        assert(s.habit.name == 'woo')

