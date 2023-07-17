# from flask import Flask, render_template, request
# import pandas as pd
# import folium
# import io

# app = Flask(__name__)

# @app.route('/')
# def index():
#     return render_template('map.html')

# @app.route('/view_map', methods=['POST'])
# def view_map():
#     if 'file' in request.files:
#         # Handle file upload
#         file = request.files['file']
#         if file.filename == '':
#             return 'No file selected for uploading'
#         if file:
#             dfs = pd.read_excel(file, sheet_name=None)

#             m = folium.Map(location=[0, 0], zoom_start=2)

#             # Loop through each sheet in the Excel file
#             for sheet_name, df in dfs.items():
#                 # Convert column names to lower case
#                 df.columns = map(str.lower, df.columns)

#                 if 'latitude' in df.columns and 'longitude' in df.columns:
#                     # Create the map centered at mean coordinates
#                     for _, row in df.iterrows():
#                         folium.Marker([row['latitude'], row['longitude']], popup=sheet_name).add_to(m)
#                 else:
#                     continue  # Continue with the next sheet if current sheet doesn't have latitude and longitude columns

#             # Save it to a file
#             m.save('templates/view_map.html')
#             return render_template('view_map.html')
#     else:
#         # Handle form submission
#         lat = request.form['latitude']
#         lon = request.form['longitude']
        
#         m = folium.Map(location=[lat, lon], zoom_start=6)
#         folium.Marker([lat, lon]).add_to(m)
#         m.save('templates/view_map.html')
#         return render_template('view_map.html')

# if __name__ == "__main__":
#     app.run(debug=True)


# #########################################################################
# ##### PLAYGROUND ABOVE CODE WORKS ###################

from flask import Flask, render_template, request
import pandas as pd
import folium
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('map.html')

@app.route('/view_map', methods=['POST'])
def view_map():
    if 'file' in request.files:
        # Handle file upload
        file = request.files['file']
        if file.filename == '':
            return 'No file selected for uploading'
        if file:
            dfs = pd.read_excel(file, sheet_name=None)

            m = folium.Map(location=[0, 0], zoom_start=2)

            # Loop through each sheet in the Excel file
            for sheet_name, df in dfs.items():
                # Convert column names to lower case
                df.columns = map(str.lower, df.columns)

                if 'latitude' in df.columns and 'longitude' in df.columns and 'city' in df.columns:
                    # Create the map centered at mean coordinates
                    for _, row in df.iterrows():
                        folium.Marker([row['latitude'], row['longitude']], popup=row['city']).add_to(m)
                else:
                    continue  # Continue with the next sheet if current sheet doesn't have latitude and longitude columns

            # Save it to a file
            m.save('templates/view_map.html')
            return render_template('view_map.html')
    else:
        # Handle form submission
        lat = request.form['latitude']
        lon = request.form['longitude']
        
        m = folium.Map(location=[lat, lon], zoom_start=6)
        folium.Marker([lat, lon]).add_to(m)
        m.save('templates/view_map.html')
        return render_template('view_map.html')

if __name__ == "__main__":
    app.run(debug=True)
