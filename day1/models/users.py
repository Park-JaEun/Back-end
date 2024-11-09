from sqlmodel import Field, SQLModel

class MenuBase(SQLModel):
	menuname: str
	one_time_offer: int

class Menu(MenuBase, table=True):
	id: int = Field(default=None, primary_key=True)