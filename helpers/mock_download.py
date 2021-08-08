import time

def mock_download(file_size, downloader):
    job_id = downloader.create_job(file_size)
    while not downloader.is_job_done(job_id):
        time.sleep(1)
