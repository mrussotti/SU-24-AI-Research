import os

def run_demo(demo_file):
    print(f"Running {demo_file}...")
    os.system(f"python {demo_file}")

if __name__ == "__main__":
    demos = {
        "1": "regression.py",
        "2": "classification.py",
        "3": "clustering.py"
    }

    while True:
        print("Select a demo to run:")
        print("1. Regression Demo")
        print("2. Classification Demo")
        print("3. Clustering Demo")
        print("4. Exit")

        choice = input("Enter the number of the demo you want to run: ")

        if choice == "4":
            print("Exiting...")
            break
        elif choice in demos:
            run_demo(demos[choice])
        else:
            print("Invalid choice. Please try again.")
