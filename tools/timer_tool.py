import time
import sys
import platform

# Only import winsound if on Windows to prevent crashes on other OS
if platform.system() == "Windows":
    import winsound

def start_workout_timer(duration_seconds: int, exercise_name: str) -> str:
    """A tool to run a live countdown timer in the terminal for workouts and rests."""
    print(f"\n[SYSTEM TIMER] Starting timer for: {exercise_name}")
    
    for remaining in range(duration_seconds, 0, -1):
        sys.stdout.write(f"\rTime remaining: {remaining:02d} seconds ")
        sys.stdout.flush()
        time.sleep(1)
        
    # Terminal notification
    sys.stdout.write(f"\r[SYSTEM TIMER] Time is UP for {exercise_name}!      \n")
    sys.stdout.flush()
    
    # Audio notification
    if platform.system() == "Windows":
        # winsound.Beep(frequency_in_hertz, duration_in_milliseconds)
        # 1000Hz is a clear, standard beep. 800ms is long enough to grab attention.
        winsound.Beep(1000, 800)
    else:
        # Fallback for Mac/Linux if deployed elsewhere
        sys.stdout.write('\a')
        sys.stdout.flush()
    
    return f"Timer for {exercise_name} completed successfully."