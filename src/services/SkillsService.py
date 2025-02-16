from typing import List, Optional
from fastapi import Depends
from sqlalchemy.orm import Session

from models.SkillsModel import Skills
from repositories.SkillsRepository import SkillsRepository
from schemas.pydantic.SkillsSchema import SkillsSchema


class SkillsService:
    skillsRepo: SkillsRepository

    def __init__(
        self, skillsRepo: SkillsRepository = Depends()
    ):
        self.skillsRepo = skillsRepo

    def create_skills(self, skills_data: SkillsSchema):
        skills = Skills(
            name=skills_data.name,
        )

        return self.skillsRepo.create(skills)

    def update_skills(
        self, skills_id: int, skills_data: SkillsSchema
    ):
        skills = Skills(
            id=skills_id,
            name=skills_data.name,
        )

        return self.skillsRepo.update(skills)

    def delete_skills(self, skills_id: int):
        skills = self.skillsRepo.get_by_id(skills_id)
        self.skillsRepo.delete(skills)

    def get_skills_by_id(self, skills_id: int):
        return self.skillsRepo.get_by_id(skills_id)

    def get_by_name(self, name: str):
        return self.skillsRepo.get_by_name(name)

    def list(
        self,
        name: Optional[str] = None,
        pageSize: Optional[int] = 100,
        startIndex: Optional[int] = 0,
    ) -> List[Skills]:
        return self.skillsRepo.list(
            name, pageSize, startIndex
        )
