import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sys

# Ajout du chemin pour importer ta classe
sys.path.append(os.path.abspath('src'))
from src.black_scholes import BlackScholesPricer

# --- CONFIGURATION DU STYLE ---
# "whitegrid" est meilleur pour les rapports écrits (fond blanc)
sns.set_style("whitegrid")
# Configuration des polices pour faire "Sérieux/Académique"
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 12,
    'ytick.labelsize': 12,
    'figure.titlesize': 18,
    'lines.linewidth': 2.5
})

def generate_graphs():
    # --- 1. Paramètres de Simulation ---
    K = 100       # Strike
    T = 1.0       # Maturité (1 an)
    r = 0.05      # Taux 5%
    sigma = 0.2   # Volatilité 20%
    
    # On génère des prix Spot de 50 à 150
    spots = np.linspace(50, 150, 100)
    
    # Listes pour stocker les résultats
    call_prices = []
    put_prices = []
    call_deltas = []
    call_gammas = []
    
    for s in spots:
        c = BlackScholesPricer(s, K, T, r, sigma, 'call')
        p = BlackScholesPricer(s, K, T, r, sigma, 'put')
        
        call_prices.append(c.price())
        put_prices.append(p.price())
        call_deltas.append(c.delta())
        call_gammas.append(c.gamma())

    # --- 2. Graphique 1 : Prix (Call vs Put) ---
    plt.figure(figsize=(10, 6))
    plt.plot(spots, call_prices, label='Call Option', color='#1f77b4') # Bleu pro
    plt.plot(spots, put_prices, label='Put Option', color='#ff7f0e')   # Orange pro
    
    # Ligne verticale pour le Strike
    plt.axvline(x=K, color='gray', linestyle='--', alpha=0.7, label=f'Strike (K={K})')
    
    plt.title(f"Profil de Prix Black-Scholes ($T={T}$, $\sigma={sigma}$)")
    plt.xlabel("Prix du Sous-jacent ($S_t$)")
    plt.ylabel("Prix de l'Option ($V_t$)")
    plt.legend()
    plt.tight_layout()
    
    filename1 = "bs_prices.png"
    plt.savefig(filename1, dpi=300)
    print(f"[OK] Graphique sauvegardé : {filename1}")
    plt.close()

    # --- 3. Graphique 2 : Delta (Sensibilité) ---
    plt.figure(figsize=(10, 6))
    plt.plot(spots, call_deltas, color='#2ca02c', label='Delta (Call)') # Vert
    
    plt.axvline(x=K, color='gray', linestyle='--', alpha=0.7, label='At-The-Money')
    plt.axhline(y=0.5, color='gray', linestyle=':', alpha=0.5)
    plt.axhline(y=1.0, color='gray', linestyle=':', alpha=0.5)
    plt.axhline(y=0.0, color='gray', linestyle=':', alpha=0.5)
    
    plt.title("Sensibilité Delta ($\Delta$)")
    plt.xlabel("Prix du Sous-jacent ($S_t$)")
    plt.ylabel("Delta (Probabilité équivalente)")
    plt.legend()
    plt.tight_layout()
    
    filename2 = "delta_plot.png"
    plt.savefig(filename2, dpi=300)
    print(f"[OK] Graphique sauvegardé : {filename2}")
    plt.close()

    # --- 4. Graphique 3 : Gamma (Convexité) ---
    plt.figure(figsize=(10, 6))
    plt.plot(spots, call_gammas, color='#d62728', label='Gamma') # Rouge
    
    plt.axvline(x=K, color='gray', linestyle='--', alpha=0.7, label=f'Strike (Risque Max)')
    plt.fill_between(spots, call_gammas, color='#d62728', alpha=0.1) # Remplissage sous la courbe
    
    plt.title("Sensibilité Gamma ($\Gamma$)")
    plt.xlabel("Prix du Sous-jacent ($S_t$)")
    plt.ylabel("Gamma (Instabilité du Delta)")
    plt.legend()
    plt.tight_layout()
    
    filename3 = "gamma_plot.png"
    plt.savefig(filename3, dpi=300)
    print(f"[OK] Graphique sauvegardé : {filename3}")
    plt.close()

if __name__ == "__main__":
    generate_graphs()

   