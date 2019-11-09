"""Module to define the database configuration"""
import os

DATABASE = {
    'CONNECTION': os.getenv('DB_CONNECTION_URL')
}
