from dataclasses import asdict

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, status

from dependencies import get_current_user
from dependencies.containers import RepositoriesContainer
from models import User
from repositories import JobRepository, ResponseRepository
from web.schemas import ResponseSchema, ResponseCreateSchema, ResponseUpdateSchema
from models.dto.response import ResponseCreateDto, ResponseUpdateDto

router = APIRouter(prefix="/responses", tags=["responses"])

@router.get("")
@inject
async def read_responses(
    limit: int = 100,
    skip: int = 0,
    response_repository: ResponseRepository = Depends(
        Provide[RepositoriesContainer.response_repository]
    ),
) -> list[ResponseSchema]:

    response_models = await response_repository.retrieve_many(limit, skip)

    response_schemas = []
    for model in response_models:
        response_schemas.append(
            ResponseSchema(
                id=model.id,
                user_id=model.user_id,
                job_id=model.job_id,
                message=model.message,
            )
        )
    return response_schemas


@router.get("/{job_id}")
@inject
async def get_responses_by_job_id(
    job_id: int,
    response_repository: ResponseRepository = Depends(
        Provide[RepositoriesContainer.response_repository]
    ),
    job_repository: JobRepository = Depends(
        Provide[RepositoriesContainer.job_repository]
    ),
    current_user: User = Depends(get_current_user),
) -> list[ResponseSchema]:

    job_model = await job_repository.retrieve(id=job_id)
    if job_model and job_model.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав"
        )

    response_models = await response_repository.retrieve_many()

    response_schemas = []
    for model in response_models:
        if model.job_id == job_id:
            response_schema = ResponseSchema(
                id=model.id,
                user_id=model.user_id,
                job_id=model.job_id,
                message=model.message,
            )
            response_schemas.append(response_schema)

    return response_schemas


@router.post("")
@inject
async def create_response(
    response_create_schema: ResponseCreateSchema,
    response_repository: ResponseRepository = Depends(
        Provide[RepositoriesContainer.response_repository]
    ),
    current_user: User = Depends(get_current_user),
) -> ResponseSchema:

    if current_user.is_company:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Откликаться могут только соискатели",
        )

    response_create_dto = ResponseCreateDto(
        user_id=current_user.id, **response_create_schema.model_dump()
    )

    response = await response_repository.create(response_create_dto)

    return ResponseSchema(**asdict(response))


@router.put("")
@inject
async def update_response(
    response_update_schema: ResponseUpdateSchema,
    response_repository: ResponseRepository = Depends(
        Provide[RepositoriesContainer.response_repository]
    ),
    current_user: User = Depends(get_current_user),
) -> ResponseSchema:

    existing_response = await response_repository.retrieve(id=response_update_schema.id)
    if existing_response and existing_response.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав"
        )

    try:
        response_update_dto = ResponseUpdateDto(message=response_update_schema.message)

        updated_response = await response_repository.update(
            existing_response.id, response_update_dto
        )

    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Отклик не найден"
        )

    return ResponseSchema(**asdict(updated_response))


@router.delete("/{id}")
@inject
async def delete(
    id: int,
    response_repository: RepositoriesContainer = Depends(
        Provide[RepositoriesContainer.response_repository]
    ),
    current_user: User = Depends(get_current_user),
) -> ResponseSchema:

    existing_response = await response_repository.retrieve(id=id)
    if existing_response and existing_response.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Недостаточно прав"
        )

    try:
        deleted_response = await response_repository.delete(id=id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Отклик не найден"
        )

    return ResponseSchema(**asdict(deleted_response))