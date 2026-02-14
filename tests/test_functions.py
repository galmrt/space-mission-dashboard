import pytest
import sys
import os
import pandas as pd
import numpy as np


from src.data_processing import (
    getMissionCountByCompany, 
    getSuccessRate, 
    getMissionsByDateRange, 
    getTopCompaniesByMissionCount, 
    getMissionStatusCount, 
    getMissionsByYear, 
    getMostUsedRocket, 
    getAverageMissionsPerYear,
    load_data,
    _csv_path
    )

@pytest.fixture(scope="module")
def df():
    df = load_data(_csv_path)
    return df

class TestFunctions:
    def test_getMissionCountByCompany(self, df):
        ''' Test getting mission count by company.'''
        # test known company 
        for company in ['NASA', 'SpaceX', 'RVSN USSR']:
            expected = len(df[df['Company'] == company])
            actual = getMissionCountByCompany(company)
            assert actual == expected, f"{company}: expected {expected}, got {actual}"
        
        # Test edge cases
        assert getMissionCountByCompany('NonExistent') == 0
        assert isinstance(getMissionCountByCompany('NASA'), int)

    def test_getSuccessRate(self, df):
        """Test success rate calculation for companies."""
        # Test first 5 companies
        for company in df['Company'].unique()[:5]:
            rate = getSuccessRate(company)
            success_count = df[df['Company'] == company]['MissionStatus'].str.contains('Success', na=False).sum()
            expected_rate = round((success_count / len(df[df['Company'] == company])) * 100, 2)
            assert rate == expected_rate, f"{company}: expected {expected_rate}%, got {rate}%"
            # Check that it's rounded to 2 decimal places
            assert rate == round(rate, 2), f"{company} rate not properly rounded"
        # Verify return type is float and in valid range
        assert isinstance(getSuccessRate('NASA'), float)
        assert 0.0 <= rate <= 100.0

        # Test non-existent company returns 0.0
        assert getSuccessRate('NonExistent') == 0.0
        assert getSuccessRate('') == 0.0

        # Test company with 100% success rate (if any)
        # Find a company with all successful missions
        company_success_rates = df.groupby('Company').apply(
            lambda x: (x['MissionStatus'].str.contains('Success', na=False).sum() / len(x)) * 100
        )
        perfect_companies = company_success_rates[company_success_rates == 100.0]
        if len(perfect_companies) > 0:
            perfect_company = perfect_companies.index[0]
            assert getSuccessRate(perfect_company) == 100.0

        # Test company with 0% success rate (if any)
        zero_companies = company_success_rates[company_success_rates == 0.0]
        if len(zero_companies) > 0:
            zero_company = zero_companies.index[0]
            assert getSuccessRate(zero_company) == 0.0

        
    def test_getMissionsByDateRange(self, df):
        """Test getting missions by date range."""

        # Test with a known date range (first few missions in 1957)
        start_date = '1957-10-04'
        end_date = '1957-12-31'
        missions = getMissionsByDateRange(start_date, end_date)

        # Verify return type is list
        assert isinstance(missions, list), f"Expected list, got {type(missions)}"

        # Calculate expected missions from raw data
        expected_missions = df[
            (df['Date'] >= pd.to_datetime(start_date).date()) &
            (df['Date'] <= pd.to_datetime(end_date).date())
        ]['Mission'].tolist()
        expected_missions_sorted = sorted(expected_missions)

        # Verify count matches
        assert len(missions) == len(expected_missions), \
            f"Expected {len(expected_missions)} missions, got {len(missions)}"

        # Verify missions are sorted chronologically
        assert missions == expected_missions_sorted, "Missions should be sorted"

        # Test with a single day range
        single_day = '1957-10-04'
        missions_single = getMissionsByDateRange(single_day, single_day)
        expected_single = df[df['Date'] == pd.to_datetime(single_day).date()]['Mission'].tolist()
        assert len(missions_single) == len(expected_single)

        # Test with a broader range (entire year)
        missions_year = getMissionsByDateRange('2020-01-01', '2020-12-31')
        expected_year = df[
            (df['Date'] >= pd.to_datetime('2020-01-01').date()) &
            (df['Date'] <= pd.to_datetime('2020-12-31').date())
        ]['Mission'].tolist()
        assert len(missions_year) == len(expected_year)

        # Test with date range that has no missions (far future)
        missions_future = getMissionsByDateRange('2100-01-01', '2100-12-31')
        assert missions_future == [], "Future dates should return empty list"

        # Test with date range before any missions (if applicable)
        missions_past = getMissionsByDateRange('1900-01-01', '1950-12-31')
        expected_past = df[
            (df['Date'] >= pd.to_datetime('1900-01-01').date()) &
            (df['Date'] <= pd.to_datetime('1950-12-31').date())
        ]['Mission'].tolist()
        assert len(missions_past) == len(expected_past)

        # Test invalid date format (wrong format)
        assert getMissionsByDateRange('2020/01/01', '2020-12-31') == []
        assert getMissionsByDateRange('2020-12-31', '2020/12/31') == []

        # Test invalid date format (invalid month)
        assert getMissionsByDateRange('2020-13-01', '2020-12-31') == []
        assert getMissionsByDateRange('2020-01-01', '2020-13-31') == []

        # Test invalid date format (invalid day)
        assert getMissionsByDateRange('2020-02-30', '2020-12-31') == []

        # Test invalid date format (wrong length)
        assert getMissionsByDateRange('2020-1-1', '2020-12-31') == []
        assert getMissionsByDateRange('20-01-01', '2020-12-31') == []

        # Test invalid date format (non-string input)
        assert getMissionsByDateRange('invalid-date', '2020-12-31') == []
        assert getMissionsByDateRange('2020-01-01', 'not-a-date') == []

        # Test that all returned missions are strings
        if len(missions) > 0:
            assert all(isinstance(m, str) for m in missions), "All missions should be strings"

        # Test inclusive boundaries (start and end dates are included)
        # Find a specific mission date
        if len(df) > 0:
            specific_date = df.iloc[0]['Date'].strftime('%Y-%m-%d')
            missions_boundary = getMissionsByDateRange(specific_date, specific_date)
            expected_boundary = df[df['Date'] == pd.to_datetime(specific_date).date()]['Mission'].tolist()
            assert len(missions_boundary) == len(expected_boundary), \
                "Start and end dates should be inclusive"
        
        
    def test_getTopCompaniesByMissionCount(self, df):
        """Test getting top companies by mission count."""

        # Calculate expected top companies from raw data
        company_counts = df['Company'].value_counts()

        # Test with n=5
        top_5 = getTopCompaniesByMissionCount(5)

        # Verify return type is list
        assert isinstance(top_5, list), f"Expected list, got {type(top_5)}"

        # Verify correct number of results
        expected_count = min(5, len(company_counts))
        assert len(top_5) == expected_count, f"Expected {expected_count} companies, got {len(top_5)}"

        # Verify each item is a tuple with 2 elements
        assert all(isinstance(item, tuple) for item in top_5), "All items should be tuples"
        assert all(len(item) == 2 for item in top_5), "Each tuple should have 2 elements"

        # Verify structure: (company_name: str, count: int)
        for company, count in top_5:
            assert isinstance(company, str), f"Company name should be string, got {type(company)}"
            assert isinstance(count, (int, np.integer)), f"Count should be int, got {type(count)}"
            assert count > 0, f"Count should be positive, got {count}"

        # Verify sorting: descending by count
        counts = [item[1] for item in top_5]
        assert counts == sorted(counts, reverse=True), "Companies should be sorted by count (descending)"

        # Verify the actual counts match expected
        for i, (company, count) in enumerate(top_5):
            expected_count = company_counts.iloc[i]
            assert count == expected_count, f"Position {i}: expected count {expected_count}, got {count}"

        # Test alphabetical sorting when counts are equal
        # Group companies by count and check alphabetical order within each group
        from itertools import groupby
        for count_value, group in groupby(top_5, key=lambda x: x[1]):
            companies_with_same_count = [item[0] for item in group]
            assert companies_with_same_count == sorted(companies_with_same_count), \
                f"Companies with count {count_value} should be sorted alphabetically"

        # Test with n=1 (top company only)
        top_1 = getTopCompaniesByMissionCount(1)
        assert len(top_1) == 1
        assert top_1[0][0] == company_counts.index[0]
        assert top_1[0][1] == company_counts.iloc[0]

        # Test with n=0 (should return empty list)
        top_0 = getTopCompaniesByMissionCount(0)
        assert top_0 == [], "n=0 should return empty list"

        # Test with negative n (should return empty list)
        assert getTopCompaniesByMissionCount(-1) == []
        assert getTopCompaniesByMissionCount(-10) == []

        # Test with n larger than total companies
        total_companies = len(company_counts)
        top_large = getTopCompaniesByMissionCount(total_companies + 100)
        assert len(top_large) == total_companies, \
            f"Should return all {total_companies} companies when n exceeds total"

        # Test with n=10
        top_10 = getTopCompaniesByMissionCount(10)
        expected_10 = min(10, len(company_counts))
        assert len(top_10) == expected_10

        # Verify all counts in top_10 match expected
        for i, (company, count) in enumerate(top_10):
            assert count == company_counts.iloc[i]

        # Test consistency: calling twice should give same result
        top_5_again = getTopCompaniesByMissionCount(5)
        assert top_5 == top_5_again, "Function should return consistent results"
    
    
    
    
    def test_getMissionStatusCount(self, df):
        """Test getting mission status counts."""

        status_count = getMissionStatusCount()

        # Verify return type is dict
        assert isinstance(status_count, dict), f"Expected dict, got {type(status_count)}"

        # Calculate expected counts from raw data
        expected_counts = df['MissionStatus'].value_counts().to_dict()

        # Verify the counts match expected
        assert status_count == expected_counts, \
            f"Expected {expected_counts}, got {status_count}"

        # Verify all values are integers
        for status, count in status_count.items():
            assert isinstance(count, (int, np.integer)), \
                f"Count for {status} should be int, got {type(count)}"
            assert count > 0, f"Count for {status} should be positive, got {count}"

        # Verify expected status types exist
        assert 'Success' in status_count, "Should have 'Success' status"
        assert 'Failure' in status_count, "Should have 'Failure' status"

        # Verify total count matches dataframe length
        total_missions = sum(status_count.values())
        assert total_missions == len(df), \
            f"Total missions {total_missions} should equal dataframe length {len(df)}"

        # Test consistency: calling twice should give same result
        status_count_again = getMissionStatusCount()
        assert status_count == status_count_again, "Function should return consistent results"
    
    
    
    
    def test_getMissionsByYear(self, df):
        """Test getting missions by year."""

        # Test with year 2020
        count_2020 = getMissionsByYear(2020)

        # Verify return type is int
        assert isinstance(count_2020, int), f"Expected int, got {type(count_2020)}"

        # Calculate expected count from data (extract year from Date column)
        expected_2020 = len(df[df['Date'].apply(lambda x: x.year) == 2020])
        assert count_2020 == expected_2020, \
            f"Expected {expected_2020} missions in 2020, got {count_2020}"

        # Test with the first year in the dataset
        first_year = df['Date'].apply(lambda x: x.year).min()
        count_first = getMissionsByYear(first_year)
        expected_first = len(df[df['Date'].apply(lambda x: x.year) == first_year])
        assert count_first == expected_first, \
            f"Expected {expected_first} missions in {first_year}, got {count_first}"

        # Test with the last year in the dataset
        last_year = df['Date'].apply(lambda x: x.year).max()
        count_last = getMissionsByYear(last_year)
        expected_last = len(df[df['Date'].apply(lambda x: x.year) == last_year])
        assert count_last == expected_last, \
            f"Expected {expected_last} missions in {last_year}, got {count_last}"

        # Test with year that has no missions (far future)
        assert getMissionsByYear(2100) == 0, "Future year should return 0"

        # Test with year before any missions
        assert getMissionsByYear(1900) == 0, "Year before missions should return 0"

        # Test with negative year
        assert getMissionsByYear(-1) == 0, "Negative year should return 0"

        # Test multiple years and verify counts
        for year in [2018, 2019, 2021]:
            count = getMissionsByYear(year)
            expected = len(df[df['Date'].apply(lambda x: x.year) == year])
            assert count == expected, f"Year {year}: expected {expected}, got {count}"

        # Verify count is non-negative
        assert count_2020 >= 0, "Count should be non-negative"

        # Test consistency: calling twice should give same result
        count_2020_again = getMissionsByYear(2020)
        assert count_2020 == count_2020_again, "Function should return consistent results"
    
    
    
    
    def test_getMostUsedRocket(self, df):
        """Test getting the most used rocket."""

        rocket = getMostUsedRocket()

        # Verify return type is string
        assert isinstance(rocket, str), f"Expected str, got {type(rocket)}"

        # Verify it's not empty
        assert len(rocket) > 0, "Rocket name should not be empty"

        # Calculate expected most used rocket from data
        rocket_counts = df['Rocket'].value_counts()
        max_count = rocket_counts.max()

        # Get all rockets with the maximum count
        most_used_rockets = rocket_counts[rocket_counts == max_count].index.tolist()

        # If there are ties, the function should return the first alphabetically
        expected_rocket = sorted(most_used_rockets)[0]

        assert rocket == expected_rocket, \
            f"Expected '{expected_rocket}', got '{rocket}'"

        # Verify the rocket actually exists in the dataset
        assert rocket in df['Rocket'].values, \
            f"Rocket '{rocket}' should exist in the dataset"

        # Verify it has the maximum count
        actual_count = len(df[df['Rocket'] == rocket])
        assert actual_count == max_count, \
            f"Rocket '{rocket}' should have count {max_count}, got {actual_count}"

        # Test consistency: calling twice should give same result
        rocket_again = getMostUsedRocket()
        assert rocket == rocket_again, "Function should return consistent results"
    
    
    
    
    def test_getAverageMissionsPerYear(self, df):
        """Test getting average missions per year."""

        # Test with range 2018-2020 (3 years)
        avg_2018_2020 = getAverageMissionsPerYear(2018, 2020)

        # Verify return type is float
        assert isinstance(avg_2018_2020, float), f"Expected float, got {type(avg_2018_2020)}"

        # Calculate expected average from raw data (extract year from Date column)
        df_years = df['Date'].apply(lambda x: x.year)
        missions_in_range = df[df_years.between(2018, 2020)]
        expected_avg = round(len(missions_in_range) / 3, 2)  # 3 years: 2018, 2019, 2020

        assert avg_2018_2020 == expected_avg, \
            f"Expected {expected_avg}, got {avg_2018_2020}"

        # Test with single year range (2020-2020)
        avg_single = getAverageMissionsPerYear(2020, 2020)
        expected_single = round(len(df[df_years == 2020]) / 1, 2)
        assert avg_single == expected_single, \
            f"Single year: expected {expected_single}, got {avg_single}"

        # Test with 2-year range
        avg_2019_2020 = getAverageMissionsPerYear(2019, 2020)
        missions_2019_2020 = df[df_years.between(2019, 2020)]
        expected_2019_2020 = round(len(missions_2019_2020) / 2, 2)
        assert avg_2019_2020 == expected_2019_2020, \
            f"2019-2020: expected {expected_2019_2020}, got {avg_2019_2020}"

        # Test with range that has no missions (far future)
        avg_future = getAverageMissionsPerYear(2100, 2105)
        assert avg_future == 0.0, "Future years should return 0.0"

        # Test with invalid range (end < start)
        assert getAverageMissionsPerYear(2020, 2018) == 0.0, \
            "Invalid range (end < start) should return 0.0"

        # Test with negative years
        assert getAverageMissionsPerYear(-1, 0) == 0.0, \
            "Negative years should return 0.0"
        assert getAverageMissionsPerYear(-10, -5) == 0.0, \
            "Negative year range should return 0.0"

        # Test with very large range
        first_year = int(df_years.min())
        last_year = int(df_years.max())
        avg_all = getAverageMissionsPerYear(first_year, last_year)
        num_years = last_year - first_year + 1
        expected_all = round(len(df) / num_years, 2)
        assert avg_all == expected_all, \
            f"Full range: expected {expected_all}, got {avg_all}"

        # Verify result is rounded to 2 decimal places
        assert avg_2018_2020 == round(avg_2018_2020, 2), \
            "Result should be rounded to 2 decimal places"

        # Verify average is non-negative
        assert avg_2018_2020 >= 0.0, "Average should be non-negative"

        # Test consistency: calling twice should give same result
        avg_again = getAverageMissionsPerYear(2018, 2020)
        assert avg_2018_2020 == avg_again, "Function should return consistent results"
        
    
    
        
















































































