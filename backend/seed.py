"""
Seed script to populate the database with demo data for hackathon presentations.
"""
import asyncio
from datetime import date, timedelta
from uuid import uuid4
from app.database import AsyncSessionLocal, engine, Base
from app.core.security import hash_password
from app.models import User, Vineyard, Block, Observation


async def seed():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        admin_id = uuid4()
        admin = User(
            id=admin_id,
            name="Jeffrey Moepi",
            email="jeffrey@vinemind.ai",
            password_hash=hash_password("demo1234"),
            role="admin",
        )
        db.add(admin)

        vineyard_id = uuid4()
        vineyard = Vineyard(
            id=vineyard_id,
            name="Stellenbosch Estate",
            owner_id=admin_id,
            location_lat=-33.9321,
            location_lon=18.8602,
            area_hectares=120.0,
        )
        db.add(vineyard)

        blocks_data = [
            {"name": "Block A12", "cultivar": "Cabernet Sauvignon", "area_ha": 8.5, "planting_year": "2018"},
            {"name": "Block B05", "cultivar": "Merlot", "area_ha": 6.2, "planting_year": "2016"},
            {"name": "Block C09", "cultivar": "Pinotage", "area_ha": 10.1, "planting_year": "2020"},
            {"name": "Block D03", "cultivar": "Chenin Blanc", "area_ha": 7.8, "planting_year": "2015"},
            {"name": "Block E07", "cultivar": "Shiraz", "area_ha": 9.3, "planting_year": "2019"},
        ]

        block_ids = []
        for bd in blocks_data:
            block_id = uuid4()
            block_ids.append(block_id)
            block = Block(
                id=block_id,
                vineyard_id=vineyard_id,
                name=bd["name"],
                cultivar=bd["cultivar"],
                area_ha=bd["area_ha"],
                planting_year=bd["planting_year"],
            )
            db.add(block)

        await db.commit()

        phenology_stages = ["veraison", "flowering", "fruit_set", "ripening", "bud_break"]
        today = date.today()

        for i, block_id in enumerate(block_ids):
            for day_offset in range(14):
                obs_date = today - timedelta(days=13 - day_offset)
                obs = Observation(
                    block_id=block_id,
                    observation_date=obs_date,
                    eta=3.5 + (i * 0.3) + (day_offset * 0.1),
                    eto=5.8 + (day_offset * 0.05),
                    kc=0.85 + (i * 0.02),
                    ndvi=0.65 + (i * 0.03) - (day_offset * 0.005),
                    soil_moisture=45.0 - (day_offset * 1.5) + (i * 2.0),
                    temperature=22.0 + (day_offset * 0.3),
                    rainfall=0.0 if day_offset < 12 else 2.5,
                    phenology_stage=phenology_stages[i],
                    data_source="et-geo-sentinel2",
                )
                db.add(obs)

        await db.commit()
        print("Seed data created successfully.")
        print("Demo login: jeffrey@vinemind.ai / demo1234")


if __name__ == "__main__":
    asyncio.run(seed())
