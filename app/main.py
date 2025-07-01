import os
import pickle
from flask import Blueprint, abort, render_template, request, redirect, send_file, session, url_for, flash,Response , send_from_directory 
import matplotlib.pyplot as plt
import io
import pandas as pd
import requests
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
import csv  
from datetime import datetime

main = Blueprint('main', __name__)

# Load your climate data (make sure to adjust the path)
data = pd.read_csv('static/data/climate_data.csv')

# Load the model (make sure the path is correct)
pickle_file_path = os.path.join('static', 'model', 'model.pkl')
with open(pickle_file_path, 'rb') as file:
    model = pickle.load(file)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/visualization', methods=['GET', 'POST'])
def visualization():
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.signin'))  # Redirect to login page
    if request.method == 'GET':
        return render_template('visualization.html')
    else:
        return render_template('visualization_results.html')

# Route for visualizing single variable
@main.route('/visualization_results', methods=['POST'])
def visualization_results():
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.signin'))  # Redirect to login page

    variable = request.form['variable']

    # Plot the selected variable
    fig, ax = plt.subplots()
    ax.plot(data['date'], data[variable], label=variable)
    ax.set_xlabel('Date')
    ax.set_ylabel(variable.capitalize())
    ax.legend()

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')

# Route for correlation matrix
@main.route('/correlation_matrix', methods=['POST'])
def correlation_matrix():
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.signin'))  # Redirect to login page

    # Compute correlation matrix
    corr = data[['temperature', 'humidity', 'co2_levels']].corr()

    # Plot correlation matrix
    fig, ax = plt.subplots()
    cax = ax.matshow(corr, cmap='coolwarm')
    fig.colorbar(cax)
    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.columns)))
    ax.set_xticklabels(corr.columns)
    ax.set_yticklabels(corr.columns)

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')

# Route for multi-variable comparison
@main.route('/multi_variable_comparison', methods=['POST'])
def multi_variable_comparison():
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.signin'))  # Redirect to login page

    selected_vars = request.form.getlist('variables')

    # Plot the selected variables
    fig, ax = plt.subplots()
    for var in selected_vars:
        ax.plot(data['date'], data[var], label=var)

    ax.set_xlabel('Date')
    ax.set_ylabel('Values')
    ax.legend()

    # Save plot to a BytesIO object
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)

    return send_file(img, mimetype='image/png')


@main.route('/predict', methods=['GET', 'POST'])
def predict():
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.signin'))  # Redirect to login page

    countries = {
       'USA': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
            'UK': ['London', 'Manchester', 'Birmingham', 'Liverpool', 'Glasgow'],
            'India': ['Delhi', 'Mumbai', 'Bangalore', 'Chennai', 'Hyderabad'],
            'Canada': ['Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Ottawa'],
            'Australia': ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide'],
            'Germany': ['Berlin', 'Munich', 'Frankfurt', 'Hamburg', 'Cologne'],
            'France': ['Paris', 'Marseille', 'Lyon', 'Toulouse', 'Nice'],
            'China': ['Beijing', 'Shanghai', 'Shenzhen', 'Guangzhou', 'Chengdu'],
            'Japan': ['Tokyo', 'Osaka', 'Yokohama', 'Nagoya', 'Fukuoka'],
            'Brazil': ['São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador', 'Fortaleza'],
            'Russia': ['Moscow', 'Saint Petersburg', 'Novosibirsk', 'Yekaterinburg', 'Kazan'],
            'South Africa': ['Johannesburg', 'Cape Town', 'Durban', 'Pretoria', 'Port Elizabeth'],
            'Mexico': ['Mexico City', 'Guadalajara', 'Monterrey', 'Puebla', 'Tijuana'],
            'Italy': ['Rome', 'Milan', 'Naples', 'Turin', 'Palermo'],
            'Spain': ['Madrid', 'Barcelona', 'Valencia', 'Seville', 'Zaragoza'],
            'Netherlands': ['Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 'Eindhoven'],
            'Argentina': ['Buenos Aires', 'Córdoba', 'Rosario', 'Mendoza', 'La Plata'],
            'Pakistan': ['Karachi', 'Lahore', 'Islamabad', 'Quetta', 'Multan'],
            'Saudi Arabia': ['Riyadh', 'Jeddah', 'Mecca', 'Medina', 'Dammam'],
            'Turkey': ['Istanbul', 'Ankara', 'Izmir', 'Bursa', 'Antalya'],
            'Nigeria': ['Lagos', 'Abuja', 'Kano', 'Ibadan', 'Port Harcourt'],
            'South Korea': ['Seoul', 'Busan', 'Incheon', 'Daegu', 'Daejeon'],
            'Indonesia': ['Jakarta', 'Surabaya', 'Bandung', 'Medan', 'Bekasi'],
            'Egypt': ['Cairo', 'Alexandria', 'Giza', 'Shubra El Kheima', 'Port Said'],
            'Philippines': ['Manila', 'Quezon City', 'Davao City', 'Caloocan', 'Cebu City']
    }

    selected_country = None
    selected_city = None
    prediction = None
    alert_color = "success"

    # API details
    api_key = 'acc49f75c81fdf103fdf717e168be8b1'  # Ensure this is valid
    base_url = "https://api.openweathermap.org/data/2.5/weather"

    if request.method == 'POST':
        selected_country = request.form.get('country')
        selected_city = request.form.get('city')

        if not selected_country or not selected_city:
            flash('Please select both a country and a city.', 'warning')
            return render_template('predict.html', countries=countries)

        # Construct the complete URL with country code
        complete_url = f"{base_url}?q={selected_city},{selected_country}&appid={api_key}&units=metric"
        print(f"Fetching URL: {complete_url}")  # Debug print for the URL
        response = requests.get(complete_url)

        # Check for successful API response
        if response.status_code == 200:
            weather_data = response.json()
            print(weather_data)  # Print the full API response for debugging
            current_temp = weather_data['main']['temp']  # Get temperature from API response

            # Determine alert color based on the temperature
            if current_temp > 30:
                alert_color = "danger"  # Red for high temperature
            elif current_temp < 20:
                alert_color = "warning"  # Yellow for low temperature
            else:
                alert_color = "success"  # Green for normal temperature

            # Display prediction message
            prediction = f"Current temperature for {selected_city}, {selected_country}: {current_temp:.2f}°C."
            trend = "further increase" if current_temp > 28 else "remain stable"
            prediction += f" The temperature is expected to {trend}."
        else:
            print(f"Error fetching data: {response.status_code} - {response.text}")  # Log status code and message
            flash('Failed to fetch temperature data. Please try again.', 'danger')

    return render_template('predict.html', countries=countries, selected_country=selected_country, selected_city=selected_city, prediction=prediction, alert_color=alert_color)


@main.route('/download/<format>/<country>/<city>')
def download_data(format, country, city):
    # Get the prediction data
    api_key = 'acc49f75c81fdf103fdf717e168be8b1'
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    complete_url = f"{base_url}?q={city},{country}&appid={api_key}&units=metric"
    response = requests.get(complete_url)

    if response.status_code != 200:
        flash('Failed to fetch temperature data for download.', 'danger')
        return redirect(url_for('main.predict'))

    weather_data = response.json()
    current_temp = weather_data['main']['temp']
    trend = "further increase" if current_temp > 28 else "remain stable"
    
    # Prepare data for download
    data = {
        'location': f"{city}, {country}",
        'current_temperature': current_temp,
        'prediction': f"Temperature expected to {trend}",
        'forecast': [
            {'year': 'Current', 'temperature': current_temp, 'anomaly': 'High' if current_temp > 30 else 'Low' if current_temp < 20 else 'Normal'},
            {'year': '2024', 'temperature': current_temp + 0.5, 'anomaly': '+0.5°C'},
            {'year': '2025', 'temperature': current_temp + 0.8, 'anomaly': '+0.8°C'}
        ]
    }

    # Ensure reports directory exists
    reports_dir = os.path.join('static', 'reports')
    os.makedirs(reports_dir, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"climate_report_{city}_{country}_{timestamp}"

    if format == 'csv':
        # Save CSV file
        csv_filename = f"{filename}.csv"
        csv_path = os.path.join(reports_dir, csv_filename)
        
        # Write to disk first
        with open(csv_path, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Location', 'Current Temperature', 'Prediction'])
            writer.writerow([data['location'], data['current_temperature'], data['prediction']])
            writer.writerow([])
            writer.writerow(['Year', 'Temperature', 'Anomaly'])
            for row in data['forecast']:
                writer.writerow([row['year'], row['temperature'], row['anomaly']])
        
        # Then create response
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Location', 'Current Temperature', 'Prediction'])
        writer.writerow([data['location'], data['current_temperature'], data['prediction']])
        writer.writerow([])
        writer.writerow(['Year', 'Temperature', 'Anomaly'])
        for row in data['forecast']:
            writer.writerow([row['year'], row['temperature'], row['anomaly']])
        
        output.seek(0)
        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={"Content-disposition": f"attachment; filename={csv_filename}"}
        )
        
    elif format == 'excel':
        try:
            # Save Excel file
            excel_filename = f"{filename}.xlsx"
            excel_path = os.path.join(reports_dir, excel_filename)
            
            df = pd.DataFrame(data['forecast'])
            # Write to disk first
            df.to_excel(excel_path, sheet_name='Climate Forecast', index=False)
            
            # Then create response
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Climate Forecast', index=False)
            output.seek(0)
            return Response(
                output.getvalue(),
                mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                headers={"Content-disposition": f"attachment; filename={excel_filename}"}
            )
        except ImportError:
            flash('Excel export requires xlsxwriter package. Please install it.', 'warning')
            return redirect(url_for('main.predict'))
            
    elif format == 'pdf':
        # Save PDF file
        pdf_filename = f"{filename}.pdf"
        pdf_path = os.path.join(reports_dir, pdf_filename)
        
        # Create PDF and save to disk
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []
        
        # Add title
        elements.append(Paragraph(f"Climate Data Report for {city}, {country}", styles['Title']))
        elements.append(Spacer(1, 12))
        
        # Add current data
        elements.append(Paragraph(f"Current Temperature: {current_temp}°C", styles['Heading2']))
        elements.append(Paragraph(f"Prediction: Temperature expected to {trend}", styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Add forecast table
        forecast_data = [['Year', 'Temperature', 'Anomaly']]
        for row in data['forecast']:
            forecast_data.append([row['year'], f"{row['temperature']}°C", row['anomaly']])
        
        table = Table(forecast_data)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(table)
        
        doc.build(elements)
        
        # Then create response
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        doc.build(elements)
        buffer.seek(0)
        
        return Response(
            buffer.getvalue(),
            mimetype="application/pdf",
            headers={"Content-disposition": f"attachment; filename={pdf_filename}"}
        )
        
    flash('Report downloaded successfully!', 'success')
    return redirect(url_for('main.reports'))


@main.route('/reports')
def reports():
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.signin'))
    
    # Get list of report files
    reports_dir = os.path.join('static', 'reports')
    report_files = []
    
    # Ensure directory exists
    os.makedirs(reports_dir, exist_ok=True)
    
    if os.path.exists(reports_dir):
        for filename in os.listdir(reports_dir):
            if filename.endswith(('.pdf', '.csv', '.xlsx')):
                file_path = os.path.join(reports_dir, filename)
                file_size = os.path.getsize(file_path)
                file_date = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M')
                report_files.append({
                    'name': filename,
                    'path': f"/static/reports/{filename}",  # Changed to absolute path
                    'size': f"{file_size / 1024:.1f} KB",
                    'date': file_date,
                    'type': filename.split('.')[-1].upper()
                })
    
    # Sort by date (newest first)
    report_files.sort(key=lambda x: x['date'], reverse=True)
    
    return render_template('reports.html', reports=report_files)

@main.route('/view_report/<filename>')
def view_report(filename):
    if 'username' not in session:
        flash('Please log in to access this page.', 'warning')
        return redirect(url_for('auth.signin'))
    
    # Validate filename to prevent directory traversal
    if not os.path.exists(os.path.join('static', 'reports', filename)):
        abort(404)
        
    return send_from_directory(os.path.join('static', 'reports'), filename)
