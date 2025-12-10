# Black-Scholes Option Pricing Engine 

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Status](https://img.shields.io/badge/Status-Completed-success)

## Description
Ce projet est une implémentation complète orientée objet du modèle de **Black-Scholes-Merton** pour le pricing d'options Européennes. 
Il a été réalisé dans le cadre de mon Master 1 en Mathématiques Appliquées à l'Ingénierie Financière.

L'objectif n'est pas seulement d'appliquer la formule, mais de fournir une analyse approfondie des sensibilités (**Grecs**) et de résoudre le problème inverse de la **Volatilité Implicite** via des méthodes numériques.

## Fonctionnalités Clés
* **Pricing Analytique :** Calcul exact pour Call et Put.
* **Moteur de Grecs :** Calcul de Delta, Gamma, Vega, Theta, Rho.
* **Calibration de Marché :** Algorithme de **Newton-Raphson** pour extraire la Volatilité Implicite.
* **Visualisation :** Génération de graphiques haute résolution pour l'analyse des risques.

## Structure du Projet
* `src/` : Contient la classe `BlackScholesPricer`.
* `docs/` : Rapport mathématique complet (Preuve du Lemme d'Ito et résolution EDP).
* `notebooks/` : Analyses interactives.

##  Analyse Visuelle

### 1. Profil de Prix et Payoff
Le modèle capture la valeur temps de l'option avant maturité.
![Prix](images/bs_prices.png)

### 2. Gestion des Risques (Delta & Gamma)
Analyse de la sensibilité pour le Delta-Hedging dynamique.
![Delta](images/delta_plot.png)
*Le Gamma (risque de convexité) est maximal à la monnaie :*
![Gamma](images/gamma_plot.png)

##  Exemple d'Utilisation

```python
from src.black_scholes import BlackScholesPricer

# Initialisation d'un Call
call = BlackScholesPricer(S=100, K=100, T=1, r=0.05, sigma=0.2, option_type='call')

# Calcul du Prix et du Delta
print(f"Prix théorique : {call.price():.2f} €")
print(f"Delta de couverture : {call.delta():.2f}")

# Calcul Inverse (Volatilité Implicite)
iv = call.implied_volatility(target_price=10.45)
print(f"Volatilité Implicite : {iv*100:.2f}%")