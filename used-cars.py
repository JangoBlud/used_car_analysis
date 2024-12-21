import pandas as pd
import streamlit as st
import plotly.express as px

# Streamlit Page Configuration
st.set_page_config(page_title="🚗 Used Car Market Analysis", layout="wide")
st.title("🚘 Used Car Market Analysis - Pakistan")

# Load Dataset
file_path = "dataset.csv"  # Path to the uploaded dataset

# Try loading the data
try:
    data = pd.read_csv(file_path)
    st.write("✅ Dataset Loaded Successfully!")
except Exception as e:
    st.error(f"❌ Failed to load dataset: {e}")
    st.stop()

# Dataset Cleaning
st.subheader("🔧 Cleaning Dataset...")

# Remove duplicates
initial_count = len(data)
data = data.drop_duplicates()
duplicates_removed = initial_count - len(data)
st.write(f"Removed **{duplicates_removed}** duplicate rows.")

# Handle missing values
missing_count = data.isnull().sum().sum()
data = data.dropna()
st.write(f"Removed **{missing_count}** rows with missing values.")

# Convert numerical columns to proper types
numeric_columns = ['price', 'mileage', 'year']
for col in numeric_columns:
    if col in data.columns:
        data[col] = pd.to_numeric(data[col], errors='coerce')

# Handle invalid rows (e.g., non-numeric values in numeric columns)
before_invalid_removal = len(data)
data = data.dropna(subset=numeric_columns)
invalid_rows_removed = before_invalid_removal - len(data)
st.write(f"Removed **{invalid_rows_removed}** rows with invalid numeric values.")

# Normalize categorical columns
categorical_columns = ['model', 'fuel_type', 'transmission', 'color', 'city']
for col in categorical_columns:
    if col in data.columns:
        data[col] = data[col].str.strip().str.lower()

st.write("✅ Data Cleaning Complete!")

# Preview Cleaned Data
st.subheader("📋 Cleaned Data Preview")
st.dataframe(data)

# Total Used Cars
total_cars = len(data)
st.metric(label="🚗 Total Used Cars", value=total_cars)

# Basic Statistical Analysis
st.subheader("📊 Basic Statistical Overview")
statistics = {
    "Total Cars": len(data),
    "Average Price (PKR in Lakhs)": f"{data['price'].mean() / 100_000:,.2f}",
    "Average Mileage (km/l)": f"{data['mileage'].mean():.2f}",
    "Oldest Car Year": int(data['year'].min()),
    "Newest Car Year": int(data['year'].max())
}
st.json(statistics)

# Car Model Count Bar Chart
if 'model' in data.columns:
    st.subheader("🚗 Most Popular Car Models")
    model_counts = data['model'].value_counts().reset_index()
    model_counts.columns = ['model', 'count']
    fig_model = px.bar(model_counts.head(15), x='model', y='count', title="Top 15 Car Models by Count",
                       color='count', color_continuous_scale='Blues')
    st.plotly_chart(fig_model)
    st.download_button("Download Chart", fig_model.to_html(), file_name="model_count.html")

# Fuel Type Distribution Pie Chart
if 'fuel_type' in data.columns:
    st.subheader("⛽ Fuel Type Distribution")
    fuel_counts = data['fuel_type'].value_counts()
    fig_fuel = px.pie(values=fuel_counts.values, names=fuel_counts.index, title="Fuel Type Distribution",
                      color_discrete_sequence=px.colors.sequential.Viridis)
    st.plotly_chart(fig_fuel)
    st.download_button("Download Chart", fig_fuel.to_html(), file_name="fuel_type_distribution.html")

# Transmission Type Distribution Pie Chart
if 'transmission' in data.columns:
    st.subheader("🔄 Transmission Type Distribution")
    transmission_counts = data['transmission'].value_counts()
    fig_transmission = px.pie(values=transmission_counts.values, names=transmission_counts.index,
                              title="Transmission Distribution",
                              color_discrete_sequence=px.colors.sequential.Plasma)
    st.plotly_chart(fig_transmission)
    st.download_button("Download Chart", fig_transmission.to_html(), file_name="transmission_distribution.html")

# Price Distribution Analysis
if 'price' in data.columns:
    st.subheader("💸 Price Distribution")
    data['price_in_lakhs'] = data['price'] / 100_000
    fig_price = px.histogram(data, x='price_in_lakhs', nbins=50, title="Distribution of Car Prices",
                             labels={'price_in_lakhs': 'Price (Lakhs of PKR)'},
                             color_discrete_sequence=['#636EFA'])
    st.plotly_chart(fig_price)
    st.download_button("Download Chart", fig_price.to_html(), file_name="price_distribution.html")

# Mileage Analysis
if 'mileage' in data.columns and 'price' in data.columns:
    st.subheader("📏 Mileage vs Price")
    data['price_in_lakhs'] = data['price'] / 100_000
    filtered_data = data[(data['price_in_lakhs'] <= 300) & (data['price_in_lakhs'] >= 1)]  # Filter to remove extreme outliers
    fig_mileage_price = px.scatter(filtered_data, x='mileage', y='price_in_lakhs',
                                   title="Mileage vs Price",
                                   labels={'mileage': 'Mileage (km/l)', 'price_in_lakhs': 'Price (Lakhs of PKR)'},
                                   color='price_in_lakhs', color_continuous_scale='Viridis')
    st.plotly_chart(fig_mileage_price)
    st.download_button("Download Chart", fig_mileage_price.to_html(), file_name="mileage_vs_price.html")

# Car Availability Trends Over Years
if 'year' in data.columns:
    st.subheader("📈 Car Availability Trends Over Years")
    year_counts = data['year'].value_counts().reset_index()
    year_counts.columns = ['year', 'count']
    fig_year = px.line(year_counts.sort_values('year'), x='year', y='count', title="Car Availability Over Years",
                       color_discrete_sequence=['#EF553B'])
    st.plotly_chart(fig_year)
    st.download_button("Download Chart", fig_year.to_html(), file_name="car_availability_trends.html")

# Most Common Car Colors
if 'color' in data.columns:
    st.subheader("🎨 Most Common Car Colors")
    color_counts = data['color'].value_counts().reset_index()
    color_counts.columns = ['color', 'count']
    fig_color = px.bar(color_counts.head(15), x='color', y='count', title="Top 15 Most Common Car Colors",
                       color='count', color_continuous_scale='Teal')
    st.plotly_chart(fig_color)
    st.download_button("Download Chart", fig_color.to_html(), file_name="car_colors.html")

# Statistical: Average Price by Year
if 'year' in data.columns and 'price' in data.columns:
    st.subheader("📈 Average Price by Year")
    avg_price_year = data.groupby('year')['price'].mean().reset_index()
    avg_price_year['price_in_lakhs'] = avg_price_year['price'] / 100_000
    fig_avg_price = px.line(avg_price_year, x='year', y='price_in_lakhs', title="Average Price Over Years",
                            labels={'year': 'Year', 'price_in_lakhs': 'Average Price (Lakhs of PKR)'},
                            color_discrete_sequence=['#FFA15A'])
    st.plotly_chart(fig_avg_price)
    st.download_button("Download Chart", fig_avg_price.to_html(), file_name="average_price_by_year.html")

# Statistical: Most Common Cities for Cars
if 'city' in data.columns:
    st.subheader("🏙️ Most Common Cities for Cars")
    city_counts = data['city'].value_counts().reset_index()
    city_counts.columns = ['city', 'count']
    fig_city = px.bar(city_counts.head(10), x='city', y='count', title="Top 10 Cities by Car Listings",
                      color='count', color_continuous_scale='Cividis')
    st.plotly_chart(fig_city)
    st.download_button("Download Chart", fig_city.to_html(), file_name="most_common_cities.html")

st.success("🎉 Analysis complete! Explore the interactive visualizations.")
