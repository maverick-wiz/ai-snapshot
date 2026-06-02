"""GET /api/countries. AISNP-19 · Owner: OMEGA"""
from fastapi import APIRouter
from app.schemas import Country

router = APIRouter(tags=["Countries"])

COUNTRIES = [
    Country(iso2="US", name="United States", flag="🇺🇸"),
    Country(iso2="CN", name="China", flag="🇨🇳"),
    Country(iso2="DE", name="Germany", flag="🇩🇪"),
    Country(iso2="JP", name="Japan", flag="🇯🇵"),
    Country(iso2="IN", name="India", flag="🇮🇳"),
    Country(iso2="GB", name="United Kingdom", flag="🇬🇧"),
    Country(iso2="FR", name="France", flag="🇫🇷"),
    Country(iso2="KR", name="South Korea", flag="🇰🇷"),
    Country(iso2="CA", name="Canada", flag="🇨🇦"),
    Country(iso2="RU", name="Russia", flag="🇷🇺"),
    Country(iso2="IT", name="Italy", flag="🇮🇹"),
    Country(iso2="BR", name="Brazil", flag="🇧🇷"),
    Country(iso2="AU", name="Australia", flag="🇦🇺"),
    Country(iso2="ES", name="Spain", flag="🇪🇸"),
    Country(iso2="MX", name="Mexico", flag="🇲🇽"),
    Country(iso2="ID", name="Indonesia", flag="🇮🇩"),
    Country(iso2="NL", name="Netherlands", flag="🇳🇱"),
    Country(iso2="SA", name="Saudi Arabia", flag="🇸🇦"),
    Country(iso2="TR", name="Turkey", flag="🇹🇷"),
    Country(iso2="CH", name="Switzerland", flag="🇨🇭"),
    Country(iso2="TW", name="Taiwan", flag="🇹🇼"),
    Country(iso2="PL", name="Poland", flag="🇵🇱"),
    Country(iso2="SE", name="Sweden", flag="🇸🇪"),
    Country(iso2="BE", name="Belgium", flag="🇧🇪"),
    Country(iso2="AR", name="Argentina", flag="🇦🇷"),
]

@router.get("/countries", response_model=list[Country])
async def get_countries():
    return COUNTRIES
