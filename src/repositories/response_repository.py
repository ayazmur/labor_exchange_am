from contextlib import AbstractContextManager
from http.client import responses
from typing import Callable

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from interfaces import IRepositoryAsync
from models import Job as JobModel
from models import Response as ResponseModel
from models import User as UserModel
from storage.sqlalchemy.tables import Response
from web.schemas import ResponseCreateSchema, ResponseUpdateSchema


# job_id: int
# user_id: int
# message: str
class ResponseRepository(IRepositoryAsync):
    def __init__(self, session: Callable[..., AbstractContextManager[Session]]):
        self.session = session

    async def create(self, response_create_dto: ResponseCreateSchema) -> UserModel:
        response = Response(
            user_id = response_create_dto.user_id,
            job_id=response_create_dto.job_id,
            message = response_create_dto.message
        )
        async with self.session() as session:

            session.add(response)
            await session.commit()
            await session.refresh(response)

        return self.__to_response_model(response_from_db=response, include_relations=False)

    async def retrieve(self, include_relations: bool = False, **kwargs) -> ResponseModel:
        async with self.session() as session:
            query = select(Response).filter_by(**kwargs).limit(1)
            res = await session.execute(query)
            response_from_db = res.scalars().first()

        response_model = self.__to_response_model(
            response_from_db=response_from_db
        )
        return response_model

    async def retrieve_many(
        self, limit: int = 100, skip: int = 0, include_relations: bool = False
    ) -> list[ResponseModel]:
        async with self.session() as session:
            query = select(Response).limit(limit).offset(skip)
            if include_relations:
                query = select(Response).limit(limit)

            res = await session.execute(query)
            response_from_db = res.scalars().all()

        responses_model = []
        for response in response_from_db:
            model = self.__to__model(response_from_db=response)
            responses_model.append(model)

        return responses_model

    async def update(self, id: int, response_update_dto: ResponseUpdateSchema) -> ResponseModel:
        async with self.session() as session:
            query = select(Response).filter_by(id=id).limit(1)
            res = await session.execute(query)
            response_from_db = res.scalars().first()

            if not response_from_db:
                raise ValueError("Запрос не найден")

            # job_id: int
            # user_id: int
            # message: str
            job_id = response_update_dto.job_id if response_update_dto.job_id is not None else response_from_db.job_id
            user_id = response_update_dto.user_id if response_update_dto.user_id is not None else response_from_db.user_id
            message = response_update_dto.message if response_update_dto.message is not None else response_from_db.message



            response_from_db.job_id = job_id
            response_from_db.user_id = user_id
            response_from_db.message = message

            session.add(response_from_db)
            await session.commit()
            await session.refresh(response_from_db)

        new_response = self.__to_response_model(response_from_db)
        return new_response

    async def delete(self, id: int):
        async with self.session() as session:
            query = select(Response).filter_by(id=id).limit(1)
            res = await session.execute(query)
            response_from_db = res.scalars().first()

            if response_from_db:
                await session.delete(response_from_db)
                await session.commit()
            else:
                raise ValueError("Запрос не найден")

        return self.__to_response_model(response_from_db)

    @staticmethod
    def __to_response_model(response_from_db: Response) -> ResponseModel:
        response_model = None

        if response_from_db:
            response_model = ResponseModel(
                id = response_from_db.id,
                user_id = response_from_db.user_id,
                job_id=response_from_db.job_id,
                message=response_from_db.message
            )

        return response_model
