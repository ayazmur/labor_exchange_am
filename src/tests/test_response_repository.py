import pytest

from models.dto.response import ResponseCreateDto, ResponseUpdateDto
from tools.fixtures.jobs import JobFactory
from tools.fixtures.responses import ResponseFactory


@pytest.mark.asyncio
async def test_get_all(response_repository, sa_session):
    async with sa_session() as session:
        response = ResponseFactory.build()
        session.add(response)
        session.flush()

    all_responses = await response_repository.retrieve_many()
    assert all_responses
    assert len(all_responses) == 1

    response_from_repo = all_responses[0]

    assert response_from_repo.id == response.id
    assert response_from_repo.user_id == response.user_id
    assert response_from_repo.job_id == response.job_id
    assert response_from_repo.message == response.message


@pytest.mark.asyncio
async def test_get_by_id(response_repository, sa_session):
    async with sa_session() as session:
        response = ResponseFactory.build()
        session.add(response)
        session.flush()

    current_response = await response_repository.retrieve(id=response.id)
    assert current_response is not None
    assert current_response.id == response.id


@pytest.mark.asyncio
async def test_create(response_repository, sa_session):
    async with sa_session() as session:
        job = JobFactory.build()
        session.add(job)
        session.flush()

    response = ResponseCreateDto(
        user_id=job.user_id,
        job_id=job.id,
        message="Professional uchpochmak taster"
    )

    new_response = await response_repository.create(response_create_dto=response)
    assert new_response is not None
    assert new_response.user_id == response.user_id
    assert new_response.job_id == response.job_id
    assert new_response.message == response.message


@pytest.mark.asyncio
async def test_update(response_repository, sa_session):
    async with sa_session() as session:
        response = ResponseFactory.build()
        session.add(response)
        session.flush()

    response_update_dto = ResponseUpdateDto(message="Skilled baursak taster")
    updated_response = await response_repository.update(id=response.id, response_update_dto=response_update_dto)
    assert updated_response.id == response.id
    assert updated_response.message == "Skilled baursak taster"


@pytest.mark.asyncio
async def test_delete(response_repository, sa_session):
    async with sa_session() as session:
        response = ResponseFactory.build()
        session.add(response)
        session.flush()

    await response_repository.delete(id=response.id)
    res = await response_repository.retrieve(id=response.id)
    assert not res