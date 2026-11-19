import numpy as np
import time

class ITLoadSimulator:
    def __init__(self, base_load_kw=500, variability=50):
        self.base_load = base_load_kw    # Baseline power draw of the hall
        self.variability = variability  # Random noise in kW
        self.time_step = 0

    def get_current_load(self):
        """
        Generates a synthetic load consisting of:
        1. A base load
        2. A slow-moving sine wave (simulating diurnal traffic)
        3. Random 'spikes' (simulating batch jobs)
        """
        # Diurnal Cycle (24-hour period represented as 100 ticks for the lab)
        diurnal = 100 * np.sin(2 * np.pi * self.time_step / 100)
        
        # Sudden Spikes (10% chance of a 200kW jump)
        spike = 200 if np.random.random() > 0.9 else 0
        
        # Random Noise
        noise = np.random.uniform(-self.variability, self.variability)
        
        total_load = self.base_load + diurnal + spike + noise
        self.time_step += 1
        
        return round(total_load, 2)

# --- FOR CLASSROOM DEMONSTRATION ---
if __name__ == "__main__":
    sim = ITLoadSimulator()
    print("Time(s) | IT Load (kW)")
    print("-" * 25)
    for t in range(1000):
        load = sim.get_current_load()
        print(f"{t:02d}      | {load} kW")
        time.sleep(0.5) # Simulating real-time for the demo