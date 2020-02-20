"""Module to define the global setting of the API"""
import os

API = {
    'ENV': os.getenv('API_ENV', 'local'),
    'PORT': os.getenv('API_PORT', 7777),
    'CORS': os.getenv('API_CORS', False),
}
