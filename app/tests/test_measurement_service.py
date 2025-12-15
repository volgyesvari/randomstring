from unittest.mock import MagicMock, patch
from unittest import TestCase
from datetime import datetime

from sqlalchemy import Engine

from app.models.database_models import MetricItem
from app.models.measurement_input_model import MeasurementInputModel
from app.services.measurement_service import MeasurementFacade


class MeasurementServiceTest(TestCase):
    def setUp(self):
        self.event_dict = {
            "sensorId": 2,
            "metricType": "humidity",
            "metricValue": 65.9,
            "timestamp": 1765831261
        }
        self.event = MeasurementInputModel(**self.event_dict)
        self.engine_mock = MagicMock(spec=Engine)
        self.sut = MeasurementFacade(self.engine_mock)

    @patch('app.services.measurement_service.MetricItem')
    @patch('app.services.measurement_service.Session')
    def test_create_item(self, MockSession, MockMetricItem):
        mock_session_instance = MockSession.return_value
        mock_session_instance.__enter__.return_value = mock_session_instance
        metric_item_mock = MagicMock(spec=MetricItem)
        MockMetricItem.return_value = metric_item_mock

        result = self.sut.create_item(self.event)
        MockSession.assert_called_once_with(self.engine_mock)
        mock_session_instance.add.assert_called_once_with(metric_item_mock)
        mock_session_instance.commit.assert_called_once()
