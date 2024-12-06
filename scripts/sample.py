import random

class Python:
    beginner = {
        1: 'Write a python program to calculate GCD of any Number',
        2: 'Write a python program to add int and float number',
        3: 'Write a python program to calculate the grade of a student',
        4: 'Write a python program to reverse a string',
        5: 'Write a python program to check if a number is even or odd',
    }
    
    medium = {
        1: 'Write a python program to find the factorial of a number',
        2: 'Write a python program to find the Fibonacci series up to n terms',
        3: 'Write a python program to count the frequency of elements in a list',
        4: 'Write a python program to find the second largest number in a list',
        5: 'Write a python program to merge two sorted lists',
    }

    hard = {
        1: 'Write a python program to solve the N-Queens problem',
        2: 'Write a python program to implement a binary search tree',
        3: 'Write a python program to find the shortest path in a graph using Dijkstra\'s algorithm',
        4: 'Write a python program to implement a cache using LRU (Least Recently Used) strategy',
        5: 'Write a python program to solve the traveling salesman problem using dynamic programming',
    }

    @classmethod
    def get_questions(cls, num_questions_to_generate, level):
        if level == 'beginner':
            question_pool = cls.beginner
        elif level == 'medium':
            question_pool = cls.medium
        elif level == 'hard':
            question_pool = cls.hard
        else:
            print(f"Unsupported level: {level}")
            return {}

        selected_keys = random.sample(list(question_pool.keys()), k=num_questions_to_generate)
        selected_questions = {key: question_pool[key] for key in selected_keys}

        return selected_questions

def questions(num_questions_to_generate, level):
    return Python.get_questions(num_questions_to_generate, level)
