#!/bin/bash
cd services/api_gateway && uvicorn app:app --host 0.0.0.0 --port $PORT
