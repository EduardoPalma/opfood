import unittest
from api.init_app import init_run
from api.optimizer.crossover import SinglePointCrossover
from api.optimizer.mutation import MutationOnePoint
from api.optimizer.op_food import OptimizerFood
from api.optimizer.selection import SelectionOnePoint


class MyTestCase(unittest.IsolatedAsyncioTestCase):

    async def asyncSetUp(self):
        self.universe_foods = []
        await init_run(self.universe_foods)
        self.selection = SelectionOnePoint()
        self.crossover = SinglePointCrossover()
        self.mutation = MutationOnePoint()
        self.optimizer_food = OptimizerFood(self.universe_foods, self.selection, self.crossover, self.mutation)

    async def test_something(self):
        self.assertEqual(True, True)  # add assertion here


if __name__ == '__main__':
    unittest.main()
