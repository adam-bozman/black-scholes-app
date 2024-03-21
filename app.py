# black_scholes

import streamlit as st
import numpy as np
from scipy.stats import norm
import yfinance as yf

# Black-Scholes formula for European call and put options
def black_scholes(S, K, T, r, sigma, q=0.0, option_type="call"):
    """
    S: stock price
    K: strike price
    T: time to maturity in years
    r: risk-free interest rate
    q: dividend yield
    sigma: volatility of the underlying asset
    option_type: 'call' or 'put'
    """
    d1 = (np.log(S / K) + (r - q + 0.5 * sigma ** 2) * T) / (sigma * np.sqrt(T))
    d2 = d1 - sigma * np.sqrt(T)
    
    if option_type == "call":
        price = S * np.exp(-q * T) * norm.cdf(d1) - K * np.exp(-r * T) * norm.cdf(d2)
    elif option_type == "put":
        price = K * np.exp(-r * T) * norm.cdf(-d2) - S * np.exp(-q * T) * norm.cdf(-d1)
    else:
        raise ValueError("Invalid option type. Use 'call' or 'put'.")
    
    return price

# Function to fetch real-time stock price
def get_stock_price(symbol):
    stock = yf.Ticker(symbol)
    hist = stock.history(period="1d")
    return hist['Close'][0]  # Return the last closing price

# Streamlit UI
st.title('Black-Scholes Option Price Calculator')

# User input
ticker_symbol = st.text_input('Enter Stock Ticker:', 'AAPL').upper()  # Default to AAPL
strike_price = st.number_input('Enter Strike Price:', value=100.0)
time_to_maturity_days = st.number_input('Enter Time to Maturity (in days):', value=365, format='%d')
risk_free_rate_percent = st.number_input('Enter Risk-Free Rate (%):', value=5.0)
# volatility = st.number_input('Enter Volatility (as a decimal):', value=0.2)
volatility_percent = st.number_input('Enter Volatility (%):', value=20.0)
option_type = st.selectbox('Select Option Type:', ['call', 'put'])

# Convert volatility from percentage to decimal for the calculation
volatility_decimal = volatility_percent / 100.0

# Convert time to maturity from days to years, and risk-free rate from percentage to decimal
time_to_maturity_years = time_to_maturity_days / 365.0
risk_free_rate_decimal = risk_free_rate_percent / 100.0

# Fetch the current stock price
current_price = get_stock_price(ticker_symbol)

# Display the current stock price (formatted to two decimal places)
st.write(f"Current Price of {ticker_symbol}: ${current_price:.2f}")

# Calculate and display the option price
if st.button('Calculate Option Price'):
    S = float(current_price)
    K = float(strike_price)
    T = float(time_to_maturity_years)
    r = float(risk_free_rate_decimal)
    sigma = float(volatility_decimal)  # Use the converted decimal value
    q = 0.0  # Assuming no dividend yield (q=0.0) for simplicity; adjust as needed

    option_price = black_scholes(S, K, T, r, sigma, q, option_type)
    # Display the option price in large and bold text
    st.markdown(f"**The {option_type} option price is: ${option_price:.2f}**", unsafe_allow_html=True)
    
    # Calculate and display the total cost of one contract (100 options)
    total_cost = option_price * 100  # One contract is typically 100 options
    st.markdown(f"**Total cost for one contract (100 options): ${total_cost:.2f}**", unsafe_allow_html=True)
