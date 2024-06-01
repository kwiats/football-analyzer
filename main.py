from core.app import FootballMatchAnalyzerApp

if __name__ == "__main__":
    try:
        FootballMatchAnalyzerApp().run()
    except KeyboardInterrupt:
        print("\nExiting...")
