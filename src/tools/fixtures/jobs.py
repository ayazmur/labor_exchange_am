from datetime import datetime

import factory

from storage.sqlalchemy.tables import Job
from tools.fixtures.users import UserFactory


class JobFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Job

    id = factory.Sequence(lambda n: n)
    user = factory.SubFactory(UserFactory)
    user_id = factory.setAttribute("user_id")
    title = factory.Faker("job")
    description = factory.Faker("sentence")
    salary_from = factory.Faker("numerify", text="###000")
    salary_to = factory.Faker("numerify", text="###000")
    is_active = factory.Faker("pybool")
    created_at = factory.LazyFunction(datetime.utcnow)