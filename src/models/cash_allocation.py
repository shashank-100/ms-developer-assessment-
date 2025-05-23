import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from enum import Enum

class RiskTolerance(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class CashAllocationModel:
    def __init__(self):
        self.risk_weights = {
            RiskTolerance.LOW: {
                'vix_weight': 0.4,
                'fii_dii_weight': 0.3,
                'market_breadth_weight': 0.3
            },
            RiskTolerance.MEDIUM: {
                'vix_weight': 0.33,
                'fii_dii_weight': 0.33,
                'market_breadth_weight': 0.34
            },
            RiskTolerance.HIGH: {
                'vix_weight': 0.3,
                'fii_dii_weight': 0.4,
                'market_breadth_weight': 0.3
            }
        }

    def calculate_vix_score(self, vix_data: pd.DataFrame) -> float:
        """
        Calculate score based on VIX levels
        Higher VIX = Higher cash allocation
        """
        current_vix = vix_data['Close'].iloc[-1]
        vix_mean = vix_data['Close'].mean()
        vix_std = vix_data['Close'].std()
        
        # Normalize VIX score between 0 and 1
        vix_score = min(1.0, max(0.0, (current_vix - vix_mean) / (2 * vix_std) + 0.5))
        return vix_score

    def calculate_fii_dii_score(self, fii_dii_data: pd.DataFrame) -> float:
        """
        Calculate score based on FII/DII flows
        Negative flows = Higher cash allocation
        """
        recent_fii = fii_dii_data['FII'].iloc[-30:].sum()  # Last 30 days
        recent_dii = fii_dii_data['DII'].iloc[-30:].sum()
        
        # Normalize the combined flow score
        total_flow = recent_fii + recent_dii
        max_flow = max(abs(fii_dii_data['FII'].sum()), abs(fii_dii_data['DII'].sum()))
        
        flow_score = 1 - min(1.0, max(0.0, (total_flow + max_flow) / (2 * max_flow)))
        return flow_score

    def calculate_market_breadth_score(self, breadth_data: pd.DataFrame) -> float:
        """
        Calculate score based on market breadth
        Lower breadth = Higher cash allocation
        """
        current_breadth = breadth_data['adv_dec_ratio'].iloc[-1]
        breadth_mean = breadth_data['adv_dec_ratio'].mean()
        breadth_std = breadth_data['adv_dec_ratio'].std()
        
        # Normalize breadth score between 0 and 1
        breadth_score = 1 - min(1.0, max(0.0, (current_breadth - breadth_mean) / (2 * breadth_std) + 0.5))
        return breadth_score

    def calculate_cash_allocation(self,
                                vix_data: pd.DataFrame,
                                fii_dii_data: pd.DataFrame,
                                breadth_data: pd.DataFrame,
                                risk_tolerance: RiskTolerance = RiskTolerance.MEDIUM) -> Dict:
        """
        Calculate recommended cash allocation based on market indicators
        """
        # Calculate individual scores
        vix_score = self.calculate_vix_score(vix_data)
        fii_dii_score = self.calculate_fii_dii_score(fii_dii_data)
        breadth_score = self.calculate_market_breadth_score(breadth_data)
        
        # Get weights based on risk tolerance
        weights = self.risk_weights[risk_tolerance]
        
        # Calculate weighted score
        weighted_score = (
            vix_score * weights['vix_weight'] +
            fii_dii_score * weights['fii_dii_weight'] +
            breadth_score * weights['market_breadth_weight']
        )
        
        # Convert score to cash allocation percentage (0-30%)
        cash_allocation = weighted_score * 30
        
        return {
            'cash_allocation': round(cash_allocation, 2),
            'vix_score': round(vix_score * 100, 2),
            'fii_dii_score': round(fii_dii_score * 100, 2),
            'breadth_score': round(breadth_score * 100, 2),
            'risk_tolerance': risk_tolerance.value
        }

    def get_allocation_recommendation(self, cash_allocation: float) -> str:
        """
        Get a text recommendation based on the cash allocation percentage
        """
        if cash_allocation < 10:
            return "Market conditions appear favorable. Consider maintaining a minimal cash position."
        elif cash_allocation < 20:
            return "Moderate market uncertainty. Consider maintaining a balanced cash position."
        else:
            return "High market uncertainty. Consider maintaining a significant cash position for potential opportunities." 