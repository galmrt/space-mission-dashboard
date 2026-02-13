import pandas as pd
import numpy as np
from datetime import datetime

df = None

def load_data(path="src/data/space_missions (1) 2.csv"):
    global df
    df = pd.read_csv(path)
    return df

'''
Function 1: `getMissionCountByCompany(companyName: str) -> int`
**Description**: Returns the total number of missions for a given company.
**Input**:
- `companyName` (string): Name of the company (e.g., "SpaceX", "NASA", "RVSN USSR")
**Output**:
- Integer representing the total number of missions
'''
def getMissionCountByCompany(companyName:str) -> int:
    return df[df['Company'] == companyName].shape[0]

'''
Function 2: `getSuccessRate(companyName: str) -> float`
**Description**: Calculates the success rate for a given company as a percentage.
**Input**:
- `companyName` (string): Name of the company
**Output**:
- Float representing success rate as a percentage (0-100), rounded to 2 decimal places
- Only "Success" missions count as successful
- Return `0.0` if company has no missions
'''    
def getSuccessRate(companyName: str) -> float:
    companyData = df[df['Company'] == companyName]
    if len(companyData) == 0:
        return float(0.0)
    
    successCount = companyData['MissionStatus'].str.contains('Success')
    return round(sum(successCount) / len(successCount) * 100, 2)

'''
Function 3: `getMissionsByDateRange(startDate: str, endDate: str) -> list`
**Description**: Returns a list of all mission names launched between startDate and
endDate (inclusive).
**Input**:
- `startDate` (string): Start date in "YYYY-MM-DD" format
- `endDate` (string): End date in "YYYY-MM-DD" format
**Output**:
- List of strings containing mission names, sorted chronologically
'''
def getMissionsByDateRange(startDate: str, endDate: str) -> list:
    if not isValidDate(startDate) or not isValidDate(endDate):
        print("Incorrect Time Format. Need 'YYYY-MM-DD'")
        return []
    
    df['Date'] = pd.to_datetime(df['Date'])
    ans = df[df['Date'] <= datetime.strptime(endDate, "%Y-%m-%d")]
    ans = ans[datetime.strptime(startDate, "%Y-%m-%d") <= ans['Date']]
    
    return list(ans['Mission'])

def isValidDate(s:str) -> bool:
    if not isinstance(s, str) or len(s) != 10:
        return False
    try: 
        datetime.strptime(s, "%Y-%m-%d")
        return True
    except ValueError:
        return False
    
'''
Function 4: `getTopCompaniesByMissionCount(n: int) -> list`
**Description**: Returns the top N companies ranked by total number of missions.
**Input**:
- `n` (integer): Number of top companies to return
**Output**:
- List of tuples: `[(companyName, missionCount), ...]`
- Sorted by mission count in descending order
- If companies have the same count, sort alphabetically by company name
''' 
def getTopCompaniesByMissionCount(n: int) -> list:
    if n < 0:
        return []
        
    vals = df['Company'].value_counts()[:n]
    ans = []
    #convert to tuples
    for label, item in vals.items():
        ans.append((label, item))

    # sort by specific value
    ans.sort(key = lambda x: (-x[1], x[0]), reverse=False)
    return ans

'''
Function 5: `getMissionStatusCount() -> dict`
**Description**: Returns the count of missions for each mission status.

**Input**: None

**Output**:
- Dictionary with status as key and count as value
- Keys: "Success", "Failure", "Partial Failure", "Prelaunch Failure"

**Example**:
```python
getMissionStatusCount()
# Returns: {"Success": 3879, "Failure": 485, "Partial Failure": 68, "Prelaunch Failure": 7}
'''
def getMissionStatusCount() -> dict:
    vals = df['MissionStatus'].value_counts()
    return vals.to_dict()

'''
Function 6: `getMissionsByYear(year: int) -> int`
**Description**: Returns the total number of missions launched in a specific year.
**Input**:
- `year` (integer): Year (e.g., 2020)
**Output**:
- Integer representing the total number of missions in that year
**Example**:
```python
getMissionsByYear(2020) # Returns: 114
'''

def getMissionsByYear(year: int) -> int:
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    return len(df[df['Year'] == year])


'''Function 7: `getMostUsedRocket() -> str`
**Description**: Returns the name of the rocket that has been used the most times.
**Input**: None
**Output**:
- String containing the rocket name
- If multiple rockets have the same count, return the first one alphabetically'''

def getMostUsedRocket():
    if df.empty:
        return ''

    rocketCount = df['Rocket'].value_counts()
    maxCount = rocketCount.max()
    topCounts = rocketCount[rocketCount == maxCount].index.sort_values()
    return topCounts[0]

'''
Function 8: `getAverageMissionsPerYear(startYear: int, endYear: int) -> float`
**Description**: Calculates the average number of missions per year over a given range.
**Input**:
- `startYear` (integer): Starting year (inclusive)
- `endYear` (integer): Ending year (inclusive)
**Output**:
- Float representing average missions per year, rounded to 2 decimal places
'''
def getAverageMissionsPerYear(startYear: int, endYear: int) -> float:
    if startYear > endYear or startYear < 0 or endYear < 0:
        return 0.0
    
    totalCount = 0
    for year in range(startYear, endYear + 1):
        totalCount += getMissionsByYear(year)
    return round(totalCount / (endYear - startYear + 1), 2)
