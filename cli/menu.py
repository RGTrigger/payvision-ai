from rich import print
from main import run_analysis, get_crossover_year
from analytics.report import generate_pdf_report
from analytics.export import export_csv
from analytics.visualization import adoption_heatmap
from analytics.anomaly import detect_anomalies
from analytics.anomaly import realtime_alert


def interactive_menu():
    while True:
        print("\n[cyan]Digital Payment Intelligence Menu[/cyan]")
        print("1. Run Forecast")
        print("2. Show Crossover Year")
        print("3. Generate Report")
        print("4. Export CSV")
        print("5. Adoption Heatmap")
        print("6. Detect Anomalies")
        print("7. System Health Check")
        print("0. Exit")

        choice = input("\nSelect option: ")

        if choice == "1":
            run_analysis()
        elif choice == "2":
            print(get_crossover_year())
        elif choice == "3":
            print(generate_pdf_report())
        elif choice == "4":
            print(export_csv())
        elif choice == "5":
            adoption_heatmap()
        elif choice == "6":
            print(detect_anomalies())
        elif choice == "7":
            print(realtime_alert())
        elif choice == "0":
            break
