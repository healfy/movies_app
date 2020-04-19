import tempfile
import requests
from django.core.files import File
from video_encoding.tasks import convert_all_videos
from movies_app.celery import celery
from .models import Movie


@celery.task
def convert_video(app_label: str, model_name: str, pk: int):
    convert_all_videos(app_label, model_name, pk)


@celery.task
def download_and_create_video(url):
    local_filename = url.split('/')[-1]
    lf = tempfile.NamedTemporaryFile()
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        for block in r.iter_content(1024 * 8):
            # If no more file then stop
            if not block:
                break

            lf.write(block)

    db_file = File(lf, name=local_filename)
    video = Movie.objects.create(db_file=db_file)
    convert_video.apply_async(args=(
        video._meta.app_label, video._meta.model_name, video.pk
    ))
