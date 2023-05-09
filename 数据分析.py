import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import csv

# 代码1部分
def read_csv(input_file):
    data = []
    with open(input_file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.append(row)
    return data

def write_csv(output_file, data):
    with open(output_file, 'w', newline='') as file:
        writer = csv.writer(file)
        for row in data:
            writer.writerow(row)

def extract_data(input_file, output_file):
    data = read_csv(input_file)
    extracted_data = []
    for i in range(0, len(data), 4):
        extracted_data.append(data[i])
    write_csv(output_file, extracted_data)

# 代码2部分
def read_data(file_name):
    data = pd.read_csv(file_name)
    return data

def find_slope_intercept(x, y):
    slope, intercept = np.polyfit(x, y, 1)
    return slope, intercept

def linear_func(x, a, b):
    return a * x + b

def plot_graphs(x, y, xlabel, ylabel, title):
    plt.plot(x, y, 'o', label='data')
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.legend()
    plt.show()
   

# 整合代码
input_file = 'data_input_1.csv'
output_file = 'tg_data_out.csv'
extract_data(input_file, output_file)

data = read_data(output_file)

heating_rate_ids = data['Heating_Rate_ID'].unique()
E_values = []
n_values = []
A_values = []

for heating_rate_id in heating_rate_ids:
    subset_data = data[data['Heating_Rate_ID'] == heating_rate_id]
    
    T = subset_data['Temperature']
    alpha = subset_data['Weight_Loss']
    phi = subset_data['Heating_Rate']
    dalpha_dT = np.gradient(alpha, T)

    ln_phi_dalpha_dT = np.log(phi * dalpha_dT)
    inv_T = 1 / T

    slope, intercept = find_slope_intercept(inv_T, ln_phi_dalpha_dT)
    E = -slope * 8.314
    E_values.append(E)

    plot_graphs(inv_T, ln_phi_dalpha_dT, '1/T', 'ln[ϕ(dα/dT)]', f'ln[ϕ(dα/dT)] vs 1/T for Heating Rate ID {heating_rate_id}')

    ln_A_n_alpha = ln_phi_dalpha_dT + E * inv_T
    ln_one_minus_alpha = np.log(1 - alpha)

    params, _ = curve_fit(linear_func, ln_one_minus_alpha, ln_A_n_alpha)
    n, ln_A = params
    A = np.exp(ln_A)

    n_values.append(n)
    A_values.append(A)

    plot_graphs(ln_one_minus_alpha, ln_A_n_alpha, 'ln(1-α)', 'ln[A(1-α)^n]', f'ln[A(1-α)^n] vs ln(1-α) for Heating Rate ID {heating_rate_id}')

print('活化能 E:', np.mean(E_values),'J/mol')
print('反应级数 n:', np.mean(n_values))
print('频率因子 A:', np.mean(A_values), 's^-1')
