from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class DeviceModel(Base):
    __tablename__ = "device_models"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    model_id: Mapped[str] = mapped_column(String(100), unique=True)
    model_series: Mapped[str] = mapped_column(String(100))

    device_type_id: Mapped[int] = mapped_column(
        ForeignKey("device_types.id")
    )

    vendor_id: Mapped[int] = mapped_column(
        ForeignKey("vendors.id")
    )

    rack_units: Mapped[int | None] = mapped_column(nullable=True)

    part_number: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    body_colour: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    front_image: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    rear_image: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    left_image: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    right_image: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    top_image: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    bottom_image: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    glb_path: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True,
    )

    status: Mapped[str] = mapped_column(
        String(20),
        default="draft",
        nullable=False,
    )