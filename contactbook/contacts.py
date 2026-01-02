from uuid import uuid4
from typing import Optional
from dataclasses import dataclass, field


@dataclass
class Contact:
    first_name: str
    last_name: str
    phone_number: str
    id: str = field(default_factory=lambda: str(uuid4()))
    email: Optional[str] = None


    def get_full_name(self) -> str:
        return f"{self.first_name.capitalize()} {self.last_name.capitalize()}"

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone_number,
            "email": self.email,
        }

    @staticmethod
    def from_dict(d: dict) -> "Contact":
        return Contact(
            id=d["id"],
            first_name=d["first_name"],
            last_name=d["last_name"],
            phone_number=d["phone"],
            email=d.get("email"),
        )
