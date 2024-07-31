import sys
import subprocess

def main():
    if len(sys.argv) != 4:
        print("Something went wrong")
        return

    selected_language = sys.argv[1]
    selected_questions = int(sys.argv[2])
    selected_level = sys.argv[3].lower()

    # Navigating to different Languages
    if selected_language:
        language = selected_language.lower()
        if language == "python":
            import pythonquestion
            questions = pythonquestion.questions(selected_questions, selected_level)
            for i, question in enumerate(questions.values(), start=1):
                print(f"Question {i}: {question}")
        elif language == "java":
            import javaquestion
            questions = javaquestion.questions(selected_questions, selected_level)
            for i, question in enumerate(questions.values(), start=1):
                print(f"Question {i}: {question}")
        elif language == "cpp":
            import cppquestion
            questions = cppquestion.questions(selected_questions, selected_level)
            for i, question in enumerate(questions.values(), start=1):
                print(f"Question {i}: {question}")
        else:
            print(f"Unsupported language: {selected_language}")

if __name__ == "__main__":
    main()