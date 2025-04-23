import time
import threading
from datetime import datetime
from app.database.db import SessionLocal
from app.models.schedule import Schedule
from app.models.device import Device
import logging

# Set up logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("scheduler_service")


class SchedulerService:
    def __init__(self):
        self.running = False
        self.thread = None

    def start(self):
        if self.running:
            logger.info("Scheduler already running")
            return

        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler)
        self.thread.daemon = True  # Allow app to exit even if thread is running
        self.thread.start()
        logger.info("Scheduler service started")

    def stop(self):
        if not self.running:
            return

        logger.info("Stopping scheduler service...")
        self.running = False
        if self.thread:
            self.thread.join(timeout=5)
        logger.info("Scheduler service stopped")

    def _run_scheduler(self):
        # Run check immediately on startup to handle any missed schedules
        self._check_schedules()

        # Main scheduler loop - check every 1 second for more precision
        while self.running:
            self._check_schedules()
            time.sleep(1)  # Check every second instead of every 30 seconds

    def _check_schedules(self):
        """Check all schedules and execute them if needed"""
        db = SessionLocal()
        try:
            # Get current time and weekday
            now = datetime.now()
            current_hour_minute = now.strftime("%H:%M")
            current_second = now.second

            # Only execute at the start of each minute (when seconds is 0)
            if current_second != 0:
                db.close()
                return

            # Convert to day index (0=Sunday, 1=Monday, ..., 6=Saturday)
            current_day = now.weekday()
            # Convert from Monday=0 to Sunday=0 format
            if current_day == 6:  # If Saturday
                current_day = 6
            else:
                current_day += 1

            logger.info(f"Checking schedules at {current_hour_minute}:00, day {current_day}")

            # Get all schedules matching the current time
            schedules = db.query(Schedule).filter(Schedule.time == current_hour_minute).all()

            if schedules:
                logger.info(f"Found {len(schedules)} schedules for time {current_hour_minute}")

            for schedule in schedules:
                try:
                    # Parse days from comma-separated string
                    days_list = [int(d) for d in schedule.days.split(",") if d]

                    # Check if today is in the schedule days
                    if current_day in days_list:
                        logger.info(f"Executing schedule {schedule.id} for device {schedule.device_id}")

                        # Get device and update status
                        device = db.query(Device).filter(Device.id == schedule.device_id).first()
                        if device:
                            device.status = schedule.operation
                            db.commit()
                            logger.info(f"Device {device.id} ({device.name}) set to {schedule.operation}")
                        else:
                            logger.warning(f"Device {schedule.device_id} not found")
                except Exception as schedule_error:
                    logger.error(f"Error processing schedule {schedule.id}: {str(schedule_error)}")

        except Exception as e:
            logger.error(f"Error in scheduler: {str(e)}")
        finally:
            db.close()