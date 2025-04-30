from dataclasses import dataclass


@dataclass
class Response:
    """
    Ответ на вакансию
    """
    id: int
    job_id: int
    user_id: int
    message: str
