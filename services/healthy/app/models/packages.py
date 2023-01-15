from pydantic import BaseModel


class Packages(BaseModel):
    packages_names_list: list
