import hupper
import sys
import os

def main():
    from Main import App
    app = App()
    app.mainloop()

if __name__ == "__main__":
    if os.environ.get("HUPPER_RELOAD_ENABLED") is None:
        # Start hupper reloader
        reloader = hupper.start_reloader('run.main')
    else:
        # Run the application
        main() 