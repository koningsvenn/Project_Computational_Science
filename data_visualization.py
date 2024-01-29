import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Read CSV file
filename = '2024-01-29_14-02-50_fh1_pnd0.0008_psd0.01'
df = pd.read_csv(f'exported_data/{filename}.csv')

# Function to plot the time series of each variable
def plot_time_series(df):
    plt.figure(figsize=(12, 8))
    for column in df.columns[1:]:
        plt.plot(df['Time Step'], df[column], marker='o', linestyle='-', label=column)
    plt.title("Time Series Analysis")
    plt.xlabel("Time Step")
    plt.ylabel("Values")
    plt.legend()
    plt.grid(True)
    plt.show()

# Function to plot histograms for each variable
def plot_histograms(df):
    df.hist(bins=15, figsize=(12, 8))
    plt.suptitle("Histograms of Variables")
    plt.show()

# Function to plot scatter plots between pairs of variables
def plot_scatter_plots(df):
    sns.pairplot(df, diag_kind='kde')
    plt.suptitle("Scatter and Distribution Plots")
    plt.show()

# Function to plot a correlation matrix
def plot_correlation_matrix(df):
    plt.figure(figsize=(10, 8))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.title("Correlation Matrix")
    plt.show()

# Call the functions
plot_time_series(df)
plot_histograms(df)
plot_scatter_plots(df)
plot_correlation_matrix(df)
