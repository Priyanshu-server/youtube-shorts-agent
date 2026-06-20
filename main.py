import settings  # loads .env and configures logging on import
from registry import REGISTRY
from src.utils.logging import bind_context, clear_context




def pick_agent() -> int:
    print("\nAvailable agents:")
    for i, entry in enumerate(REGISTRY):
        print(f"  [{i + 1}] {entry.agent_name} — {entry.agent_description}")
    print()

    while True:
        raw = input("Select an agent (number): ").strip()
        if raw.isdigit() and 1 <= int(raw) <= len(REGISTRY):
            return int(raw) - 1
        print(f"  Please enter a number between 1 and {len(REGISTRY)}.")


def collect_inputs(entry) -> dict[str, str]:
    collected: dict[str, str] = {}
    for key, prompt in entry.inputs.items():
        collected[key] = input(prompt).strip()
    return collected


def main() -> None:
    idx = pick_agent()
    entry = REGISTRY[idx]

    bind_context(agent=entry.agent_name)
    try:
        collected = collect_inputs(entry)

        graph = entry.factory()
        output = graph.invoke(entry.build_graph_input(collected))

        print("\n" + "-" * 40)
        print(output[entry.output_key])
        print("-" * 40 + "\n")
    finally:
        clear_context()


if __name__ == "__main__":
    main()
