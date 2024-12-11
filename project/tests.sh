#!/bin/bash
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[0;33m'
NC='\033[0m'

echo -e "${YELLOW}Installing Python dependencies from requirements.txt....${NC}"
pip install -r requirements.txt

echo "${YELLOW}Executing pipeline...${NC}"
sh pipeline.sh

echo "${YELLOW}Running tests...${NC}"

echo "${YELLOW}Testcase 1 : Checking if airbnb data exists..${NC}"
if [ -f "../data/airbnb_data/AB_US_2020.csv" ]; then
    echo "${GREEN}Testcase 1 Passed: airbnb data exists.${NC}"
else
    echo "${RED}Testcase 1 Failed: airbnb data does not exist. Exiting....${NC}"
    exit 1
fi

echo "${YELLOW}Testcase 2 : Checking if cities data exists..${NC}"
if [ -f "../data/uscities/uscities.csv" ]; then
    echo "${GREEN}Testcase 2 Passed: cities data exists.${NC}"
else
    echo "${RED}Testcase 2 Failed: cities data does not exist. Exiting....${NC}"
    exit 1
fi

echo "${YELLOW}Testcase 3 : Checking if final output file exists..${NC}"
if [ -f "../data/Final_data.csv" ]; then
    echo "${GREEN}Testcase 3 Passed: Final_data.csv exists.${NC}"
else
    echo "${RED}Testcase 3 Failed: Final_data.csv does not exist. Exiting....${NC}"
    exit 1
fi

echo "${YELLOW}Testcase 4 : Checking if the structure of final data is correct...${NC}"

column_count=$(head -n 1 ../data/Final_data.csv | awk -F',' '{print NF}')
expected_columns=9

if [ "$column_count" -eq "$expected_columns" ]; then
    echo "${GREEN}Testcase 4 Passed: Final_data.csv contains $column_count columns.${NC}"
else
    echo "${RED}Testcase 4 Failed: Final_data.csv contains $column_count columns instead of $expected_columns.${NC}"
    exit 1
fi