import streamlit as st
import matplotlib.pyplot as plt
import json

# Updated JSON data with "price" and optional "news" keys.
stocks_data = """
{
  "Apple": [{"price": 120}, {"price": 122}, {"price": 121, "news": "Apple announces new product"}, {"price": 123}],
  "Meta": [{"price": 250}, {"price": 252}, {"price": 251}, {"price": 253, "news": "Meta faces regulatory scrutiny"}],
  "SPY": [{"price": 370}, {"price": 372}, {"price": 371}, {"price": 373, "news": "SPY reaches all-time high"}],
  "Google": [{"price": 1520}, {"price": 1522}, {"price": 1521}, {"price": 1523, "news": "Google acquires startup"}],
  "Amazon": [{"price": 3100}, {"price": 3102}, {"price": 3101}, {"price": 3103, "news": "Amazon enters new market"}],
  "Tesla": [{"price": 700}, {"price": 702}, {"price": 701}, {"price": 703, "news": "Tesla unveils new battery technology"}],
  "Microsoft": [{"price": 210}, {"price": 212}, {"price": 211, "news": "Microsoft announces layoffs"}, {"price": 213}],
  "NVIDIA": [{"price": 500}, {"price": 502}, {"price": 501}, {"price": 503, "news": "NVIDIA releases new GPU"}],
  "PayPal": [{"price": 140}, {"price": 142}, {"price": 141}, {"price": 143, "news": "PayPal expands into cryptocurrency"}],
  "Netflix": [{"price": 350}, {"price": 352}, {"price": 351}, {"price": 353, "news": "Netflix announces new series"}]
}
"""

# Convert JSON data to a Python dictionary.
stocks = json.loads(stocks_data)

# Initialize a session state to keep track of the index.
if 'index' not in st.session_state:
    st.session_state.index = 3  # Starting with the first 3 values

def plot_individual_stock(stock_name, entries):
    """Function to plot an individual stock and handle news items."""
    fig, ax = plt.subplots()
    prices = [entry["price"] for entry in entries[:st.session_state.index]]
    news_items = [entry.get("news", None) for entry in entries[:st.session_state.index]]
    
    ax.plot(prices, marker='o', linestyle='-')
    ax.set_xlabel('Time')
    ax.set_ylabel('Price')
    ax.set_title(stock_name)

    # Annotate with news, if any
    for i, news in enumerate(news_items):
        if news:
            ax.annotate(news, (i, prices[i]), textcoords="offset points", xytext=(0,10), ha='center')

    # Calculate and display performance
    if st.session_state.index > 1:
        initial_value = prices[0]
        current_value = prices[-1]
        change = (current_value - initial_value) / initial_value * 100
        direction = "up" if change > 0 else "down"
        performance_text = f"{stock_name} went {direction} by {abs(change):.2f}%. Latest news: {news_items[-1] if news_items[-1] else 'No recent news.'}"
    else:
        performance_text = "Insufficient data for performance analysis."

    return fig, performance_text

def update_chart():
    """Function to update the chart with the next value."""
    if st.session_state.index < len(next(iter(stocks.values()))):  # Check if more data is available
        st.session_state.index += 1

# Display the stocks in a 3x3 grid
grid_cols = st.columns(3)  # Create 3 columns
col_index = 0

for stock_name, entries in stocks.items():
    with grid_cols[col_index]:
        fig, performance_text = plot_individual_stock(stock_name, entries)
        st.pyplot(fig)
        st.caption(performance_text)
    col_index = (col_index + 1) % 3  # Cycle through columns

# Button to update the chart
st.button('Pass Time', on_click=update_chart)
