from unittest.mock import patch, MagicMock
from sqlalchemy.engine import Engine
from variables.connection_redshift import create_redshift_engine

def test_create_redshift_engine():
    """
    Test that verifies the create_redshift_engine function constructs
    the connection string and creates a database engine.
    """
    # Create a mock Engine object
    mock_engine = MagicMock(spec=Engine)
    
    # Patch the create_engine method from sqlalchemy
    with patch('variables.connection_redshift.create_engine', return_value=mock_engine) as mock_create_engine:
        # Call the function to test
        engine = create_redshift_engine()
        
        # Assert that create_engine was called
        mock_create_engine.assert_called_once()
        
        # Check that the return type is Engine
        assert isinstance(engine, Engine)
