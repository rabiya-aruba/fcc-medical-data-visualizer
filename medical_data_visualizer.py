import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

# Import data
df = pd.read_csv("medical_examination.csv")

# Add 'overweight' column
df["overweight"] = df["weight"] / ((df["height"] / 100) ** 2)
df["overweight"] = df.apply(lambda row: int(row.overweight > 25), axis=1)


# Normalize data by making 0 always good and 1 always bad.
# If the value of 'cholestorol' or 'gluc' is 1, make the value 0.
# If the value is more than 1, make the value 1.
df["cholesterol"] = df.apply(lambda row: int(row.cholesterol > 1), axis=1)
df["gluc"] = df.apply(lambda row: int(row.gluc > 1), axis=1)


# Draw Categorical Plot
def draw_cat_plot():
    # Create DataFrame for cat plot using `pd.melt` using just the values from
    # 'cholesterol', 'gluc', 'smoke', 'alco', 'active', and 'overweight'.
    df_cat = pd.melt(df, id_vars=["cardio"],
                     value_vars=['active', 'alco', 'cholesterol', 'gluc', 'overweight', 'smoke'])

    # Group and reformat the data to split it by 'cardio'.
    # Show the counts of each feature.
    # You will have to rename one of the collumns for the catplot to work correctly.

    df_cat = pd.DataFrame(df_cat.groupby(["cardio","variable","value"])["value"].count())
    df_cat.columns=["total"]
    df_cat.reset_index(inplace=True)
    # Draw the catplot with 'sns.catplot()'
    fig = sns.catplot(data=df_cat, kind="count", x="variable", hue="value", col="cardio")
    fig.set(ylabel="total")
    fig = fig.fig
    # Do not modify the next two lines
    fig.savefig('catplot.png')
    return fig


# Draw Heat Map
def draw_heat_map():
    # Clean the data
    df_heat = df[(df["ap_lo"] <= df["ap_hi"]) &
                 (df["height"] >= df["height"].quantile(0.025)) &
                 (df["height"] <= df["height"].quantile(0.975)) &
                 (df["weight"] >= df["weight"].quantile(0.025)) &
                 (df["weight"] <= df["height"].quantile(0.975))]

    # Calculate the correlation matrix
    corr = df_heat.corr()

    # Generate a mask for the upper triangle
    mask = np.triu(corr)



    # Set up the matplotlib figure
    fig, ax = plt.subplots(figsize=(9, 9))

    # Draw the heatmap with 'sns.heatmap()'
    sns.heatmap(corr, annot=True, fmt='.1f', linewidths=1, mask=mask, vmax=.8, center=0.09, square=True,
                cbar_kws={'shrink': 0.5})
    plt.show()


    # Do not modify the next two lines
    fig.savefig('heatmap.png')
    return fig
