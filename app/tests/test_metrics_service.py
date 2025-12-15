from unittest import TestCase
from unittest.mock import MagicMock, patch, call
from datetime import datetime

from sqlalchemy import Engine

from app.models.metrics_models import MetricsInputModel
from app.services.metrics_dao import MetricsDAO
from app.services.metrics_service import MetricsFacade


class MetricServiceTest(TestCase):
    def setUp(self):
        self.event_dict = {"sensor_ids": [1,2,3,4,5],
                           "metrics": ["temperature", "humidity", "windSpeed"],
                           "statistic": "max",
                           "start_date": "2025-01-10",
                           "end_date": "2025-01-15",}
        self.event = MetricsInputModel(**self.event_dict)
        self.engine_mock = MagicMock(spec=Engine)
        self.metrics_dao_mock = MagicMock(spec=MetricsDAO)
        self.sut = MetricsFacade(self.metrics_dao_mock)
        self.dummy_entry = {"sensorId": 1, "metric": "temperature", "value": 25.7}

    @patch('app.services.metrics_service.row_to_dict')
    def test_get_metrics(self, row_to_dict_mock):
        row_to_dict_mock.return_value = self.dummy_entry
        self.metrics_dao_mock.get_metric.return_value = [MagicMock, MagicMock]
        result = self.sut.get_metrics(self.event)
        self.metrics_dao_mock.get_metric.assert_has_calls([call(
            MetricsInputModel(sensor_ids=[1, 2, 3, 4, 5], metrics=['humidity', 'temperature', 'windSpeed'],
                              statistic='max', start_date=datetime(2025, 1, 10, 0, 0),
                              end_date=datetime(2025, 1, 15, 0, 0)), 'humidity'),
                                                           call(MetricsInputModel(sensor_ids=[1, 2, 3, 4, 5],
                                                                                  metrics=['humidity', 'temperature',
                                                                                           'windSpeed'],
                                                                                  statistic='max',
                                                                                  start_date=datetime(2025, 1,
                                                                                                               10, 0,
                                                                                                               0),
                                                                                  end_date=datetime(2025, 1,
                                                                                                             15, 0, 0)),
                                                                'temperature'),
                                                           call(MetricsInputModel(sensor_ids=[1, 2, 3, 4, 5],
                                                                                  metrics=['humidity', 'temperature',
                                                                                           'windSpeed'],
                                                                                  statistic='max',
                                                                                  start_date=datetime(2025, 1,
                                                                                                               10, 0,
                                                                                                               0),
                                                                                  end_date=datetime(2025, 1,
                                                                                                             15, 0, 0)),
                                                                'windSpeed')])
