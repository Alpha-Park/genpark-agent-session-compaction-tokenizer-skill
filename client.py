import json
from typing import List, Dict, Any, Optional

class AgentSessionCompactionTokenizerClient:
    """
    Production-grade session context window tokenizer and compaction manager.
    Protects system prompt anchor tokens while applying FIFO rolling trim to intermediate dialogue.
    """
    def __init__(self, max_token_budget: int = 4096):
        self.budget = max_token_budget

    def _estimate_tokens(self, text: str) -> int:
        return max(1, int(len(text.split()) * 1.3))

    def compact_session_window(self, messages: Optional[List[Dict[str, str]]] = None) -> Dict[str, Any]:
        if not messages:
            messages = [
                {"role": "system", "content": "You are an autonomous e-commerce purchasing agent with strict budget constraints."},
                {"role": "user", "content": "Search for top 3 rated cordless robot vacuums with automated mop washing stations."},
                {"role": "assistant", "content": "I found Roborock S8 MaxV ($1599), Dreame X40 Ultra ($1499), and Ecovacs Deebot X2 ($999)."},
                {"role": "user", "content": "What is the warranty and battery cycle rating of the Roborock S8?"},
                {"role": "assistant", "content": "The Roborock S8 MaxV offers a 2-year manufacturer warranty and a 4000-cycle battery."},
                {"role": "user", "content": "Proceed to generate single-use virtual card and checkout the Roborock S8."}
            ]

        system_msg = [m for m in messages if m["role"] == "system"]
        dialogue = [m for m in messages if m["role"] != "system"]

        sys_tokens = sum(self._estimate_tokens(m["content"]) for m in system_msg)
        dialogue_budget = self.budget - sys_tokens

        retained_dialogue = []
        current_tokens = 0
        # Retain most recent dialogue backwards
        for m in reversed(dialogue):
            m_tok = self._estimate_tokens(m["content"])
            if current_tokens + m_tok <= dialogue_budget:
                retained_dialogue.insert(0, m)
                current_tokens += m_tok
            else:
                break

        final_messages = system_msg + retained_dialogue
        total_tok = sys_tokens + current_tokens

        return {
            "compaction_id": "ctx_win_8819",
            "max_token_budget": self.budget,
            "total_estimated_tokens": total_tok,
            "original_messages_count": len(messages),
            "retained_messages_count": len(final_messages),
            "pruned_messages_count": len(messages) - len(final_messages),
            "system_anchor_preserved": len(system_msg) > 0,
            "compacted_session": final_messages
        }
