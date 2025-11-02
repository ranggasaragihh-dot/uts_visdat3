import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

sns.set_style('whitegrid')

df = pd.read_csv('data_penjualan.csv')

df = df[df['is_valid'] == 1]
df['net_profit'] = df['after_discount'] - df['cogs']

total_value_sales = df['before_discount'].sum()
total_net_profit = df['net_profit'].sum()
total_quantity = df['qty_ordered'].sum()

df_kategori = df.groupby('category').agg({
  'before_discount': 'sum', 
  'net_profit': 'sum',
  'qty_ordered': 'sum'
}).reset_index()

df_sorted = df_kategori.sort_values(
  by='net_profit',
  ascending=False
).reset_index(drop=True)

COLOR_NET_PROFIT = '#2E8B57' 
COLOR_VALUE_SALES = '#A9A9A9'

fig, ax = plt.subplots(figsize=(10, 8))

bar_width = 0.35 
y_pos = np.arange(len(df_sorted['category']))


rects1 = ax.barh(y_pos - bar_width/2, 
                 df_sorted['before_discount'], 
                 bar_width, 
                 label='Value Sales (Rp)', 
                 color=COLOR_VALUE_SALES)


rects2 = ax.barh(y_pos + bar_width/2, 
                 df_sorted['net_profit'], 
                 bar_width, 
                 label='Net Profit (Rp)', 
                 color=COLOR_NET_PROFIT)


ax.set_yticks(y_pos)
ax.set_yticklabels(df_sorted['category'])
ax.invert_yaxis() 

ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.tick_params(axis='x', length=0) 

ax.get_xaxis().set_visible(False) 

def add_labels(rects):
    for rect in rects:
        
        ax.annotate(f'Rp {rect.get_width():,.0f}',
                    xy=(rect.get_width(), rect.get_y() + rect.get_height() / 2),
                    xytext=(5, 0), 
                    textcoords="offset points",
                    ha='left', va='center')

add_labels(rects1)
add_labels(rects2)

ax.legend(loc='lower right')

plt.tight_layout()
plt.savefig('bar_chart.png', bbox_inches='tight')
plt.show()

total_profit = f"Rp {total_net_profit:,.0f}"
total_sales = f"Rp {total_value_sales:,.0f}"





