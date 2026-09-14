import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from client import AgentSessionCompactionTokenizerClient

def main():
    client = AgentSessionCompactionTokenizerClient(max_token_budget=120)
    res = client.compact_session_window()
    print("=== Agent Session Compaction Tokenizer Output ===")
    print(f"Token Budget: {res['max_token_budget']} | Estimated Tokens: {res['total_estimated_tokens']}")
    print(f"Messages: {res['original_messages_count']} -> Retained: {res['retained_messages_count']} (Pruned: {res['pruned_messages_count']})")
    print(f"System Anchor Preserved: {res['system_anchor_preserved']}")
    print("\nCompacted History:")
    for m in res['compacted_session']:
        print(f"  - [{m['role'].upper()}]: {m['content'][:50]}...")

if __name__ == '__main__':
    main()
