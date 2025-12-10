import numpy as np
from scipy.stats import norm

class BlackScholesPricer:
    """
    Implémentation du modèle de Black-Scholes-Merton pour les options Européennes.
    
    Attributs:
    ----------
    S : float
        Prix spot de l'actif sous-jacent.
    K : float
        Prix d'exercice (Strike).
    T : float
        Temps restant avant maturité (en années).
    r : float
        Taux d'intérêt sans risque (ex: 0.05 pour 5%).
    sigma : float
        Volatilité de l'actif sous-jacent (ex: 0.2 pour 20%).
    option_type : str
        Type de l'option : 'call' ou 'put'.
    """

    def __init__(self, S: float, K: float, T: float, r: float, sigma: float, option_type: str = 'call'):
        self.S = S
        self.K = K
        self.T = T
        self.r = r
        self.sigma = sigma
        self.option_type = option_type.lower()

        if self.option_type not in ['call', 'put']:
            raise ValueError("L'argument option_type doit être 'call' ou 'put'")
        if self.sigma < 0 or self.T < 0:
            raise ValueError("La volatilité et le temps doivent être positifs.")

    def _d1(self) -> float:
        """Calcule le terme d1 de la formule de Black-Scholes."""
        if self.T == 0:
            return np.inf if self.S > self.K else -np.inf
        return (np.log(self.S / self.K) + (self.r + 0.5 * self.sigma ** 2) * self.T) / (self.sigma * np.sqrt(self.T))

    def _d2(self) -> float:
        """Calcule le terme d2 (d1 - sigma * sqrt(T))."""
        return self._d1() - self.sigma * np.sqrt(self.T)

    def price(self) -> float:
        """Retourne le prix théorique de l'option."""
        if self.T == 0:
            # Payoff à maturité
            if self.option_type == 'call':
                return max(self.S - self.K, 0.0)
            else:
                return max(self.K - self.S, 0.0)

        d1 = self._d1()
        d2 = self._d2()

        if self.option_type == 'call':
            price = self.S * norm.cdf(d1) - self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
        else:
            price = self.K * np.exp(-self.r * self.T) * norm.cdf(-d2) - self.S * norm.cdf(-d1)
        
        return price

    # --- Les Grecs (Analytiques) ---

    def delta(self) -> float:
        """
        Delta: Sensibilité du prix de l'option par rapport au prix du sous-jacent (dS).
        Représente le ratio de couverture.
        """
        d1 = self._d1()
        if self.option_type == 'call':
            return norm.cdf(d1)
        else:
            return norm.cdf(d1) - 1.0


    def gamma(self) -> float:
        """
        Gamma: Sensibilité du Delta par rapport au prix du sous-jacent (d^2S).
        Mesure la convexité de l'option. Identique pour Call et Put.
        """
        d1 = self._d1()
        return norm.pdf(d1) / (self.S * self.sigma * np.sqrt(self.T))

    def vega(self) -> float:
        """
        Vega: Sensibilité par rapport à la volatilité (dSigma).
        Identique pour Call et Put.
        Attention: Souvent exprimé pour 1% de changement de vol (ici brut).
        """
        d1 = self._d1()
        return self.S * np.sqrt(self.T) * norm.pdf(d1)

    def theta(self) -> float:
        """
        Theta: Sensibilité par rapport au temps (Time Decay).
        Généralement négatif pour les options Long.
        Exprimé ici en "par année". Pour avoir par jour, diviser par 365.
        """
        d1 = self._d1()
        d2 = self._d2()
        
        term1 = - (self.S * norm.pdf(d1) * self.sigma) / (2 * np.sqrt(self.T))
        
        if self.option_type == 'call':
            term2 = - self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(d2)
            return term1 + term2
        else:
            term2 = self.r * self.K * np.exp(-self.r * self.T) * norm.cdf(-d2)
            return term1 + term2

    def rho(self) -> float:
        """
        Rho: Sensibilité par rapport au taux d'intérêt sans risque (dr).
        """
        d2 = self._d2()
        if self.option_type == 'call':
            return self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(d2)
        else:
            return -self.K * self.T * np.exp(-self.r * self.T) * norm.cdf(-d2)
        
    # ---------------------------------------------------------
    #  BlackScholesPricer
    # ---------------------------------------------------------
        

    def implied_volatility(self, target_price: float, tol: float = 1e-5, max_iter: int = 100) -> float:
        """
        Calcule la volatilité implicite en utilisant la méthode de Newton-Raphson.
        
        Args:
            target_price (float): Le prix de marché de l'option.
            tol (float): La tolérance d'erreur acceptée (précision).
            max_iter (int): Nombre maximum d'itérations avant arrêt.
            
        Returns:
            float: La volatilité implicite (ex: 0.20 pour 20%).
            Retourne None si l'algorithme ne converge pas.
        """
        # 1. Estimation initiale (Seed)
        sigma = 0.5  # On commence avec une vol de 50% par défaut
        
        for i in range(max_iter):
            # On met à jour la volatilité de l'instance actuelle
            self.sigma = sigma
            
            # Calcul du prix et du vega avec cette volatilité
            price = self.price()
            vega = self.vega()
            
            # Différence entre prix modèle et prix cible
            diff = target_price - price
            
            # Critère d'arrêt (Convergence atteinte)
            if abs(diff) < tol:
                return sigma
            
            # Protection contre division par zéro (si Vega est nul)
            if abs(vega) < 1e-8:
                # Si le Vega est nul, Newton ne marche pas (souvent pour options Deep ITM/OTM)
                # On arrête pour éviter l'erreur.
                print("Attention: Vega trop faible, convergence impossible.")
                return None
                
            # Mise à jour Newton-Raphson
            sigma = sigma + diff / vega
            
        print("Attention: Nombre maximum d'itérations atteint.")
        return None

