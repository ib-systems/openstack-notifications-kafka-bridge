#!/bin/bash
source .venv/Scripts/activate
faststream run main:app --reload "$@"