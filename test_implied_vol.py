from src.black_scholes import BlackScholesPricer

def test_iv():
    # Paramètres
    S, K, T, r = 100, 100, 1, 0.05
    true_sigma = 0.30  # La vérité qu'on veut retrouver
    
    # 1. Calcul du "Prix Marché" théorique
    pricer = BlackScholesPricer(S, K, T, r, true_sigma, 'call')
    market_price = pricer.price()
    
    print(f"1. Volatilité réelle utilisée : {true_sigma*100}%")
    print(f"2. Prix de marché généré      : {market_price:.4f} €")
    
    # 3. Retrouver la vol (Calibration)
    # On réinitialise le pricer avec une vol fausse pour commencer
    pricer_solver = BlackScholesPricer(S, K, T, r, sigma=0.5, option_type='call')
    
    implied_vol = pricer_solver.implied_volatility(market_price)
    
    print(f"3. Volatilité Implicite trouvée : {implied_vol*100:.4f}%")
    
    if abs(implied_vol - true_sigma) < 1e-4:
        print("\n[SUCCÈS] L'algorithme a retrouvé la volatilité exacte !")
    else:
        print("\n[ÉCHEC] Problème de convergence.")

if __name__ == "__main__":
    test_iv()