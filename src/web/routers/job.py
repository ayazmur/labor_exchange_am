from dataclasses import asdict

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_current_user
from dependencies.containers import RepositoriesContainer
from models import User
from repositories import JobRepository
from web.schemas import JobSchema, JobCreateSchema, JobUpdateSchema
from models.dto.job import JobCreateDto, JobUpdateDto

router = APIRouter(prefix="/jobs", tags=["jobs"])

@router.get("")
@inject
async def read_jobs(
    limit: int = 100,
    skip: int = 0,
    job_repository: JobRepository = Depends(Provide[RepositoriesContainer.job_repository]),
) -> list[JobSchema]:
    jobs_model = await job_repository.retrieve_many(limit, skip)

    jobs_schema = []
    for model in jobs_model:
        jobs_schema.append(
            JobSchema(
                id=model.id,
                user_id=model.user_id,
                title=model.title,
                description=model.description,
                salary_from=model.salary_from,
                salary_to=model.salary_to,
                is_active=model.is_active
            )
        )
    return jobs_schema


@router.post("")
@inject
async def create_job(
    job_create_schema: JobCreateSchema,
    job_repository: JobRepository = Depends(
        Provide[RepositoriesContainer.job_repository]
    ),
    current_user: User = Depends(get_current_user),
) -> JobSchema:

    if not current_user.is_company:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Недостаточно прав"
        )

    job_create_dto = JobCreateDto(
        user_id=current_user.id, **job_create_schema.model_dump()
    )

    job = await job_repository.create(job_create_dto)

    return JobSchema(**asdict(job))

@router.put("")
@inject
async def update_job(
    job_update_schema: JobUpdateSchema,
    job_repository: JobRepository = Depends(
        Provide[RepositoriesContainer.job_repository]
    ),
    current_user: User = Depends(get_current_user),
) -> JobSchema:

    existing_job = await job_repository.retrieve(id=job_update_schema.id)
    if existing_job and existing_job.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Недостаточно прав"
        )

    try:
        job_update_dto = JobUpdateDto(
            title=job_update_schema.title,
            description=job_update_schema.description,
            salary_from=job_update_schema.salary_from,
            salary_to=job_update_schema.salary_to,
            is_active=job_update_schema.is_active,
        )

        updated_job = await job_repository.update(job_update_schema.id, job_update_dto)

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена"
        )

    return JobSchema(**asdict(updated_job))


@router.delete("/{id}")
@inject
async def delete(
    id: int,
    job_repository: RepositoriesContainer = Depends(
        Provide[RepositoriesContainer.job_repository]
    ),
    current_user: User = Depends(get_current_user),
) -> JobSchema:

    existing_job = await job_repository.retrieve(id=id)
    if existing_job and existing_job.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Недостаточно прав"
        )

    try:
        deleted_job = await job_repository.delete(id=id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Вакансия не найдена"
        )

    return JobSchema(**asdict(deleted_job))