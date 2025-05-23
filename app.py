from flask import Flask, render_template, request
import requests
app = Flask(__name__)

@app.route("/")
def home():
    year_range = request.args.get("range")
    artworkList = []

    try:
        url = "https://api.artic.edu/api/v1/artworks"
        params = {
            "fields": "id,title,image_id,artist_display,date_display,main_reference_number,date_start",
            "page": 1,
            "limit": 100
        }

        if year_range:
            start_year, end_year = map(int, year_range.split("-"))
            params["date_start"] = f"{start_year}"
            params["date_end"] = f"{end_year}"

        response = requests.get(url, params=params)
        data = response.json()
        artworkList = data.get("data", [])

    except Exception as e:
        print(f"Artwork not available. Error: {e}")

    return render_template("index.html", artworkList=artworkList)
    """ try:
        response = requests.get("https://api.artic.edu/api/v1/artworks?fields=id,title,image_id,artist_display,date_display,main_reference_numb&page=1&limit=50")
        data = response.""json""()
    except:
        print("Artwork not available.")
    else:
        artworkList = data["data"]
    return render_template("index.html", artworkList=artworkList)"""

@app.route("/artworks/<int:id>")
def artworkDetail(id):
    try:
        response = requests.get(f"https://api.artic.edu/api/v1/artworks/{id}")
        data = response.json()
    except:
        print("Artwork data not available")
    else:
        artworkData = data.get("data", {})

        title = artworkData.get('title')
        artist = artworkData.get('artist_display')
        origin = artworkData.get('place_of_origin')
        imageId = artworkData.get('image_id')
        date = artworkData.get('date_start')
        description = artworkData.get('short_description')
        if description == None:
            description = ''
        medium = artworkData.get('medium_display')
        department = artworkData.get('department_title') 
        imageUrl = f"https://www.artic.edu/iiif/2/{imageId}/full/843,/0/default.jpg" 
    return render_template("artwork.html", artwork = {
        'title': title, 
        'artist': artist, 
        'origin': origin,
        'image' : imageUrl,
        'date': date,
        'description': description,
        'medium': medium,
        'department': department
    })
'''@app.route("/artworks/<int:date>")
def artworkFilter():
    try:
        response = requests.get(f"https://api.artic.edu/api/v1/artworks")
        data = response.json()
        artworkList = data["data"]
    except:
        print("Artwork data not available")
    else:
        for artwork in artworkList:
            artworkData = artwork.get("data", {})
            date = artworkData.get('date_start')
            datesArr = []
            datesArr.append(date)
    return render_template("index.html", date=date)'''
if __name__ == '__main__':
    app.run(debug=True)
