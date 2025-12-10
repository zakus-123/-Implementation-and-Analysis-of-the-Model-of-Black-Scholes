from src.black_scholes import BlackScholesPricer

def run_test():
    # --- Paramètres du test ---
    S = 100.0    # Prix actuel (Spot)
    K = 100.0    # Strike (ATM - At The Money)
    T = 1.0      # 1 an
    r = 0.05     # 5% taux sans risque
    sigma = 0.2  # 20% volatilité

    # --- Instanciation ---
    call = BlackScholesPricer(S, K, T, r, sigma, 'call')
    put = BlackScholesPricer(S, K, T, r, sigma, 'put')

    # --- Affichage des résultats ---
    print(f"{'Metric':<15} | {'Call Option':<15} | {'Put Option':<15}")
    print("-" * 50)
    print(f"{'Price':<15} | {call.price():.4f}          | {put.price():.4f}")
    print(f"{'Delta':<15} | {call.delta():.4f}          | {put.delta():.4f}")
    print(f"{'Gamma':<15} | {call.gamma():.4f}          | {put.gamma():.4f}")
    print(f"{'Vega':<15}  | {call.vega():.4f}          | {put.vega():.4f}")
    print(f"{'Theta (Year)':<15}| {call.theta():.4f}          | {put.theta():.4f}")
    print(f"{'Rho':<15}   | {call.rho():.4f}          | {put.rho():.4f}")

    # --- Vérification Put-Call Parity ---
    # C - P = S - K * exp(-rT)
    parity_diff = (call.price() - put.price()) - (S - K * 2.718281828**(-r*T))
    print("-" * 50)
    print(f"Put-Call Parity Check (doit être proche de 0): {parity_diff:.6f}")

if __name__ == "__main__":
    run_test()