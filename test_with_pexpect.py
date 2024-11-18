import pexpect

## Does not work because curses constantly rewrites the output
def test_initial_screen_state():
    # Launch the application
    app_process = pexpect.spawn("python workout.py")  # Replace 'your_command_here' with the actual command

    # Wait for the initial output
    #app_process.expect("0\s+\n00:00:00\s+\n--\s+\n", timeout=5)  # Match the expected pattern
    app_process.expect("0", timeout=5)  # Match the expected pattern

    # Get the matched output
    output = app_process.before.decode("utf-8")

    # Validate the output
    expected_output = "0\n00:00:00\n--\n"
    assert output.strip() == expected_output.strip(), f"Unexpected output: {output}"

    # Clean up
    app_process.terminate()

if __name__ == "__main__":
    test_initial_screen_state()
