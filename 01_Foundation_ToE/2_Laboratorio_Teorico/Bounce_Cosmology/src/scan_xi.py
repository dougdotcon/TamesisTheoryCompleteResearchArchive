import numpy as np
from src.physics_models.black_hole_universe import UniversosBuracoNegro
from src.physics_models.relativity import CamposEscalarAcoplados
import warnings

def test_xi(xi):
    print(f"\n--- Testing Xi = {xi:.1e} ---")
    M_parent = 5e22
    bhu = UniversosBuracoNegro(M_parent)
    condicoes = bhu.gerar_condicoes_iniciais_rebote()
    
    # Normalizations
    condicoes['a_inicial'] = 1.0
    condicoes['pi_phi_inicial'] = 0.0
    condicoes['phi_inicial'] = 1.0 
    
    modelo = CamposEscalarAcoplados(xi=xi, alpha=-1e-6)
    
    try:
        evol = modelo.evolucao_campo_bounce(
            t_span=(0.0, 5000.0), # Optimized window
            n_pontos=500,
            initial_conditions=condicoes
        )
        
        if evol['sucesso']:
            val_a = evol['a'][-1]
            try:
                N = np.log(val_a) # Since a_init=1.0
            except:
                N = 0
            print(f"✅ Success! Final a = {val_a:.4e} -> N = {N:.4f} e-folds")
            return N
        else:
            msg = evol.get('mensagem', 'No Message')
            print(f"❌ Failed: {msg}")
            return -1
    except Exception as e:
        print(f"❌ Exception: {e}")
        return -1

if __name__ == "__main__":
    import concurrent.futures
    import time

    xis = [1.0, 10.0, 100.0, 1000.0, 3000.0, 5000.0, 10000.0]
    
    print(f"=== PARALLEL SCAN Starting for {len(xis)} candidates (LSODA, t=5000) ===", flush=True)
    start_time = time.time()
    
    results = {}
    
    # Use ProcessPoolExecutor for CPU-bound tasks (simulations)
    with concurrent.futures.ProcessPoolExecutor() as executor:
        # Submit all tasks
        future_to_xi = {executor.submit(test_xi, xi): xi for xi in xis}
        
        for future in concurrent.futures.as_completed(future_to_xi):
            xi = future_to_xi[future]
            try:
                N = future.result()
                results[xi] = N
                print(f"--> Finished Xi = {xi:.1e} : N = {N:.4f}", flush=True)
            except Exception as exc:
                print(f"--> Xi = {xi:.1e} generated an exception: {exc}", flush=True)
                results[xi] = -1

    elapsed = time.time() - start_time
    print(f"\n=== SUMMARY (Time: {elapsed:.2f}s) ===")
    # Sort by Xi for readable output
    for xi in sorted(results.keys()):
        N = results[xi]
        print(f"Xi = {xi:.1e} : N = {N:.4f}")
