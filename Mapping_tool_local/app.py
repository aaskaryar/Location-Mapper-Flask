# from flask import Flask, render_template, request
# import pandas as pd
# import folium

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

#             # Concatenate data from all sheets into a single DataFrame
#             df_combined = pd.concat(dfs.values(), ignore_index=True)

#             # Convert column names to lower case
#             df_combined.columns = map(str.lower, df_combined.columns)

#             if 'actual_latitude' in df_combined.columns and 'actual_longitude' in df_combined.columns and 'stationcode' in df_combined.columns:
#                 # Drop rows with missing latitude or longitude values
#                 df_combined = df_combined.dropna(subset=['actual_latitude', 'actual_longitude'])

#                 # Create the map centered at mean coordinates
#                 for _, row in df_combined.iterrows():
#                     folium.Marker([row['actual_latitude'], row['actual_longitude']], popup=row['stationcode']).add_to(m)

#                 # Save it to a file
#                 m.save('templates/view_map.html')
#                 return render_template('view_map.html')

#     # If the latitude and longitude columns are not found or an error occurs, render the error message
#     return render_template('error.html', message='Actual Latitude, Actual Longitude, or StationCode columns not found or an error occurred.')


# if __name__ == "__main__":
#     app.run(debug=True)


# # # #########################################################################
# # # ##### PLAYGROUND ABOVE CODE WORKS ###################

from flask import Flask, request, render_template
from werkzeug.utils import secure_filename
import os
import pandas as pd
import folium
from folium import plugins

app = Flask(__name__)

# This is the path to the upload directory
app.config['UPLOAD_FOLDER'] = './uploads'

# These are the extension that we are accepting to be uploaded
app.config['ALLOWED_EXTENSIONS'] = {'xlsx'}

# For a given file, return whether it's an allowed type or not
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    # Get the name of the uploaded file
    file = request.files['file']
    # Check if the file is one of the allowed types/extensions
    if file and allowed_file(file.filename):
        # Make the filename safe, remove unsupported chars
        filename = secure_filename(file.filename)
        # Move the file form the temporal folder to
        # the upload folder we setup
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        # Redirect the user to the uploaded_file route, which
        # will basically show on the browser the uploaded file
        # Load an example dataframe
        df = pd.read_excel(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Verify the existence of 'actual_latitude' and 'actual_longitude' columns
        if 'actual_latitude' not in df.columns or 'actual_longitude' not in df.columns:
            return "Error: The uploaded file must contain 'actual_latitude' and 'actual_longitude' columns."

        # Create a map centered around the mean coordinates
        m = folium.Map(location=[df['actual_latitude'].mean(), df['actual_longitude'].mean()], zoom_start=13)

        # Add a marker for each point in the dataframe
        for i, row in df.iterrows():
            folium.Marker(location=[row['actual_latitude'], row['actual_longitude']]).add_to(m)
        # Save it to html
        m.save('/path/to/save/html/map.html')

        return "File Uploaded and Map Created!"

if __name__ == '__main__':
    app.run(debug=True)
