function initMap() {
  var map = new google.maps.Map(document.getElementById('map'), {
    zoom: 17,
    center: {
      lat: -36.7895748,
      lng: 174.7284535
    },
    mapTypeId: 'hybrid'
  });
  firebase.database().ref().once('value', function(snap) {
    var heatmapData = [];
    var i = 0;
    var n = snap.numChildren();
    snap.forEach(function(data) {
        var point = new google.maps.LatLng(
        data.child('lat').val(),
        data.child('lng').val()
      );
      heatmapData.push(point);
      if (++i === n) {
        new google.maps.Marker({
            title: new Date(parseInt(data.key)*1000).toString(),
          position: point,
          map: map
        });
      }
    });
    new google.maps.visualization.HeatmapLayer({
      data: heatmapData,
      radius: 20,
      map: map
    });
  });
}
