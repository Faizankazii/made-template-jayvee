#!/bin/bash
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo "${YELLOW}Fething Airbnb datasets...${NC}"
curl -L -o airbnb_data.zip\
    https://www.kaggle.com/api/v1/datasets/download/kritikseth/us-airbnb-open-data

echo "${YELLOW}Fething Us citites datasets...${NC}"
curl -L -o uscities.zip https://simplemaps.com/static/data/us-cities/1.79/basic/simplemaps_uscities_basicv1.79.zip

echo "${YELLOW}Unzipping...${NC}"
unzip -o airbnb_data.zip -d airbnb_data
unzip -o uscities.zip -d uscities
echo "${GREEN}Process Completed succesfully.${NC}"

echo "${YELLOW}Starting python script.${NC}"
python fetch_process_data.py
