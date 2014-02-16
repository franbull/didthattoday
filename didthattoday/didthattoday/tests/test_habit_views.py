import simplejson

from base import IntegrationTestBase
from didthattoday.models import Habit

class TestHabitViews(IntegrationTestBase):
    def test_habits(self):
        assert(self.session.query(Habit).count() == 0)
        habit = {'name': 'woo', 'description': 'hoo'}
        res = self.app.post('/habit', simplejson.dumps(habit))
        self.assertEqual(res.status_int, 200)

        res = self.app.get('/habits')
        self.assertEqual(res.status_int, 200)
        rd = res.json

        assert(1 == len(rd['habits']))
        habit = rd['habits'][0]
        assert(habit['name'] == 'woo')

    def test_get_habit(self):
        assert(self.session.query(Habit).count() == 0)
        habit = {'name': 'woo', 'description': 'hoo'}
        res = self.app.post('/habit', simplejson.dumps(habit))
        self.assertEqual(res.status_int, 200)

        res = self.app.get('/habits')
        self.assertEqual(res.status_int, 200)
        rd = res.json

        assert(1 == len(rd['habits']))
        habit = rd['habits'][0]
        assert(habit['name'] == 'woo')

        id = habit['id']
        res = self.app.get('/habit/%s' % id)
        self.assertEqual(res.status_int, 200)
        rd = res.json
        assert(rd['id'] == id)
        assert(rd['name'] == 'woo')

    def test_update_habit(self):
        assert(self.session.query(Habit).count() == 0)
        habit = {'name': 'woo', 'description': 'hoo'}
        res = self.app.post('/habit', simplejson.dumps(habit))
        self.assertEqual(res.status_int, 200)

        res = self.app.get('/habits')
        self.assertEqual(res.status_int, 200)
        rd = res.json

        assert(1 == len(rd['habits']))
        habit = rd['habits'][0]
        assert(habit['name'] == 'woo')

        id = habit['id']
        habit['name'] = 'coo'
        res = self.app.post('/habit/%s' % id, simplejson.dumps(habit))
        self.assertEqual(res.status_int, 200)

        res = self.app.get('/habit/%s' % id)
        self.assertEqual(res.status_int, 200)
        rd = res.json
        assert(rd['id'] == id)
        assert(rd['name'] == 'coo')



