from api.models import VideoFileModel
import json
from unittest.mock import patch
import os
from rest_framework.test import APITestCase
from api.tasks import process_video


class TestApi(APITestCase):

    @patch('api.tasks.process_video.apply_async')
    def test_all(self, process):
        # загрузка видео
        response = self.client.post(
            '/api/file/',
            {'file': open('ololo.mp4', 'rb')})
        db_file = VideoFileModel.objects.all()[0]
        data = json.loads(response.content)
        id = data['id']
        file_path = db_file.file.path
        self.assertEqual(id, str(db_file.id))
        # изменение параметров видео
        file_size = os.stat(file_path).st_size
        response = self.client.patch(
            f'/api/file/{id}/',
            {'width': '30',
             'height': '30'})
        data = json.loads(response.content)
        self.assertTrue(data['success'])
        process_video(id, 30, 30)
        file_path_after_processing = VideoFileModel.objects.all()[0].file.path
        file_size_after_processing = os.stat(
            file_path_after_processing).st_size
        self.assertTrue(file_size > file_size_after_processing)
        # проверка статуса видео
        file = VideoFileModel.objects.all()[0]
        assert_data = {
              'id': str(file.id),
              'filename': file.filename,
              'processing': False,
              'processingSuccess': 'true'}
        response = self.client.get(f'/api/file/{id}/')
        response_data = json.loads(response.content)
        self.assertEqual(assert_data, response_data)
        # удаление файла
        response = self.client.delete(f'/api/file/{id}/')
        response_data = json.loads(response.content)
        self.assertEqual(response_data,
                         {'success': True})
        self.assertFalse(os.path.exists(file_path))
