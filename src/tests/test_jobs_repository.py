import pytest

from models.dto.job import JobCreateDto, JobUpdateDto
from tools.fixtures.jobs import JobFactory
from tools.fixtures.users import UserFactory


@pytest.mark.asyncio
async def test_get_all(job_repository, sa_session):
    async with sa_session() as session:
        job = JobFactory.build()
        session.add(job)
        session.flush()

    all_jobs = await job_repository.retrieve_many()
    assert all_jobs
    assert len(all_jobs) == 1

    job_from_repo = all_jobs[0]

    assert job_from_repo.id == job.id
    assert job_from_repo.user_id == job.user_id
    assert job_from_repo.title == job.title
    assert job_from_repo.description == job.description
    assert job_from_repo.salary_from == job.salary_from
    assert job_from_repo.salary_to == job.salary_to
    assert job_from_repo.is_active == job.is_active


@pytest.mark.asyncio
async def test_get_by_id(job_repository, sa_session):
    async with sa_session() as session:
        job = JobFactory.build()
        session.add(job)
        session.flush()

    current_job = await job_repository.retrieve(id=job.id)
    assert current_job is not None
    assert current_job.id == job.id


@pytest.mark.asyncio
async def test_create(job_repository, sa_session):
    async with sa_session() as session:
        user = UserFactory.build(is_company=True)
        session.add(user)
        session.flush()

    job = JobCreateDto(
        user_id=user.id,
        title="Chak-Chak",
        description="with honey",
        salary_from="10000",
        salary_to="200000",
        is_active=True
    )

    new_job = await job_repository.create(job_create_dto=job)
    assert new_job is not None
    assert new_job.user_id == job.user_id
    assert new_job.title == job.title
    assert new_job.description == job.description
    assert new_job.salary_from == job.salary_from
    assert new_job.salary_to == job.salary_to
    assert new_job.is_active == job.is_active


@pytest.mark.asyncio
async def test_update(job_repository, sa_session):
    async with sa_session() as session:
        job = JobFactory.build()
        session.add(job)
        session.flush()

    job_update_dto = JobUpdateDto(title="Baursak")
    updated_job = await job_repository.update(id=job.id, job_update_dto=job_update_dto)
    assert job.id == updated_job.id
    assert updated_job.title == "Baursak"


@pytest.mark.asyncio
async def test_delete(job_repository, sa_session):
    async with sa_session() as session:
        job = JobFactory.build()
        session.add(job)
        session.flush()

    await job_repository.delete(id=job.id)
    res = await job_repository.retrieve(id=job.id)
    assert not res