import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime, timedelta
from staging.api_extract_data import get_crypto_ohlc_data, create_crypto_table

class TestCryptoDataFunctions(unittest.TestCase):
    
    def setUp(self):
        # Calcular la fecha de ayer
        self.yesterday = (datetime.now() - timedelta(days=1)).date()
    
    @patch('staging.api_extract_data.requests.get')
    def test_get_crypto_ohlc_data_success(self, mock_get: MagicMock)-> None:
        # Simular una respuesta exitosa de la API de CoinGecko
        mock_response = MagicMock()
        mock_response.json.return_value = [
            [int(self.yesterday.strftime("%s")) * 1000, 4000, 4050, 3950, 4025, 1000]  # Ejemplo de datos OHLC
        ]
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Llamar a la función
        result = get_crypto_ohlc_data('ethereum', str(self.yesterday))

        # Comprobar el resultado
        expected_data = {
            'date': [pd.Timestamp(self.yesterday)],  # Asegurarse de que sea un Timestamp
            'time': ['00:00:00'],
            'stock_symbol': ['ethereum'],
            'open_price': [4000.0],
            'high_price': [4050.0],
            'low_price': [3950.0],
            'close_price': [4025.0],
        }
        expected_df = pd.DataFrame(expected_data)

        # Asegúrate de que ambos DataFrames tienen el mismo tipo de datos
        result['date'] = pd.to_datetime(result['date'])  # Convierte a datetime si es necesario
        pd.testing.assert_frame_equal(result, expected_df)

    @patch('staging.api_extract_data.requests.get')
    def test_get_crypto_ohlc_data_no_data(self, mock_get: MagicMock):
        # Simular una respuesta vacía de la API de CoinGecko
        mock_response = MagicMock()
        mock_response.json.return_value = []
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Llamar a la función
        result = get_crypto_ohlc_data('ethereum', str(self.yesterday))

        # Comprobar que el resultado es un DataFrame vacío
        expected_df = pd.DataFrame()
        pd.testing.assert_frame_equal(result, expected_df)

    @patch('staging.api_extract_data.requests.get')
    def test_create_crypto_table_success(self, mock_get: MagicMock):
        # Simular una respuesta exitosa de la API de CoinMarketCap
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'data': {
                '1': {  # ID de Bitcoin
                    'symbol': 'BTC',
                    'id': '1',
                    'name': 'Bitcoin',
                    'category': 'Cryptocurrency',
                    'description': 'La criptomoneda más popular.',
                    'logo': 'https://bitcoin.org/img/icons/opengraph.png',
                    'urls': {
                        'website': ['https://bitcoin.org'],
                        'reddit': ['https://reddit.com/r/bitcoin']
                    }
                }
            }
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Llamar a la función
        api_key = 'fake_api_key'  # Reemplazar por una clave ficticia
        result = create_crypto_table('1', api_key)

        # Comprobar el resultado
        expected_data = {
            'symbol': ['BTC'],
            'id': ['1'],
            'name': ['Bitcoin'],
            'category': ['Cryptocurrency'],
            'description': ['La criptomoneda más popular.'],
            'logo': ['https://bitcoin.org/img/icons/opengraph.png'],
            'website': ['https://bitcoin.org'],
            'reddit': ['https://reddit.com/r/bitcoin'],
        }
        expected_df = pd.DataFrame(expected_data)

        pd.testing.assert_frame_equal(result, expected_df)

    @patch('staging.api_extract_data.requests.get')
    def test_create_crypto_table_no_data(self, mock_get: MagicMock):
        # Simular una respuesta sin datos de la API de CoinMarketCap
        mock_response = MagicMock()
        mock_response.json.return_value = {
            'data': {}
        }
        mock_response.status_code = 200
        mock_get.return_value = mock_response
        
        # Llamar a la función
        api_key = 'fake_api_key'  # Reemplazar por una clave ficticia
        result = create_crypto_table('1', api_key)

        # Comprobar que el resultado es un DataFrame vacío
        expected_df = pd.DataFrame()
        pd.testing.assert_frame_equal(result, expected_df)

    @patch('staging.api_extract_data.requests.get')
    def test_create_crypto_table_http_error(self, mock_get: MagicMock):
        # Simular un error HTTP (ej. 404 Not Found)
        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response
        
        # Llamar a la función
        api_key = 'fake_api_key'  # Reemplazar por una clave ficticia
        result = create_crypto_table('invalid_id', api_key)

        # Comprobar que el resultado es un DataFrame vacío
        expected_df = pd.DataFrame()
        pd.testing.assert_frame_equal(result, expected_df)

if __name__ == '__main__':
    unittest.main()
