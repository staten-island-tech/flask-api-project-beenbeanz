from flask import Flask, render_template, request
import requests
app = Flask(__name__)

@app.route("/")
def home():
    year_range = request.args.get("range")
    artworkList = []
    start_year = 0
    end_year = 0

    try: 
        if year_range:
            start_year, end_year = map(int, year_range.split("-"))
        
        response = requests.get("https://api.artic.edu/api/v1/artworks?fields=id,title,image_id,date_start,artist_display,date_display,main_reference_numb&page=1&limit=50")
        data = response.json()

        for artwork in data["data"]:
            if artwork['date_start'] > int(start_year) and artwork['date_start'] < int(end_year):
                artworkList.append(artwork)

    except Exception as e:
        print(f"Artwork not available. Error: {e}")

    return render_template("index.html", artworkList=artworkList)

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
