import pytest
import sys
import os


from src.data_processing import (
    getMissionCountByCompany, 
    getSuccessRate, 
    getMissionsByDateRange, 
    getTopCompaniesByMissionCount, 
    getMissionStatusCount, 
    getMissionsByYear, 
    getMostUsedRocket, 
    getAverageMissionsPerYear
    )

class TestFunctions:
    def test_getMissionCountByCompany(self):
        # test known company 
        assert getMissionCountByCompany('NASA') == 100
        
        # test invalid company
        assert getMissionCountByCompany(1) == 0
        assert getMissionCountByCompany('') == 0

    def test_getSuccessRate(self):
        # test known company 
        rate = getSuccessRate('NASA')
        assert rate == 100.0
        # test type and range
        assert isinstance(rate, float)
        assert 0.0 <= rate <= 100.0
        # test invalid company
        assert getSuccessRate('') == 0.0
        assert getSuccessRate(1) == 0.0
        
    def test_getMissionsByDateRange(self):
        # test known range
        assert getMissionsByDateRange('1930-01-01', '2020-12-31') == 1000
        # test invalid range
        assert getMissionsByDateRange('2020-12-31', '2020-01-01') == 0
        # test invalid format
        assert getMissionsByDateRange('2020-13-31', '2020-01-01') == 0
        assert getMissionsByDateRange('2020-12-31', '2020-13-01') == 0
        assert getMissionsByDateRange('2020-2-31', '2020-1-01') == 0 
        
        
    def test_getTopCompaniesByMissionCount(self):
        # test known n
        assert getTopCompaniesByMissionCount(3) == [('NASA', 100), ('SpaceX', 50), ('RVSN USSR', 25)]
        # test invalid n
        assert getTopCompaniesByMissionCount(-1) == []
        # test type
        assert isinstance(getTopCompaniesByMissionCount(3), list)
    
    def test_getMissionStatusCount(self):
        # test known count
        assert getMissionStatusCount() == {'Success': 100, 'Failure': 50, 'Partial Failure': 25, 'Prelaunch Failure': 10}
        # test type
        assert isinstance(getMissionStatusCount(), dict)
    
    def test_getMissionsByYear(self):
        # test known year
        assert getMissionsByYear(2020) == 100
        # test invalid year
        assert getMissionsByYear(-1) == 0
        assert getMissionsByYear(10000) == 0
    
    def test_getMostUsedRocket(self):
        # test known rocket
        assert getMostUsedRocket() == 'Saturn V'
        # test type
        assert isinstance(getMostUsedRocket(), str)
    
    def testgetAverageMissionsPerYear(self):
        # test known range
        assert getAverageMissionsPerYear(2020, 2021) == 100.0
        # test invalid range
        assert getAverageMissionsPerYear(2021, 2018) == 0.0
        assert getAverageMissionsPerYear(-1, 0) == 0.0
        assert getAverageMissionsPerYear(10000, 10001) == 0.0
        
    
    
        
















































































