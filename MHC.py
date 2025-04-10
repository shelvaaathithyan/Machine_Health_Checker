import pandas as pd
import tkinter as tk
from tkinter import ttk
from sklearn.tree import DecisionTreeClassifier
def load_dataset():
 data = []
 with open('machines.csv', 'r') as file:
 for line in file:
 machine_type, problem, *solution = line.strip().split(',')
 data.append([machine_type.strip(), problem.strip(), ' '.join(solution).strip()])
 return pd.DataFrame(data, columns=['Machine_Type', 'Problem', 'Solution'])
def get_problems(machine_type):
 df = load_dataset()
 return df[df['Machine_Type'] == machine_type]['Problem'].tolist()
def get_solution(machine_type, problem):
 df = load_dataset()
 solution = df[(df['Machine_Type'] == machine_type) & (df['Problem'] ==
problem)]['Solution'].values
 if solution.size > 0:
 return solution[0]
 else:
 return "Solution not found for the provided problem."
def train_model():
 df = load_dataset()
 X = pd.get_dummies(df[['Machine_Type', 'Problem']], drop_first=True)
 y = df['Solution']
 model = DecisionTreeClassifier()
 model.fit(X, y)
 return model, X # Return both the trained model and the feature matrix X
def predict_solution(model, X, machine_type, problem):
input_data = pd.DataFrame([[machine_type, problem]], columns=['Machine_Type',
'Problem'])
 input_data_encoded = pd.get_dummies(input_data, columns=['Machine_Type',
'Problem'], drop_first=True)
 # Ensure all columns present in training data are present in input data
 missing_cols = set(X.columns) - set(input_data_encoded.columns)
 for col in missing_cols:
 input_data_encoded[col] = 0
 input_data_encoded = input_data_encoded[X.columns] # Reorder columns to match
training data
 prediction = model.predict(input_data_encoded)
 return prediction[0]
def submit():
 machine_type = machine_var.get()
 problem = problem_var.get()
 solution = predict_solution(model, X, machine_type, problem) # Pass the trained model
and X
 solution_label.config(text=solution)
def update_problems(event=None):
 machine_type = machine_var.get()
 problems = get_problems(machine_type)
 problem_var.set('')
 problem_menu['menu'].delete(0, 'end')
 for problem in problems:
 problem_menu['menu'].add_radiobutton(label=problem, variable=problem_var,
value=problem)
def select_machine(machine_type):
 machine_var.set(machine_type)
 update_problems()
root = tk.Tk()
root.title("Machine Health Monitoring System")
style = ttk.Style()
style.theme_use('clam')
style.configure('TFrame', background='#f0f0f0')
style.configure('TButton', background='#CCCCCC', foreground='white', font=('Arial', 14)) #
Changed color to #CCCCCC
style.configure('TRadiobutton', background='#f0f0f0', font=('Arial', 14))
style.configure('TLabel', background='#f0f0f0', font=('Arial', 16))
main_frame = ttk.Frame(root, padding=20)
main_frame.grid(row=0, column=0, sticky='nsew')
header_label = ttk.Label(main_frame, text="Machine Health Checking System",
font=('Arial', 24, 'bold'), background='#f0f0f0', foreground='#000000')
header_label.pack(pady=(0, 20))
machine_frame = ttk.Frame(main_frame)
machine_frame.pack()
ttk.Label(machine_frame, text="Select Machine Type:", font=('Arial', 18),
background='#f0f0f0').grid(row=0, column=0, padx=5, pady=5, sticky='w')
machine_var = tk.StringVar(root)
machine_options = load_dataset()['Machine_Type'].unique()
for i, machine in enumerate(machine_options):
 ttk.Button(machine_frame, text=machine, command=lambda m=machine:
select_machine(m), style='TButton').grid(row=i+1, column=0, padx=10, pady=5, sticky='w')
problem_frame = ttk.Frame(main_frame)
problem_frame.pack()
select_problem_label = ttk.Label(problem_frame, text="Select Problem:", font=('Arial', 18),
background='#f0f0f0', foreground='#000000')
select_problem_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')
problem_var = tk.StringVar(root)
problem_menu = ttk.OptionMenu(problem_frame, problem_var, '', style='TButton')
problem_menu.grid(row=0, column=1, padx=10, pady=5, sticky='ew')
submit_button = ttk.Button(main_frame, text="Submit", command=submit, style='TButton')
submit_button.pack(pady=(20, 10)) # corrected the missing value for pady
style.configure('TButton', foreground='black', background='#CCCCCC')
solution_frame = ttk.Frame(main_frame)
solution_frame.pack()
ttk.Label(solution_frame, text="Solution:", font=('Arial', 18), background='#f0f0f0',
foreground='#000000').grid(row=0, column=0, padx=5, pady=5, sticky='w')
solution_label = ttk.Label(solution_frame, text="", font=('Arial', 16), wraplength=500,
background='#f0f0f0')
solution_label.grid(row=0, column=1, padx=10, pady=5, sticky='w')
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
main_frame.grid_rowconfigure((0, 1, 2, 3), weight=1)
main_frame.grid_columnconfigure(0, weight=1)
model, X = train_model() # train the model and get X
root.mainloop()
