import simplejson

from base import IntegrationTestBase

class TestHabitViews(IntegrationTestBase):
    def test_habits(self):
        habit = {'name': 'woo', 'description': 'hoo'}
        res = self.app.post('/habit', simplejson.dumps(habit))
        self.assertEqual(res.status_int, 200)

        res = self.app.get('/habits')
        self.assertEqual(res.status_int, 200)
        rd = res.json

        assert(1 == len(rd['habits']))
        habit = rd['habits'][0]
        assert(habit['name'] == 'woo')
