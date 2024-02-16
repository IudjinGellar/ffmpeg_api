from celery import shared_task
import ffmpeg
from api.models import VideoFileModel
from datetime import datetime
from os import remove


@shared_task
def process_video(videofile_id, width, height):
    file_model = VideoFileModel.objects.get(id=videofile_id)
    file_field = file_model.file
    current_file = file_field.path
    current_time = datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
    new_file = f'media/{file_model.id}_{current_time}.mp4'
    process = (
        ffmpeg.input(current_file)
        .output(('media/'+new_file), vf='scale={}:{}'.format(width, height))
        .run()
    )
    file_model.file = new_file
    file_model.processing_success = VideoFileModel.ProcessingSucces.true
    file_model.process_status = VideoFileModel.Processing.end
    file_model.save()
    remove(current_file)
