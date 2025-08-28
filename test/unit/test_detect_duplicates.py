import pytest
import unittest.mock as mock
from src.util import detector
from src.util.detector import parse
from src.util.parser import Article

@pytest.mark.unit
def test_detect_duplicates_not_enough_no1():
    detector.parse = mock.MagicMock()
    detector.parse.return_value = [Article("testkey")] # Return only one article
    test_detector = detector
    with pytest.raises(ValueError) as error:
        test_detector.detect_duplicates("test")
    assert error.type == ValueError

@pytest.mark.unit
def test_detect_duplicates_no_key_duplicates_no2():
    detector.parse = mock.MagicMock()
    detector.parse.return_value = [Article("testkey"), Article("different_testkey")]
    test_detector = detector
    res = test_detector.detect_duplicates("test")
    assert res == []

@pytest.mark.unit
def test_detect_duplicates_no_key_nor_doi_duplicates_no3():
    detector.parse = mock.MagicMock()
    detector.parse.return_value = [Article("testkey", "190.09123/901823"), Article("different_testkey", "200.012123/091283")]
    test_detector = detector
    res = test_detector.detect_duplicates("test")
    assert res == []

@pytest.mark.unit
def test_detect_duplicates_same_key_no_doi_no4():
    detector.parse = mock.MagicMock()
    detector.parse.return_value = [Article("testkey"), Article("testkey")]
    test_detector = detector
    res = test_detector.detect_duplicates("test")
    assert res == [Article("testkey")]

@pytest.mark.unit
def test_detect_duplicates_same_key_same_doi_no5():
    detector.parse = mock.MagicMock()
    detector.parse.return_value = [Article("testkey", "190.09123/901823"), Article("testkey", "190.09123/901823")]
    test_detector = detector
    res = test_detector.detect_duplicates("test")
    assert res == [Article("testkey", "190.09123/901823")]

@pytest.mark.unit
def test_detect_duplicates_same_doi_different_key_no6():
    detector.parse = mock.MagicMock()
    detector.parse.return_value = [Article("testkey", "190.09123/901823"), Article("different_key", "190.09123/901823")]
    test_detector = detector
    res = test_detector.detect_duplicates("test")
    assert res == [Article("different_key", "190.09123/901823")]

@pytest.mark.unit
def test_detect_duplicates_same_key_different_doi_no7():
    detector.parse = mock.MagicMock()
    detector.parse.return_value = [Article("testkey", "190.09123/901823"), Article("testkey", "12415124.123123/901823")]
    test_detector = detector
    res = test_detector.detect_duplicates("test")
    assert res == [Article("testkey", "12415124.123123/901823")]

# I structured my test cases based on my test case table, with a similar structure to all of them for ease of reading
# The test independence is assured in part by using a new mock on all of them and running a new instance of the detector class in all of them
# The only challenges I faced were the python path not being set which made importing modules impossible, fixed with a short line in pytest.ini
# and a confusion on which article should be returned if the key is the same but the DOI is different (based on the wording: 
# "[articles] are considered duplicates if they have the same key (in case either or both articles miss a DOI) or if they have the same key or DOI.)"
# I assumed in my test case (no7) that it would be the second one by looking at the append in the code. Since there is a defect regarding this 
# case, I could not check the output.
