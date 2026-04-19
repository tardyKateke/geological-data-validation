import pandas as pd
import numpy as np

# Function to validate survey data

def validate_survey(survey_file, collar_file):
    # Read the survey and collar data
    survey_df = pd.read_csv(survey_file)
    collar_df = pd.read_csv(collar_file)

    # Check BHID correspondence
    discrepancies = survey_df[~survey_df['BHID'].isin(collar_df['BHID'])]
    if not discrepancies.empty:
        with open('alert_report.txt', 'a') as f:
            f.write('BHID discrepancies found:\n')
            f.write(discrepancies.to_string(index=False) + '\n')

    # Validate AZIMUTH and DIP values
    invalid_azimuth = survey_df[(survey_df['AZIMUTH'] < 0) | (survey_df['AZIMUTH'] > 360)]
    invalid_dip = survey_df[(survey_df['DIP'] < -90) | (survey_df['DIP'] > 90)]

    if not invalid_azimuth.empty:
        with open('alert_report.txt', 'a') as f:
            f.write('Invalid AZIMUTH values found:\n')
            f.write(invalid_azimuth.to_string(index=False) + '\n')

    if not invalid_dip.empty:
        with open('alert_report.txt', 'a') as f:
            f.write('Invalid DIP values found:\n')
            f.write(invalid_dip.to_string(index=False) + '\n')

    # Generate Survey_bon.csv with valid data
    valid_surveys = survey_df[(survey_df['BHID'].isin(collar_df['BHID'])) & \
                               (~survey_df['AZIMUTH'].isin(invalid_azimuth['AZIMUTH'])) & \
                               (~survey_df['DIP'].isin(invalid_dip['DIP']))]
    valid_surveys.to_csv('Survey_bon.csv', index=False)

    return 'Validation complete, reports generated.'