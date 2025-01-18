#! /bin/bash

poetry run uvicorn src.motto_image_creator.main:app --reload