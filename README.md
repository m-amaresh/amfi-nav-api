# AMFI NAV API

A RESTful API built with FastAPI to provide Net Asset Value (NAV) data for mutual funds.
https://amfi-nav.azurewebsites.net

[![Build and deploy Python app to Azure Web App - amfi-nav](https://github.com/m-amaresh/amfi-nav-api/actions/workflows/main_amfi-nav.yml/badge.svg)](https://github.com/m-amaresh/amfi-nav-api/actions/workflows/main_amfi-nav.yml)

## Overview

The AMFI NAV API allows users to retrieve NAV data for mutual funds based on scheme codes, ISINs, scheme names, and specific dates. The API is built using FastAPI, a modern, fast (high-performance), web framework for building APIs with Python 3.7+.

## Features

- Retrieve NAV data by scheme code, ISIN, scheme name, and date.
- Pagination support for managing large result sets.

## API Endpoints

### Retrieve NAV Data
GET /navdata/
Parameters:

scheme_code: (Required) Scheme code (regex: ^\d{6}$)
isin: (Optional) ISIN code (regex: ^[A-Za-z0-9]{12}$)
scheme_name: (Optional) Scheme name
date: (Optional) Specific date for NAV data
page: (Optional) Page number for pagination (default: 1)
page_size: (Optional) Number of items per page (default: 10, max: 100)
Example:

```
curl -X 'GET' \
  'https://amfi-nav.azurewebsites.net/navdata/?scheme_code=119551&date=2024-01-15' \
  -H 'accept: application/json'
```
## API Docs
[Swagger](https://amfi-nav.azurewebsites.net/docs)
[Redoc](https://amfi-nav.azurewebsites.net/redoc)


## License
This project is licensed under the MIT License.

## Acknowledgments
FastAPI: https://fastapi.tiangolo.com/
MongoDB: https://www.mongodb.com/