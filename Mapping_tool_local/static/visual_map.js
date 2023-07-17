require([
    'esri/Map',
    'esri/views/MapView'
  ], function(Map, MapView) {
    var map = new Map({
      // Configure the map properties here
    });
  
    var view = new MapView({
      container: 'viewDiv', // The ID of the container div in your HTML
      map: map,
      // Configure the view properties here
    });
  });
  