import factory

from storage.sqlalchemy.tables import Response
from tools.fixtures.jobs import JobFactory
from tools.fixtures.users import UserFactory


class ResponseFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Response

    id = factory.Sequence(lambda n: n)
    user = factory.SubFactory(UserFactory)
    user_id = factory.setAtrribute("user_id")
    job = factory.SubFactory(JobFactory)
    job_id = factory.setAttribute("job_id")
    message = factory.Faker("sentence")