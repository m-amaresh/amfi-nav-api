# main.py
from fastapi import FastAPI, HTTPException, Query
from typing import Optional
from database import collection
import logging

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.get("/navdata/")
async def get_nav_data(
    scheme_code: str = Query(..., regex=r"^\d{6}$"),
    isin: Optional[str] = Query(None, regex=r"^[A-Za-z0-9]{12}$"),
    scheme_name: Optional[str] = None,
    date: Optional[str] = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, le=100)
):
    query = {"scheme_code": scheme_code}

    if isin:
        query["$or"] = [{"isin_div_payout": isin}, {"isin_div_reinvestment": isin}]
    elif scheme_name:
        query["scheme_name"] = scheme_name

    result = collection.find_one(query, projection={"scheme_code": 1, "isin_div_payout": 1, "isin_div_reinvestment": 1,
                                                     "fund_house": 1, "scheme_type": 1, "scheme_name": 1, "nav_data": 1})

    if not result:
        raise HTTPException(status_code=404, detail="Data not found")

    nav_data = result.get("nav_data", [])

    start_idx = (page - 1) * page_size
    end_idx = start_idx + page_size
    nav_data = nav_data[start_idx:end_idx]

    if date:
        nav_entry = next((nav for nav in nav_data if nav["date"] == date), None)
        if nav_entry:
            response_data = {
                "scheme_code": result["scheme_code"],
                "isin_div_payout": result["isin_div_payout"],
                "isin_div_reinvestment": result["isin_div_reinvestment"],
                "fund_house": result["fund_house"],
                "scheme_type": result["scheme_type"],
                "scheme_name": result["scheme_name"],
                "nav_date": nav_entry["date"],
                "net_asset_value": nav_entry["net_asset_value"]
            }
            return response_data
        else:
            latest_nav_entry = nav_data[-1]
            raise HTTPException(
                status_code=404,
                detail=f"NAV data not available for the specified date. Latest NAV data on {latest_nav_entry['date']}: "
                       f"NAV: {latest_nav_entry['net_asset_value']}"
            )

    latest_nav_entry = nav_data[-1]
    response_data = {
        "scheme_code": result["scheme_code"],
        "isin_div_payout": result["isin_div_payout"],
        "isin_div_reinvestment": result["isin_div_reinvestment"],
        "fund_house": result["fund_house"],
        "scheme_type": result["scheme_type"],
        "scheme_name": result["scheme_name"],
        "nav_date": latest_nav_entry["date"],
        "net_asset_value": latest_nav_entry["net_asset_value"]
    }

    logger.info(f"Request processed for scheme_code={scheme_code}, isin={isin}, scheme_name={scheme_name}, date={date}")

    return response_data