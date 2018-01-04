// this variable indicate if the locations had been loaded
var locationsLoaded = false;

function NeighborhoodMapViewModel() {
    var self = this;
    // this.data;
    this.catalogs = ko.observableArray();  // catalogs store options for the drop down menu
    // default value is less than 0, when sidebar shows the value is equal to 0, >0 when sidebar hides
    this.mapSize = ko.observable(-5);
    this.selectedChoice = ko.observable();// if you lick the hamburger button, the sidebar will not auto hide
    this.sidebarDisplay = ko.observable(false);
    this.message = ko.observable('');// message will show underneath drop down bar
    this.SIDEBAR_BREAK_POINT = 600;// if the viewport is less than 600px wide, side bar will hide automatically
    this.locations = ko.observableArray();// this will contain all the current locations that shows on the map
    this.currentPlace = null;// indicate the most recent clicked place

    $.getJSON('/places2/json', function (data) {
        // showDescription will toggle show and hide descriptions

        // viewModel.data = data;
        for (var key in data) {
            viewModel.catalogs.push(key);
            data[key].forEach(function (value) {
                value['showDescription'] = ko.observable(false);
                value['showItem'] = ko.observable(true);
                value['catalog'] = key;
                viewModel.locations.push(value)
            });
        }
    })
        .fail(function () { // show message if can not fetch data
            console.log('Something went wrong, can not fetch the data from server');
            viewModel.message('can not fetch the data from server');
        });

    // toggle sidebar display
    // we will rearrange components by changing their CSS classes
    this.toggleMenu = function () {
        if (this.mapSize() < 0) {
            var currentViewportWidth = Math.max(document.documentElement.clientWidth, window.innerWidth || 0);
            if (currentViewportWidth > this.SIDEBAR_BREAK_POINT) {
                // Initiate sidebar display statue
                this.mapSize(5);
                resizeMap();
            } else {
                this.mapSize(0);
                this.sidebarDisplay(true);
                resizeMap();
            }

        } else {
            // Switch to manual mode, auto folding manual will be disabled
            if (this.mapSize() == 0) {
                this.mapSize(5);
                resizeMap();
            } else {
                this.mapSize(0);
                resizeMap();
            }
        }
    };


    // filter function will update new data set
    this.filter = function () {
        // show only the selected markers
        if (viewModel.selectedChoice()) {
            if (viewModel.currentPlace) {
                viewModel.currentPlace().showDescription(false);
                viewModel.currentPlace = null;
            }
            if (markersDictionary) {
                for (var item in markersDictionary) {
                    if (markersDictionary[item].catalog == viewModel.selectedChoice()) {
                        markersDictionary[item].setVisible(true);
                    } else {
                        markersDictionary[item].setVisible(false);
                    } // end else
                } // end for
                //show only selected items
            } //end if(markersDictionary)
            else {
                console.log('Please waite for Markers to be loaded.');
                viewModel.message('Please waite for Markers to be loaded.');
            } // end else
            viewModel.locations().forEach(function (value) {
                    if (value['catalog'] == viewModel.selectedChoice()) {
                        value['showItem'](true);
                    } else {
                        value['showItem'](false);
                    } // end else
                } // end if
            ); // end forEach
        } // end  if (viewModel.selectedChoice())
    } // end if(viewModel.currentPlace)
} // end filter function

// below is google map JavaScript

var map;
var markersDictionary = {}; //we use a dictionary to store markers so we can access specific marker by placeID
var largeInfowindow = '';
var defaultIcon;
var highlightedIcon;
var bounds; //bounds of the markers

// when google map api JS library is loaded will call this function
function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: 37.7749, lng: -122.4194},
        zoom: 13,
        mapTypeControl: false
    });
    defaultIcon = makeMarkerIcon('0091ff');
    highlightedIcon = makeMarkerIcon('FFFF24');
    // if location has not been loaded, which means google map library is loaded after NeighborhoodMapViewModel
    if (!locationsLoaded) {
        if (viewModel.locations().length > 0) {
            // update markers at this step because
            // NeighborhoodMapViewModel can not update markers before google map library is ready
            updateMarkers(viewModel.locations());
            showMarkers();// show markers on the map
        }
    }

    // I did not use this event listener because it has a bug,
    // when the window was resize, there is a narrow grey space at the right side of the map
    // google.maps.event.addDomListener(window, 'resize', function () {
    //     google.maps.event.trigger(map, 'resize');
    //     if (bounds) {
    //         map.fitBounds(bounds);
    //
    //     } else {
    //         map.setCenter(map.getCenter());
    //     }
    // });
}

// create markers and one LargeInfowindow
// add event listener to the markers
function updateMarkers(places) {
    largeInfowindow = new google.maps.InfoWindow();

    places.forEach(function (place) {
        var marker = new google.maps.Marker({
            position: place['location'],
            title: place['title'],
            animation: google.maps.Animation.DROP,
            id: place['businessID'],
            icon: defaultIcon,
            businessID: place['businessID'],
            placeID: place['placeID'],
            catalog: place['catalog']
        });
        // marker.setMap(map);
        marker.addListener('click', function () {
            focusPlace(this.placeID, this.position);
        });
        marker.addListener('mouseover', function () {
            this.setIcon(highlightedIcon);
        });
        marker.addListener('mouseout', function () {
            if (viewModel.currentPlace) {
                if (viewModel.currentPlace().placeID != this.placeID) {
                    this.setIcon(defaultIcon);
                }
            } else {
                this.setIcon(defaultIcon);
            }
        });
        markersDictionary[place['placeID']] = marker;
    });

}

// Show markers on the map
// the map will auto zon to cover all the selected markers
function showMarkers() {
    bounds = new google.maps.LatLngBounds();

    for (var key in markersDictionary) {
        markersDictionary[key].setMap(map);
        bounds.extend(markersDictionary[key].position);
    }
    map.fitBounds(bounds);
}

// re center the map when the map window change it's size
function resizeMap() {
    var currCenter = map.getCenter();
    google.maps.event.trigger(map, 'resize');
    map.setCenter(currCenter);
    if (bounds) {
        map.fitBounds(bounds);
    } else {
        map.setCenter(map.getCenter());
    }
}

window.onresize = resizeMap;

// hide all the markers
function hideMarkers() {
    for (var key in markersDictionary) {
        markersDictionary[key].setMap(null);
    }
}

// customer marker icon
function makeMarkerIcon(markerColor) {
    var markerImage = new google.maps.MarkerImage(
        'http://chart.googleapis.com/chart?chst=d_map_spin&chld=1.15|0|' + markerColor +
        '|40|_|%E2%80%A2',
        new google.maps.Size(21, 34),
        new google.maps.Point(0, 0),
        new google.maps.Point(10, 34),
        new google.maps.Size(21, 34));
    return markerImage;
}

// show info window of a specific marker and also high light this marker
function showMarkerInfo(placeID) {
    if (viewModel.currentPlace == null) {
        if (markersDictionary[placeID]) {
            markersDictionary[placeID].setIcon(highlightedIcon);
            populateInfoWindow(markersDictionary[placeID], largeInfowindow)
        } else {
            console.log('Please waite for Markers to be loaded.');
            viewModel.message('Please waite for Markers to be loaded.');
        }
    }
}

// change a specific marker icon to default
function hideMarkerInfo(placeID) {
    if (viewModel.currentPlace == null) {
        if (markersDictionary[placeID]) {
            markersDictionary[placeID].setIcon(defaultIcon);
        } else {
            console.log('Please waite for Markers to be loaded.');
            viewModel.message('Please waite for Markers to be loaded.');
        }
    }
}

// bind marker and info window, fetch content from server and update it to the info window
function populateInfoWindow(marker, infowindow) {
    // Check to make sure the infowindow is not already opened on this marker.
    if (infowindow.marker != marker) {
        infowindow.marker = marker;
        var content = '<div><h4>' + marker.title + '</h4></div>';
        infowindow.setContent(content);
        infowindow.open(map, marker);
        $.getJSON('/yelp/' + marker.businessID + '/json', function (data) {
            var newContent = '<div><h4>' + marker.title + '</h4><p> Yelp Rating: ' + data.rating + '</p>';
            newContent += '<p> Price: ' + data.price + '</p>';
            newContent += '<img src="' + data.image_url + '" alt="' + marker.title + 'height="220" width="220">';
            infowindow.setContent(newContent);
            infowindow.open(map, marker);
            // Make sure the marker property is cleared if the infowindow is closed.
            infowindow.addListener('closeclick', function () {
                infowindow.marker = null;
            });
            viewModel.message('');
        }) // end $.getJSON
            .fail(function () {
                console.log('Something went wrong, can not fetch the data from Yelp.');
                viewModel.message('can not fetch the data from Yelp');
                var content = '<div><h4>' + marker.title + '</h4></div>';
                infowindow.setContent(content);
                infowindow.open(map, marker);
            }); // end fail()
    } // end if (infowindow.marker != marker)
} // end function populateIfoWindow

// center the map to this selected marker, high light the marker, show info window,
// at the side bar also show description of this place
function focusPlace(placeID, location) {

    if (markersDictionary[placeID]) {
        map.panTo(location);
        markersDictionary[placeID].setIcon(highlightedIcon);
        populateInfoWindow(markersDictionary[placeID], largeInfowindow);
        for (var i = 0; i < viewModel.locations().length; i++) {
            if (viewModel.locations()[i].placeID == placeID) {
                var newCurrentPlace = ko.observable(viewModel.locations()[i]);
                newCurrentPlace().showDescription(true);
                // if current place is exist and different
                if (viewModel.currentPlace) {
                    if (viewModel.currentPlace() != newCurrentPlace()) {
                        markersDictionary[viewModel.currentPlace().placeID].setIcon(defaultIcon);
                        viewModel.currentPlace().showDescription(false);
                        viewModel.currentPlace = newCurrentPlace;
                    }
                } else {
                    viewModel.currentPlace = newCurrentPlace;
                }
                break;
            } // end if viewModel.locations()[i].placeID == placeID)
        } // end for
    } else {
        console.log('Please waite for Markers to be loaded.');
        viewModel.message('Please waite for Markers to be loaded.');
    }

} // end function focusPlace

function googleError() {
    console.log('Something went wrong, can not load google map');
    viewModel.message('Something went wrong, can not load google map');
}

// create a new NeighborhoodMapViewModel instance
var viewModel = new NeighborhoodMapViewModel();
// knockout JS apply binding
ko.applyBindings(viewModel);
