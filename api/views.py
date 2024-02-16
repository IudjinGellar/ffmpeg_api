from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from api.models import VideoFileModel
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from api.tasks import process_video
from os import remove
from ffmpeg_api.settings import logger


@method_decorator(csrf_exempt, name='dispatch')
class FileLoadApiView(APIView):

    def post(self, request):
        'загрузка файла на хранение'
        videofile = request.FILES.get('file')
        if videofile:
            new_file = VideoFileModel(file=videofile,
                                      filename=videofile.name)
            new_file.save()
            message = {'id': new_file.id}
            logger.info(f'New file: {new_file.id}')
        else:
            message = {'error': 'no data'}
        return JsonResponse(message)


@method_decorator(csrf_exempt, name='dispatch')
class FileApiView(APIView):

    def patch(self, request, id):
        'изменение разрешения видео'
        videofile = get_object_or_404(VideoFileModel, id=id)
        width = request.POST.get('width')
        height = request.POST.get('height')
        if width and height:
            width, height = int(width), int(height)
            if width > 20 and height > 20:
                videofile.processing = VideoFileModel.Processing.processing
                videofile.save()
                videofile_id = videofile.id
                process_video.apply_async(queue='processing',
                                          args=[videofile_id, width, height])
                message = {'success': True}
                logger.info(f'Change file: {videofile.id} {width=}, {height=}')

            else:
                message = {'error': 'width and height should be >20!'}
        else:
            message = {'error': 'no width or height'}
        return JsonResponse(message)

    def get(self, request, id):
        'информация о файле и статусе его обработки'
        file = get_object_or_404(VideoFileModel, id=id)
        message = {
              'id': file.id,
              'filename': file.filename,
              'processing': (True if file.process_status ==
                             VideoFileModel.Processing.processing
                             else False),
              'processingSuccess': file.processing_success}
        logger.info(f'Return data for: {file.id}')
        return JsonResponse(message)

    def delete(self, request, id):
        'удалить файл'
        file = get_object_or_404(VideoFileModel, id=id)
        file_id = file.id
        file.delete()
        remove(file.file.path)
        logger.info(f'Delete file: {file_id}')
        return JsonResponse({'success': True})
