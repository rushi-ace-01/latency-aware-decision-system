from typing import Dict


class DecisionEngine:
    """
    Converts probabilistic outputs into actions under latency constraints.
    """

    def __init__(
        self,
        min_confidence: float = 0.65,
        latency_budget_ms: float = 20.0,
    ):
        self.min_confidence = min_confidence
        self.latency_budget_ms = latency_budget_ms

    def decide(
        self,
        probability: float,
        latency_info: Dict[str, float],
    ) -> Dict:
        """
        Make a decision based on probability and latency.
        """

        decision = {
            "execute": False,
            "reason": None,
            "probability": probability,
            "latency_ms": latency_info["total"],
        }

        if probability < self.min_confidence:
            decision["reason"] = "probability_below_threshold"
            return decision

        if latency_info["total"] > self.latency_budget_ms:
            decision["reason"] = "latency_budget_exceeded"
            return decision

        decision["execute"] = True
        decision["reason"] = "accepted"
        return decision

from core.decision import DecisionEngine

engine = DecisionEngine()
print(engine.decide(0.9, {"total": 10}))
print(engine.decide(0.4, {"total": 10}))
print(engine.decide(0.9, {"total": 30}))
