from apscheduler.schedulers.blocking import BlockingScheduler # type: ignore
from collector.collector import collect_and_store

def start():
    scheduler = BlockingScheduler()
    scheduler.add_job(collect_and_store, "interval", seconds=30)
    print("Scheduler started — collecting every 30 seconds. Ctrl+C to stop.")
    collect_and_store()  # run once immediately on start
    scheduler.start()

if __name__ == "__main__":
    start()