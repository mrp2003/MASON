# Import necessary libraries
import importlib.util  # For dynamic import of generated Python code
import warnings  # To suppress warnings
import time  # To track execution time
import json  # For loading tasks from JSON files
import random  # For task sampling
import os  # For file existence checks
from mason_framework_sample.crew import Mason  # Custom MAS framework (MASON)

# Suppress unnecessary syntax warnings from the 'pysbd' module
warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# Set seed and paths for reproducibility
SEED = 50
HUMANEVAL_FILE = "data/humanEval.jsonl"
MBPP_FILE = "data/mbpp.jsonl"

def load_mbpp_tasks(n=50):
    """
    Loads n tasks from the HumanEval benchmark file.
    Tasks are randomly sampled using a fixed seed for reproducibility.
    """
    with open(HUMANEVAL_FILE, "r") as f:
        tasks = [json.loads(line) for line in f]
    
    random.seed(SEED)
    return random.sample(tasks, min(n, len(tasks)))

def run():
    """
    Main runner that loads tasks, executes them using the MASON framework,
    evaluates their outputs, logs execution details, and computes Pass@1 score.
    """
    tasks = load_mbpp_tasks()
    total_tasks = len(tasks)
    passed_tasks = 0

    for task in tasks:
        # Prepare input dictionary for the agents
        inputs = {
            'input_request': task["prompt"],
            'test_list': task["test"],
            'function_name': task["entry_point"]
        }

        start_time = time.time()
        interaction_count = 0

        try:
            # Initialize the MAS crew
            crew = Mason().crew()

            # Count how many agents/tasks were in the pipeline
            for _ in crew.tasks:
                interaction_count += 1

            # Execute the MAS workflow
            crew.kickoff(inputs=inputs)

        except Exception as e:
            raise Exception(f"An error occurred while running the crew: {e}")
        
        # Calculate total execution time
        execution_time = time.time() - start_time

        # Run the test cases to validate the generated output
        test_passed = run_tests(task["test"], task["entry_point"])

        if test_passed:
            passed_tasks += 1  # Increment if task passed all tests

        # Log results for each task
        with open("mas_humaneval_claude_1.txt", "a") as log_file:
            log_file.write(f"Task ID: {task['task_id']}\n")
            log_file.write(f"Execution Time: {execution_time:.2f} seconds\n")
            log_file.write(f"Number of Agent Interactions: {interaction_count}\n")
            log_file.write(f"Status: {'Passed' if test_passed else 'Failed'}\n")
            log_file.write("-" * 40 + "\n")

    # Compute and log overall Pass@1 score
    pass_at_1_score = evaluate_pass_at_1(passed_tasks, total_tasks)
    with open("mas_humaneval_claude_1.txt", "a") as log_file:
        log_file.write(f"Pass@1 Score: {pass_at_1_score:.2f}\n")
        log_file.write("-" * 40 + "\n")

def run_tests(test_code, entry_point):
    """
    Dynamically loads the generated Python file (output.py),
    imports the function, and runs the provided test code.
    Returns True if all tests pass, otherwise False.
    """
    generated_file = "output.py"

    if not os.path.exists(generated_file):
        print(f"Generated file {generated_file} not found.")
        return False

    try:
        # Dynamically import the generated output module
        spec = importlib.util.spec_from_file_location("output", generated_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        # Check if the expected function exists
        if not hasattr(module, entry_point):
            print(f"Function {entry_point} not found in generated code.")
            return False

        # Retrieve the function
        func = getattr(module, entry_point)
        exec_globals = {"candidate": func}

        # Execute the test code in the context of the function
        exec(test_code, exec_globals)
        exec_globals["check"](func)

        print(f"✅ All tests passed for {entry_point}!")
        return True

    except AssertionError:
        print(f"Test failed for {entry_point}!")
        return False
    except SyntaxError as e:
        print(f"Syntax error in generated code: {e}")
        return False
    except Exception as e:
        print(f"Runtime error: {e}")
        return False

def evaluate_pass_at_1(passed, total):
    """
    Computes the Pass@1 score as a ratio of passed to total tasks.
    """
    return passed / total if total > 0 else 0.0
