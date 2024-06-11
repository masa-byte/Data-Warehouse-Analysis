from watchdog.observers import Observer
from watchdog.events import FileSystemEvent, FileSystemEventHandler
from google.cloud import bigquery
import pandas as pd
import threading
import os

directory = os.path.dirname(os.path.realpath(__file__))
############# GOOGLE BIG QUERY #############

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.path.join(directory, "")
project_id = ""
dataset_id = ""
table_id = ""

client = bigquery.Client()

job_config = bigquery.LoadJobConfig()
job_config.write_disposition = bigquery.WriteDisposition.WRITE_APPEND

############# GOOGLE BIG QUERY #############

file_queue = []
queue_condition = threading.Condition()
columns = [
    "pond_id",
    "created_at",
    "entry_id",
    "temp_c",
    "turbidity_ntu",
    "dissolved_oxygen_g_ml",
    "ph",
    "ammonia_g_ml",
    "nitrate_g_ml",
    "population",
    "fish_length_cm",
    "fish_weight_g",
]


class MyHandler(FileSystemEventHandler):
    def on_created(self, event: FileSystemEvent) -> None:
        if not event.is_directory and event.src_path.endswith(".csv"):
            with queue_condition:
                file_queue.append(event.src_path)
                queue_condition.notify()


def import_data(file_path):
    df = pd.read_csv(file_path, names=columns, header=None)
    if not df.empty:
        try:
            df["created_at"] = pd.to_datetime(df["created_at"])
            print(df.head())

            job = client.load_table_from_dataframe(df, table_id, job_config=job_config)

            job.result()

            if job.state == "DONE":
                print("Job completed successfully.")
                if job.errors:
                    print(f"Job completed with errors: {job.errors}")
                else:
                    print(f"Data imported to BigQuery from {file_path}")
            else:
                print(f"Job did not complete successfully. Job state: {job.state}")
        except Exception as e:
            print(f"Error while importing data to BigQuery: {e}")
            pass


def process_file_queue():
    while True:
        with queue_condition:
            if not file_queue:
                queue_condition.wait()

            file_path = file_queue.pop(0)
            import_data(file_path)


def start_file_watching(filepath):
    observer = Observer()
    event_handler = MyHandler()

    observer.schedule(event_handler, path=filepath, recursive=False)
    observer.start()

    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

    observer.join()


def create_output_directory(filepath):
    if not os.path.exists(filepath):
        os.makedirs(filepath)


if __name__ == "__main__":

    filepath = os.path.join(directory, "output")
    create_output_directory(filepath)

    file_processing_thread = threading.Thread(target=process_file_queue, daemon=True)
    file_processing_thread.start()

    start_file_watching(filepath)
