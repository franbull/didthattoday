import simplejson

from base import IntegrationTestBase
from didthattoday.models import Step
from didthattoday.models import Habit

class TestStepViews(IntegrationTestBase):
    def create_habit(self):
        assert(self.session.query(Habit).count() == 0)
        habit = {'name': 'woo', 'description': 'hoo'}
        res = self.app.post('/habits', simplejson.dumps(habit))
        self.assertEqual(res.status_int, 200)

        res = self.app.get('/habits')
        self.assertEqual(res.status_int, 200)
        rd = res.json

        assert(1 == len(rd['habits']))
        habit = rd['habits'][0]
        assert(habit['name'] == 'woo')
        return habit['id']

    def test_steps(self):
        assert(self.session.query(Step).count() == 0)
        habit_id = self.create_habit()
        step = {'comment': 'woo', 'happened_at': '2014-03-09T04:58:25.513Z',
                'habit_id': habit_id}
        res = self.app.post('/steps', simplejson.dumps(step))
        self.assertEqual(res.status_int, 200)

        res = self.app.get('/steps')
        self.assertEqual(res.status_int, 200)
        rd = res.json

        assert(1 == len(rd['steps']))
        step = rd['steps'][0]
        assert(step['comment'] == 'woo')

        print Step.Session.query(Step).count()
        a = Step.Session.query(Step).first()
        print a.happened_at
        import pdb; pdb.set_trace()


    #def test_get_habit(self):
        #assert(self.session.query(Habit).count() == 0)
        #habit = {'name': 'woo', 'description': 'hoo'}
        #res = self.app.post('/habits', simplejson.dumps(habit))
        #self.assertEqual(res.status_int, 200)

        #res = self.app.get('/habits')
        #self.assertEqual(res.status_int, 200)
        #rd = res.json

        #assert(1 == len(rd['habits']))
        #habit = rd['habits'][0]
        #assert(habit['name'] == 'woo')

        #id = habit['id']
        #res = self.app.get('/habit/%s' % id)
        #self.assertEqual(res.status_int, 200)
        #rd = res.json
        #assert(rd['id'] == id)
        #assert(rd['name'] == 'woo')

    #def test_update_habit(self):
        #assert(self.session.query(Habit).count() == 0)
        #habit = {'name': 'woo', 'description': 'hoo'}
        #res = self.app.post('/habits', simplejson.dumps(habit))
        #self.assertEqual(res.status_int, 200)

        #res = self.app.get('/habits')
        #self.assertEqual(res.status_int, 200)
        #rd = res.json

        #assert(1 == len(rd['habits']))
        #habit = rd['habits'][0]
        #assert(habit['name'] == 'woo')

        #id = habit['id']
        #habit['name'] = 'coo'
        #res = self.app.put('/habit/%s' % id, simplejson.dumps(habit))
        #self.assertEqual(res.status_int, 200)

        #res = self.app.get('/habit/%s' % id)
        #self.assertEqual(res.status_int, 200)
        #rd = res.json
        #assert(rd['id'] == id)
        #assert(rd['name'] == 'coo')



