from typing import Dict


class DecisionEngine:
    """
    Converts probabilistic outputs into actions under latency constraints.
    """

    def __init__(
        self,
        latency_budget_ms: float = 20.0,
    ):
        self.latency_budget_ms = latency_budget_ms

    def decide(
        self,
        probability: float,
        latency_info: Dict[str, float],
        confidence_threshold: float,
    ) -> Dict:
        """
        Make a decision based on probability, latency, and dynamic confidence threshold.
        """

        decision = {
            "execute": False,
            "reason": None,
            "probability": probability,
            "latency_ms": latency_info["total"],
        }

        if probability < confidence_threshold:
            decision["reason"] = "probability_below_threshold"
            return decision

        if latency_info["total"] > self.latency_budget_ms:
            decision["reason"] = "latency_budget_exceeded"
            return decision

        decision["execute"] = True
        decision["reason"] = "accepted"
        return decision
