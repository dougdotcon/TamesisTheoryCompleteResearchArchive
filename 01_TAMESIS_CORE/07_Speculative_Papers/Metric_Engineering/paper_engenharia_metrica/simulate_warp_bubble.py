import sys
import os
import matplotlib.pyplot as plt
import numpy as np

# Ensure src is in python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from metric_engine import MetricEngineer

def run_warp_simulation():
    print("⚙️ Starting Metric Engineering Simulation...")
    print("-------------------------------------------")
    
    engineer = MetricEngineer()
    
    # Scene: Interstellar Probe "Voyager X"
    # Mass: 1000 kg
    # Propulsion: Ion Thruster (Low Force: 10 N)
    # Goal: Reach 10% c
    
    mass = 1000.0 # kg
    thrust = 100.0 # N (Advanced Ion)
    target_vel = 0.1 * 2.998e8 # 30,000 km/s
    
    # Compare 3 Scenarios
    scenarios = [
        {"label": "Standard Vacuum (Gamma=117)", "gamma": 117.038},
        {"label": "Partial Shield (Gamma=50)", "gamma": 50.0},
        {"label": "Full Warp Bubble (Gamma=1.0)", "gamma": 1.0}
    ]
    
    results = []
    
    print(f"Vehicle Mass: {mass} kg")
    print(f"Thrust: {thrust} N")
    print(f"Target Velocity: {target_vel/1000:.0f} km/s\n")
    
    for sc in scenarios:
        gamma = sc["gamma"]
        
        # Analytical calc for time to reach target
        # a = F / (m * gamma/117)
        # t = v / a
        
        sim_result = engineer.simulate_acceleration(thrust, mass, gamma, 1.0)
        accel = sim_result["acceleration"]
        m_eff = sim_result["mass_effective"]
        
        time_to_target_s = target_vel / accel
        time_to_target_days = time_to_target_s / (24*3600)
        
        energy_cost = engineer.energy_cost_function(gamma, bubble_radius_m=5.0)
        power_req_mw = energy_cost / 1e6 # MW (assuming this is sustained power?)
        # Note: energy_cost_function currently returns raw 'cost unit', interpretation as Power (W) is cleaner
        
        results.append({
            "label": sc["label"],
            "accel": accel,
            "m_eff": m_eff,
            "time_days": time_to_target_days,
            "power_mw": power_req_mw
        })
        
        print(f"[{sc['label']}]")
        print(f"  Effective Mass: {m_eff:.2f} kg")
        print(f"  Acceleration:   {accel:.4f} m/s^2")
        print(f"  Time to 0.1c:   {time_to_target_days:.1f} days")
        print(f"  Power Reqd:     {power_req_mw:.2f} MJ (Bubble Cost Estimate)")
        print("-" * 30)

    # Visualization
    plot_simulation_results(results)
    save_report(results)

def plot_simulation_results(results):
    labels = [r["label"] for r in results]
    times = [r["time_days"] for r in results]
    
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, times, color=['gray', 'orange', 'cyan'])
    
    plt.yscale('log')
    plt.ylabel('Time to Reach 0.1c (Days) [Log Scale]')
    plt.title('Propulsion Efficency: Standard vs Metric Engineering')
    plt.grid(True, axis='y', alpha=0.3)
    
    # Add text on bars
    for bar, time in zip(bars, times):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                f'{time:.1f} d',
                ha='center', va='bottom')
                
    output_path = "Validation/warp_bubble_efficiency.png"
    plt.savefig(output_path)
    print(f"\n✅ Efficiency plot saved: {output_path}")

def save_report(results):
    with open("Validation/interstellar_trip_report.txt", "w") as f:
        f.write("INTERSTELLAR PROPULSION REPORT\n")
        f.write("==============================\n")
        for r in results:
            f.write(f"Scenario: {r['label']}\n")
            f.write(f"  Metric Factor (Gamma): {r['label'].split('=')[-1].strip(')')}\n")
            f.write(f"  Effective Mass: {r['m_eff']:.2f} kg\n")
            f.write(f"  Acceleration: {r['accel']:.4f} m/s^2\n")
            f.write(f"  Trip Time (to 0.1c): {r['time_days']:.2f} days\n")
            f.write("------------------------------\n")
            
    print("✅ Report saved to interstellar_trip_report.txt")

if __name__ == "__main__":
    run_warp_simulation()
