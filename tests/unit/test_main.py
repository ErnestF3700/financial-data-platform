import pytest
from src import main


def test_run_pipeline_raises_error_when_extract_csv_fails(monkeypatch):
    def mock_extract_csv(file_path):
        raise FileNotFoundError("Test missing file")
    
    monkeypatch.setattr(main, "extract_csv", mock_extract_csv)
    
    with pytest.raises(FileNotFoundError, match="Test missing file"):
        main.run_pipeline()