import time

from app.monitor import check_all_services


def run_monitoring_worker(interval_seconds=30):
    print("Background monitoring worker started...")

    while True:
        results = check_all_services()

        print(f"Checked {len(results)} services")

        time.sleep(interval_seconds)