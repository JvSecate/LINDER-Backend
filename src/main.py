from fastapi import Depends, FastAPI


from configs.Environment import get_environment_variables
from metadata.Tags import Tags
from models.BaseModel import init
from routers.v1.CityRouter import CityRouter
from routers.v1.CountryRouter import CountryRouter
from routers.v1.StateRouter import StateRouter
from routers.v1.UserRouter import UserRouter
from routers.v1.JobRouter import JobRouter
from routers.v1.CompanyRouter import CompanyRouter
from routers.v1.CommentRouter import CommentRouter
from routers.v1.JobApplicationStatusRouter import JobApplicationStatusRouter
from routers.v1.JobApplicationRouter import JobApplicationRouter
from routers.v1.JobCategoryRouter import JobCategoryRouter
from routers.v1.LocationRouter import LocationRouter
from routers.v1.SkillsRouter import SkillsRouter

# Application Environment Configuration
env = get_environment_variables()

# Core Application Instance
app = FastAPI(
    title=env.APP_NAME,
    version=env.API_VERSION,
    openapi_tags=Tags,
)

# Add Routers
app.include_router(UserRouter)
app.include_router(CountryRouter)
app.include_router(StateRouter)
app.include_router(CityRouter)
app.include_router(JobRouter)
app.include_router(CompanyRouter)
app.include_router(CommentRouter)
app.include_router(JobApplicationStatusRouter)
app.include_router(JobApplicationRouter)
app.include_router(JobCategoryRouter)
app.include_router(LocationRouter)
app.include_router(SkillsRouter)

# Initialise Data Model Attributes
init()
