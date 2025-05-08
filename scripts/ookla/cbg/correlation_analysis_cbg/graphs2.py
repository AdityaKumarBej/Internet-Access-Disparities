import matplotlib.pyplot as plt
import numpy as np

def plot_santa_clara_analysis(categories, income, less_than_hs, masters_or_more, avg_speed):
    x = np.arange(len(categories))
    width = 0.5

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle('Santa Clara County - Internet Access vs Socio-Economic Factors')

    axs[0, 0].bar(x, avg_speed, width, color='orange')
    axs[0, 0].set_title('Average Download Speed')
    axs[0, 0].set_xticks(x)
    axs[0, 0].set_xticklabels(categories, rotation=15)
    axs[0, 0].set_ylabel('Mbps')

    axs[0, 1].bar(x, income, width, color='skyblue')
    axs[0, 1].set_title('Median Household Income')
    axs[0, 1].set_xticks(x)
    axs[0, 1].set_xticklabels(categories, rotation=15)
    axs[0, 1].set_ylabel('Income ($)')

    axs[1, 0].bar(x, less_than_hs, width=0.3, label='< High School', color='lightcoral')
    axs[1, 0].set_title('Only High School Education %')
    axs[1, 0].set_xticks(x)
    axs[1, 0].set_xticklabels(categories, rotation=15)
    axs[1, 0].set_ylabel('Percentage')
    axs[1, 0].legend()

    axs[1, 1].bar(x, masters_or_more, width, color='mediumpurple')
    axs[1, 1].set_title('Masters Degree or More %')
    axs[1, 1].set_xticks(x)
    axs[1, 1].set_xticklabels(categories, rotation=15)
    axs[1, 1].set_ylabel('Percentage')

    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

categories = ['Overall', 'Low Density', 'Low Density high asian_alone %']
avg_speed = [270.24, 244.40, 252.96]
avg_speed_median = [273.12, 257.56, 260.20]
income = [162468.98, 186069.10, 192882.15]
less_than_hs = [10.39, 8.26, 6.16]
masters_or_more = [27.79, 32.97, 36.66]

plot_santa_clara_analysis(categories, income, less_than_hs, masters_or_more, avg_speed)

# categories = ['Overall', 'Low Density', 'Low Density high white_alone %']
# avg_speed = [270.24, 244.40, 242.8]
# avg_speed_median = [273.12, 257.56, 257.6]
# income = [162468.98, 186069.10, 208374.6]
# less_than_hs = [10.39, 8.26, 2.2]
# masters_or_more = [27.79, 32.97, 39.4]

# plot_santa_clara_analysis(categories, income, less_than_hs, masters_or_more, avg_speed)

# categories = ['Overall', 'Low Density', 'Low Density high black_or_african_alone %']
# avg_speed = [270.24, 244.40, ]
# avg_speed_median = [273.12, 257.56, ]
# income = [162468.98, 186069.10, ]
# less_than_hs = [10.39, 8.26, ]
# masters_or_more = [27.79, 32.97, ]

# plot_santa_clara_analysis(categories, income, less_than_hs, masters_or_more, avg_speed)

# categories = ['Overall', 'Low Density', 'Low Density high hispanic_or_latino %']
# avg_speed = [270.24, 244.40, ]
# avg_speed_median = [273.12, 257.56, ]
# income = [162468.98, 186069.10, ]
# less_than_hs = [10.39, 8.26, ]
# masters_or_more = [27.79, 32.97, ]

# plot_santa_clara_analysis(categories, income, less_than_hs, masters_or_more, avg_speed)