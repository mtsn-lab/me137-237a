import time
import numpy as np


class ITLoadSimulator:
    def __init__(self, base_load_kw=500, variability=50):
        self.base_load = base_load_kw    # Baseline power draw of the hall (kW)
        self.variability = variability  # Random noise amplitude (kW)
        self.time_step = 0

    def get_current_load(self):
        """
        Generates a synthetic IT thermal load consisting of:
        1. A constant baseline load
        2. A slow-moving sine wave (simulating diurnal server traffic)
        3. Stochastic +200 kW spikes (simulating batch compute jobs)
        4. Uniform random measurement/workload noise
        """
        # Diurnal Cycle (100 ticks per cycle for classroom demonstration)
        diurnal = 100 * np.sin(2 * np.pi * self.time_step / 100)

        # Sudden Spikes (10% probability of a +200 kW batch job jump)
        spike = 200 if np.random.random() > 0.9 else 0

        # Random Noise
        noise = np.random.uniform(-self.variability, self.variability)

        total_load = self.base_load + diurnal + spike + noise
        self.time_step += 1

        return round(float(total_load), 2)


if __name__ == "__main__":
    sim = ITLoadSimulator()
    print("Time(s) | IT Load (kW)")
    print("-" * 25)
    for t in range(1000):
        load = sim.get_current_load()
        print(f"{t:02d}      | {load} kW")
        time.sleep(0.5)