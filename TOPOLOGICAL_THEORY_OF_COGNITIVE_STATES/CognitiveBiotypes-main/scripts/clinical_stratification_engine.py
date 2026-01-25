import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def physics_based_classifier(connectivity_z, phase_coherence, hormonal_viscosity):
    """
    The Core Logic of the DEPRESS-ANALIST.
    Maps biological data to Physics Biotypes.
    
    1. Connectivity Z (Structure) -> Entropic Trap?
    2. Phase Coherence (Function) -> Desynchronized?
    3. Hormonal Viscosity (Medium) -> Overdamped?
    """
    diagnosis = []
    treatment = []
    
    # 1. Check Viscosity First (The Medium)
    if hormonal_viscosity > 3.0:
        diagnosis.append("Viscous Medium (Hormonal Fog)")
        treatment.append("Endocrine Regulation / Stress Reduction")
    
    # 2. Check Entropic Trap (The Energy Well)
    if connectivity_z < -0.5:
        diagnosis.append("Entropic Gravity Well (Cognitive Biotype +)")
        treatment.append("TMS (Energy Injection)")
        
    # 3. Check Resonance (The Rhythm)
    if phase_coherence < 0.6:
        if "Entropic Gravity Well (Cognitive Biotype +)" not in diagnosis:
            # If structure is fine but rhythm is off
            diagnosis.append("Oscillatory Chaos (Phase Desync)")
            treatment.append("Neurofeedback / Alpha-Training")
            
    if not diagnosis:
        return "Healthy / Sub-clinical", "Observation"
        
    return " + ".join(diagnosis), " + ".join(treatment)

def simulate_patient_cohort(n=50):
    """
    Simulates a diverse group of patients to test the Engine.
    """
    patients = []
    
    for i in range(n):
        # Generate random biological parameters
        # Z-score: Normal ~ 0, Depressed ~ -1.0
        conn_z = np.random.normal(-0.2, 0.8) 
        
        # Coherence: 0 to 1
        coherence = np.random.beta(5, 2) 
        
        # Viscosity: Normal ~ 1, High Stress ~ 5
        viscosity = np.random.gamma(2, 1.0)
        
        dx, rx = physics_based_classifier(conn_z, coherence, viscosity)
        
        patients.append({
            'Patient_ID': f"PT_{i:03d}",
            'Connectivity_Z': round(conn_z, 2),
            'Phase_Coherence': round(coherence, 2),
            'Hormonal_Viscosity': round(viscosity, 2),
            'Physics_Diagnosis': dx,
            'Precision_Rx': rx
        })
        
    return pd.DataFrame(patients)

def visualize_stratification(df):
    plt.figure(figsize=(12, 8))
    sns.set_style("whitegrid")
    
    # We plot the 3D phase space in 2D using Color/Size
    sns.scatterplot(
        data=df,
        x='Connectivity_Z',
        y='Hormonal_Viscosity',
        hue='Physics_Diagnosis',
        style='Precision_Rx',
        s=100,
        palette='viridis'
    )
    
    plt.title("Clinical Stratification: The Grand Unification", fontsize=16)
    plt.axvline(-0.5, color='red', linestyle='--', label='Entropic Event Horizon')
    plt.axhline(3.0, color='orange', linestyle='--', label='Viscosity Threshold')
    
    plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    plt.savefig('clinical_stratification_map.png', dpi=300)
    print("Stratification Map generated: 'clinical_stratification_map.png'")
    
    # Save CSV report
    df.to_csv('patient_cohort_analysis.csv', index=False)
    print("Cohort Report saved: 'patient_cohort_analysis.csv'")

if __name__ == "__main__":
    print("Running Clinical Stratification Engine...")
    df = simulate_patient_cohort()
    visualize_stratification(df)
    
    print("\nSample Diagnoses:")
    print(df[['Patient_ID', 'Physics_Diagnosis', 'Precision_Rx']].head(10))
