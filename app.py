import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy 
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from wtforms.validators import ValidationError
from forms import *
from flask_migrate import Migrate
import sys
from datetime import datetime
from models import *
from forms import ArtistForm, VenueForm, ShowForm


@app.route('/')
def index():
  return render_template('pages/home.html')



@app.route('/venues')
def venues():

  distinct_venues = Venue.query.distinct(Venue.city,Venue.state)
  real_data = []
  for row in distinct_venues:
    filtered_venues = Venue.query.filter_by(city=row.city,state=row.state)
    venue_data=[]
    for f_venue in filtered_venues:
      venue_data.append({"id":f_venue.id,"name":f_venue.name})
    #data_dict["venues"][row.state]
    real_data.append({"city":row.city , "state":row.state,"venues":venue_data[:]})





  return render_template('pages/venues.html', areas=real_data);

@app.route('/venues/search', methods=['POST'])
def search_venues():
 
  searchTerm = request.form.get('search_term', '')
  Venues_search = Venue.query.filter(Venue.name.ilike("%" + searchTerm + "%")).all()

  response={}
  response["count"] = len(Venues_search)
  response["data"] = []
  for V in Venues_search :
    response["data"].append({"id" : V.id,"name" : V.name,"num_upcoming_shows" : 0})
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):


  past_shows=[]
  upcoming_shows=[]
  venue_id_data =  Venue.query.filter_by(id=venue_id)[0]
  v_shows = db.session.query(Show).join(
        Venue).filter(venue_id == Show.venue_id)


  for show in v_shows:
    start_time = show.start_time
    if(datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')<datetime.today()):
      past_shows.append({"artist_id" : show.artist_id,"artist_name" : db.session.query(Artist).get(show.artist_id).name,"artist_image_link":db.session.query(Artist).get(show.artist_id).image_link,"start_time" : show.start_time})
    else :
      upcoming_shows.append({"artist_id" : show.artist_id,"artist_name" : db.session.query(Artist).get(show.artist_id).name,"artist_image_link":db.session.query(Artist).get(show.artist_id).image_link,"start_time" : show.start_time})  

  data ={}
  data["id"] = venue_id_data.id 
  data["genres"] = venue_id_data.genres 
  data["name"] = venue_id_data.name 
  data["address"] = venue_id_data.address 
  data["city"] = venue_id_data.city 
  data["state"] = venue_id_data.state 
  data["phone"] = venue_id_data.phone 
  data["website"] = venue_id_data.website 
  data["facebook_link"] = venue_id_data.facebook_link
  data["seeking_talent"] = venue_id_data.seeking_talent
  data["seeking_description"] = venue_id_data.seeking_description
  data["image_link"] = venue_id_data.image_link
  data["past_shows"] = past_shows[:]
  data["upcoming_shows"] = upcoming_shows[:]
  data["past_shows_count"] = len(past_shows)
  data["upcoming_shows_count"] = len(upcoming_shows)
  return render_template('pages/show_venue.html', venue=data)


@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm(request.form)
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  address = request.form['address']
  phone = request.form['phone']
  image_link = request.form['image_link']
  genres = request.form.getlist('genres')
  facebook_link = request.form['facebook_link']
  website = request.form['website_link']
  seeking_description = request.form['seeking_description']
  try :
    if(request.form['seeking_talent']):
      seeking_talent = True
    else:
      seeking_talent = False 
  except :
    seeking_talent = False
  
  

  
  try:
    if len(Venue.query.filter_by(name=name).all()) > 0:
      flash('cannot create the new venue as A Venue with this name already exists.')
    else :
      db.session.add(Venue(name=name, city=city, state=state, address=address, phone=phone, image_link=image_link,
                            genres=genres, facebook_link=facebook_link,website=website, seeking_talent=seeking_talent, seeking_description=seeking_description))
      
      db.session.commit()
      flash('Venue: {0} created successfully'.format(name))
  except Exception as err:
    flash('An error occurred creating the Venue: {0}. Error: {1}'.format(name, err))
    db.session.rollback()

 
  return render_template('pages/home.html')

@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  try:
        Venue.query.filter_by(id=venue_id).delete()
        db.session.commit()
        flash('Venue was successfully deleted!')
  except:
      flash('An error occurred. Venue could not be deleted.')
      db.session.rollback()
  return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():


  distinct_Artists = Artist.query.all()
  real_data = []
  for row in distinct_Artists:
    real_data.append({"id":row.id , "name":row.name})
  return render_template('pages/artists.html', artists=real_data)

@app.route('/artists/search', methods=['POST'])
def search_artists():

  searchTerm = request.form.get('search_term', '')
  Artists_search = Artist.query.filter(Artist.name.ilike("%" + searchTerm + "%")).all()

  response={}
  response["count"] = len(Artists_search)
  response["data"] = []
  for artist in Artists_search :
    response["data"].append({"id" : artist.id,"name" : artist.name,"num_upcoming_shows" : 0})
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):  
  past_shows=[]
  upcoming_shows=[]
  Artist_id_data =  Artist.query.filter_by(id=artist_id)[0]
  v_shows = Show.query.filter_by(artist_id=artist_id).all()
  db.session.query(Show).join(
        Artist).filter(artist_id == Show.artist_id)
  for show in v_shows:
    start_time = show.start_time
    show_venue = Venue.query.filter_by(id=show.venue_id)
    if(datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')<datetime.today()):
      past_shows.append({"venue_id" : show.venue_id,"venue_name" : db.session.query(Venue).get(show.venue_id).name,"venue_image_link":db.session.query(Venue).get(show.venue_id).image_link,"start_time" : show.start_time})
    else :
      upcoming_shows.append({"venue_id" : show.artist_id,"venue_name" : db.session.query(Venue).get(show.venue_id).name,"venue_image_link":db.session.query(Venue).get(show.venue_id).image_link,"start_time" : show.start_time})  

  data ={}
  data["id"] = Artist_id_data.id 
  data["genres"] = Artist_id_data.genres 
  data["name"] = Artist_id_data.name 
  data["city"] = Artist_id_data.city 
  data["state"] = Artist_id_data.state 
  data["phone"] = Artist_id_data.phone 
  data["website"] = Artist_id_data.website 
  data["facebook_link"] = Artist_id_data.facebook_link
  data["seeking_venue"] = Artist_id_data.seeking_venue
  data["seeking_description"] = Artist_id_data.seeking_description
  data["image_link"] = Artist_id_data.image_link
  data["past_shows"] = past_shows[:]
  data["upcoming_shows"] = upcoming_shows[:]
  data["past_shows_count"] = len(past_shows)
  data["upcoming_shows_count"] = len(upcoming_shows)
  return render_template('pages/show_artist.html', artist=data)


@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()

  artist_id_data =  Artist.query.filter_by(id=artist_id)
  data = list(artist_id_data)[0]
  form.name.data = data.name
  form.genres.data = data.genres
  form.city.data = data.city
  form.state.data = data.state
  form.phone.data = data.phone
  form.website_link.data = data.website
  form.facebook_link.data = data.facebook_link
  form.seeking_venue.data = data.seeking_venue
  form.seeking_description.data = data.seeking_description
  form.image_link.data = data.image_link

  return render_template('forms/edit_artist.html', form=form, artist=data)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  artist = db.session.query(Artist).get(artist_id)
  artist.name = request.form['name']
  artist.city = request.form['city']
  artist.state = request.form['state']
  artist.phone = request.form['phone']
  artist.image_link = request.form['image_link']
  artist.genres = request.form.getlist('genres')
  artist.facebook_link = request.form['facebook_link']
  artist.website = request.form['website_link']
  artist.seeking_description = request.form['seeking_description']
  try :
    if(request.form['seeking_venue']):
      artist.seeking_venue = True
    else:
      artist.seeking_venue = False 
  except :
    artist.seeking_venue = False
  try:
    if len(Artist.query.filter_by(name=artist.name).all()) > 0:
      flash('cannot update the new Artist as an Artist with this name already exists.')
    else :
      db.session.commit()
      flash('Artist ' + request.form['name'] + ' was successfully Updated!')
  except:
      flash('An error occurred. Artist ' +
            request.form['name'] + ' could not be Updated.')
      db.session.rollback()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue_id_data =  Venue.query.filter_by(id=venue_id)
  data = list(venue_id_data)[0]
  form.name.data = data.name
  form.genres.data = data.genres
  form.city.data = data.city
  form.state.data = data.state
  form.phone.data = data.phone
  form.address.data = data.address
  form.website_link.data = data.website
  form.facebook_link.data = data.facebook_link
  form.seeking_talent.data = data.seeking_talent
  form.seeking_description.data = data.seeking_description
  form.image_link.data = data.image_link

  return render_template('forms/edit_venue.html', form=form, venue=data)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue = db.session.query(Venue).get(venue_id)
  venue.name = request.form['name']
  venue.city = request.form['city']
  venue.state = request.form['state']
  venue.phone = request.form['phone']
  venue.address = request.form['address']
  venue.image_link = request.form['image_link']
  venue.genres = request.form.getlist('genres')
  venue.facebook_link = request.form['facebook_link']
  venue.website = request.form['website_link']
  venue.seeking_description = request.form['seeking_description']
  try :
    if(request.form['seeking_talent']):
      venue.seeking_talent = True
    else:
      venue.seeking_talent = False 
  except :
    venue.seeking_talent = False
  try:
    if len(Venue.query.filter_by(name=venue.name).all()) > 0:
      flash('cannot update the new Venue as a Venue with this name already exists.')
    else :
    
      db.session.commit()
      flash('Venue ' + request.form['name'] + ' was successfully Updated!')
  except:
      flash('An error occurred. Venue ' +
            request.form['name'] + ' could not be Updated.')
      db.session.rollback()
  return redirect(url_for('show_venue', venue_id=venue_id))


@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  name = request.form['name']
  city = request.form['city']
  state = request.form['state']
  phone = request.form['phone']
  image_link = request.form['image_link']
  genres = request.form.getlist('genres')
  facebook_link = request.form['facebook_link']
  website = request.form['website_link']
  seeking_description = request.form['seeking_description']
  try :
    if(request.form['seeking_venue']):
      seeking_venue = True
    else:
      seeking_venue = False 
  except :
    seeking_venue = False
  try:

    if len(Artist.query.filter_by(name=name).all()) > 0:
      flash('cannot create the new Artist as an Artist with this name already exists.')
    else :
        db.session.add(Artist(name=name, city=city, state=state, phone=phone, image_link=image_link,
                             genres=genres,website=website, facebook_link=facebook_link, seeking_venue=seeking_venue, seeking_description=seeking_description))
        db.session.commit()
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
  except:
      flash('An error occurred. Artist ' +
            request.form['name'] + ' could not be listed.')
      db.session.rollback()
  return render_template('pages/home.html')


@app.route('/shows')
def shows():
 
  shows = db.session.query(Show).join(Artist).filter(
        Artist.id == Show.artist_id).all()
  real_data = []
  for row in shows:
    Venue_data = db.session.query(Venue).get(row.venue_id)
    Artist_data = db.session.query(Artist).get(row.artist_id)
    real_data.append({"venue_id":row.venue_id , "artist_id":row.artist_id, "start_time":row.start_time, "venue_name":Venue_data.name ,"artist_name":Artist_data.name,"artist_image_link" :Artist_data.image_link })

  return render_template('pages/shows.html', shows=real_data)

@app.route('/shows/create')
def create_shows():
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  start_time = request.form['start_time']
  artist_id = request.form['artist_id']
  venue_id = request.form['venue_id']

  try:
        db.session.add(Show(artist_id=artist_id,venue_id=venue_id,start_time=start_time))
        db.session.commit()
        flash('Show was successfully listed!')
  except:
      flash('An error occurred. Show could not be listed.')
      db.session.rollback()
  return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')



# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
