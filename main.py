import textwrap
# from IPython.display import Markdown
import google.generativeai as genai
import os
import streamlit as st
import graphviz
import json

os.environ['GOOGLE_APU_KEY']="AIzaSyBJtToNkzQeaPV1-3NT_6iHsRNFgcYR7y8"
genai.configure(api_key=os.environ['GOOGLE_APU_KEY'])
model = genai.GenerativeModel('gemini-pro')
def to_markdown(text):
    text = text.replace("•", " *")
    return textwrap.indent(text,">",predicate=lambda _: True)   

st.title("AI Code Explainer")
Code_Snippet = st.text_area("Enter your code")

if st.button("Show Code"):
    st.code(Code_Snippet)

if st.button("Show Explanation"):
    code_example = f"""
    ----------------------------
    Example 1: Code Snippet
    x = 10
    def foo():
        global x
        x = 5

    foo()
    print(x)
    Correct output: 5
    Code Explaination: Inside the foo function, the global keyword is used to modify the global variable x to be 5.
    So, print(x) outside the function print the modfied value is 5.
    -----------------------------

    Example 2: Code Snippet
    def modify_list(input_list):
    input_list.append(4)
    input_list = [1,2,3]
    my_list = [0]
    modify_list(my_list)
    print(my_list)
    Correct output: [0, 4]
    Code Explaination: Inside the modify_list function, an element 4 is appended to input_list.
    Then, input_list is reassigned to a new list [1,2,3], but this change doesn't affeact the original list.
    So, print(my_list) outputs [0, 4].
    ------------------------------
    """


    prompt = f"""
    Your Task is to act as Code Explainer.
    I'll give you a Code Snippet.
    Your Job is to explain the Code Snippet step-by-step.
    Break down the code into as many steps as possible.
    Share intermediate checkpoints & steps along with results.
    Few good examples of python code output between #### seperator:
    ####
    {code_example}
    ####
    Code Snippet is shared below, delimited with triple backticks:
    ```
    {Code_Snippet}
    ```
    """
    completion = model.generate_content(prompt)
    st.write(to_markdown(completion.text))

if st.button("Show flowchart"):
    python_code_example = """
    ----------------------------
    Example 1: Code Snippet
    def bubble_sort(arr):
        n = len(arr)
        for i in range(n):
            for j in range(0, n-i-1):
                if arr[j] > arr[j+1]:
                    arr[j], arr[j+1] = arr[j+1], arr[j]
        return arr

    arr = [64, 34, 25, 12, 22, 11, 90]
    sorted_arr = bubble_sort(arr)
    print(sorted_arr)

    dot code: 
    digraph G {
        node [shape=box];
        
        start [label="Start", shape=circle];
        input [label="Input Array", shape=box];
        outer_loop [label="For i in range(n)", shape=box];
        inner_loop [label="For j in range(n-i-1)", shape=box];
        comparison [label="arr[j] > arr[j+1]?", shape=diamond];
        swap [label="Swap arr[j] and arr[j+1]", shape=box];
        end_inner_loop [label="End Inner Loop", shape=box];
        end_outer_loop [label="End Outer Loop", shape=box];
        return [label="Return Sorted Array", shape=box];
        stop [label="Stop", shape=circle];
        
        start -> input;
        input -> outer_loop;
        outer_loop -> inner_loop;
        inner_loop -> comparison;
        comparison -> swap [label="True"];
        swap -> end_inner_loop;
        comparison -> end_inner_loop [label="False"];
        end_inner_loop -> inner_loop [label="Continue Inner Loop"];
        end_inner_loop -> end_outer_loop [label="End Inner Loop"];
        end_outer_loop -> outer_loop [label="Continue Outer Loop"];
        outer_loop -> return [label="End Outer Loop"];
        return -> stop;
    }


    -----------------------------

    Example 2: Code Snippet
    def find_prime_numbers(n):
        primes = []
        for num in range(2, n+1):
            is_prime = True
            for j in range(2, int(num ** 0.5) + 1):
                if num % j == 0:
                    is_prime = False
                    break
            if is_prime:
                primes.append(num)
        return primes

    n = 20
    prime_numbers = find_prime_numbers(n)
    print(prime_numbers)

    dot code:
    digraph G {
        node [shape=box];

        start [label="Start", shape=circle];
        input [label="Input n", shape=box];
        init_primes [label="Initialize primes list", shape=box];
        outer_loop [label="For num in range(2, n+1)", shape=box];
        init_is_prime [label="Set is_prime = True", shape=box];
        inner_loop [label="For i in range(2, sqrt(num)+1)", shape=box];
        check_divisible [label="num % j == 0?", shape=diamond];
        set_not_prime [label="Set is_prime = False", shape=box];
        end_inner_loop [label="End Inner Loop", shape=box];
        append_prime [label="Append num to primes", shape=box];
        end_outer_loop [label="End Outer Loop", shape=box];
        return [label="Return primes list", shape=box];
        stop [label="Stop", shape=circle];

        start -> input;
        input -> init_primes;
        init_primes -> outer_loop;
        outer_loop -> init_is_prime;
        init_is_prime -> inner_loop;
        inner_loop -> check_divisible;
        check_divisible -> set_not_prime [label="True"];
        set_not_prime -> end_inner_loop;
        check_divisible -> end_inner_loop [label="False"];
        end_inner_loop -> outer_loop [label="Continue Outer Loop"];
        end_inner_loop -> append_prime [label="is_prime is True"];
        append_prime -> end_outer_loop;
        end_outer_loop -> return;
        return -> stop;
    }

    ------------------------------
    """

    prompt = f"""
        Your Task is to act as generater of a dot code for graphiz to generate flowchart.
        I'll give you a Code Snippet.
        Your Job is to generate a dot code for graphiz to generate flowchart
        Few good examples of python code output between #### seperator:
        ####
        {python_code_example}
        ####
        Code Snippet is shared below, delimited with triple backticks:
        ```
        {Code_Snippet}
        ```
        """
    completions = model.generate_content(prompt)

    # cwd = os.getcwd()
    # dot_file_path:str = os.path.join(cwd,"flowchart/mygraph.dot")
    # os.remove(dot_file_path)

    cwd = os.getcwd()
    dot_file_path:str = r"/mount/src/ai_code_explainer/flowchart/mygraph.dot"
    os.makedirs(os.path.dirname(dot_file_path), exist_ok=True)

    with open(dot_file_path, "w") as f:
        # Write the DOT graph definition
        f.write(completions.text)

    with open(dot_file_path, 'r') as fr:
        lines = fr.readlines()
        with open(dot_file_path, 'w') as fw:
            for line in lines:
                if line.strip('\n') != "```":
                    fw.write(line)
        print(lines)

    # Read the DOT file
    # dot_graph = graphviz.Source.from_file(dot_file_path)
    png_path:str = r"/mount/src/ai_code_explainer/flowchart/img.png"
    img_path:str = r"/mount/src/ai_code_explainer/flowchart/img"
    os.makedirs(os.path.dirname(png_path), exist_ok=True)
    os.makedirs(os.path.dirname(img_path), exist_ok=True)
    # dot_graph.render(img_path, format='png')
    # st.image(png_path, caption="Flowchart")
    
    d = os.path.exists(dot_file_path)
    i = os.path.exists(img_path)
    p = os.path.exists(png_path)
    st.code(d)
    st.code(i)
    st.code(p)
    # st.code(img_path)
    # st.code(png_path)
    os.remove(img_path)
    os.remove(dot_file_path)
    os.remove(png_path)
