from core.ai_engine import AIEngine


def main():
    print("=" * 45)
    print("       RZXXY AI MARKETING ASSISTANT")
    print("=" * 45)
    print("Type 'exit' to quit.\n")

    engine = AIEngine()

    while True:
        try:
            task = input("You: ").strip()

            if task.lower() in ("exit", "quit"):
                print("Goodbye!")
                break

            if not task:
                continue

            print("\nRZXXY AI: Working...\n")

            result = engine.generate(task)

            print("Categories:", ", ".join(result["categories"]))
            print("\n" + result["answer"] + "\n")

        except RuntimeError as error:
            print("Configuration Error:", error)
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as error:
            print("Error:", error)


if __name__ == "__main__":
    main()
