var tlat = 62.23252728347515; // Agoran koordinaatit oletuksena, ei mikään oikea tila
var tlon = 25.73729200674370;
var rakennusnaytetty = false;
var naytaoletus = true;
var areaId = '';
var buildingId = '';
var floorId = '';
var spaceId = '';



window.onload = function () {
    skaalaakaikki();
    naytaNykyinen()
};


window.onresize = function() {
    skaalaakaikki();
};


$.fn.scrollTo = function (target, options, callback) {
    if (typeof options == 'function' && arguments.length == 2) {
        callback = options;
        options = target;
    }
    var settings = $.extend({
        scrollTarget: target,
        offsetTop: 0,
        duration: 500,
        easing: 'swing'
    }, options);
    return this.each(function () {
        var scrollPane = $(this);
        var scrollTarget = (typeof settings.scrollTarget == "number") ? settings.scrollTarget : $(settings.scrollTarget);
        var scrollY = (typeof scrollTarget == "number") ? scrollTarget : scrollTarget.offset().top + scrollPane.scrollTop() - parseInt(settings.offsetTop);
        scrollPane.animate({scrollTop: scrollY}, parseInt(settings.duration), settings.easing, function () {
            if (typeof callback == 'function') {
                callback.call(this);
            }
        });
    });
};


$(function () {
    $("#datepicker1").datepicker({
        firstDay: 1,
        dayNames: ["Sunnuntai", "Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai"],
        dayNamesMin: ['Su', 'Ma', 'Ti', 'Ke', 'To', 'Pe', 'La'],
        monthNames: ['Tammikuu', 'Helmikuu', 'Maaliskuu', 'Huhtikuu', 'Toukokuu', 'Kesakuu',
                        'Heinakuu', 'Elokuu', 'Syyskuu', 'Lokakuu', 'Marraskuu', 'Joulukuu'],
        monthNamesShort: ['Tammi', 'Helmi', 'Maalis', 'Huhti', 'Touko', 'Kesa',
                            'Heina', 'Elo', 'Syys', 'Loka', 'Marras', 'Joulu'],
        showButtonPanel: true,
        dateFormat: 'yy-mm-dd',
        currentText: "Tänään",
        prevText: "Edellinen",
        nextText: "Seuraava",
        altField: '#sendDate',
        onSelect: function () {
            $(function () {
                $.getJSON($SCRIPT_ROOT + '/calday', {
                    selected_date: document.getElementById("sendDate").value
                }, function (data) {
                    divi = document.getElementById("valitutTapahtumat");
                    while (divi.firstChild) {
                        divi.removeChild(divi.firstChild);
                    }
                    for (var tapahtuma in data) {
                        var dataTapahtuma = data[tapahtuma];
                        var tapahtumatext = dataTapahtuma.paiva + ", "  + " klo " + dataTapahtuma.aika
                                + ". Kuvaus: " + dataTapahtuma.kuvaus;
                            var tapahtumadiv = document.createElement("div");
                            tapahtumadiv.setAttribute('class', 'list-group');
                        for (var paikka in tapahtuma) {
                            var tapahtumaPaikka = dataTapahtuma.paikat[paikka];
                            var paikkatietohref = "javascript:vaihdaTila(" + "'" + tapahtumaPaikka.lat + "'" + ","
                                + "'" + tapahtumaPaikka.lon + "'" + "," + "'" + tapahtumaPaikka.areaId + "'" + ","
                                + "'" + tapahtumaPaikka.buildingId + "'" + "," + "'" + tapahtumaPaikka.floorId + "'" + ","
                                + "'" + tapahtumaPaikka.spaceId + "')";
                            var paikkatext = tapahtumaPaikka.paikka;
                            var paikkaelem = document.createElement('a');
                            paikkaelem.setAttribute('class', 'list-group-item');
                            paikkaelem.setAttribute("href", paikkatietohref);
                            paikkaelem.textContent = paikkatext;
                            tapahtumadiv.appendChild(paikkaelem);
                        }
                            var elementa = document.createElement("a");
                            elementa.textContent = tapahtumatext;
                            elementa.setAttribute("class", "list-group-item");
                            document.getElementById("valitutTapahtumat").appendChild(elementa);
                            document.getElementById('valitutTapahtumat').appendChild(tapahtumadiv);

                    }
                });
                return false;
            });
        }
    });
});


$(function () {
    $("#datepickermob").datepicker({
        firstDay: 1,
        dayNames: ["Sunnuntai", "Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai"],
        dayNamesMin: ['Su', 'Ma', 'Ti', 'Ke', 'To', 'Pe', 'La'],
        monthNames: ['Tammikuu', 'Helmikuu', 'Maaliskuu', 'Huhtikuu', 'Toukokuu', 'Kesakuu',
                        'Heinakuu', 'Elokuu', 'Syyskuu', 'Lokakuu', 'Marraskuu', 'Joulukuu'],
        monthNamesShort: ['Tammi', 'Helmi', 'Maalis', 'Huhti', 'Touko', 'Kesa',
                            'Heina', 'Elo', 'Syys', 'Loka', 'Marras', 'Joulu'],
        showButtonPanel: true,
        dateFormat: 'yy-mm-dd',
        currentText: "Tänään",
        prevText: "Edellinen",
        nextText: "Seuraava",
        altField: '#sendDate',
        onSelect: function () {
            $(function () {
                $.getJSON($SCRIPT_ROOT + '/calday', {
                    selected_date: document.getElementById("sendDate").value
                }, function (data) {
                    divi = document.getElementById("valitutTapahtumatmob");
                    while (divi.firstChild) {
                        divi.removeChild(divi.firstChild);
                    }
                    if (data.length == 0) { //TODO: Ilmoituksesta samanlainen <li> kuin tapahtumastakin
                        var spanni = document.createElement("SPAN");
                        var text = document.createTextNode("Ei tapahtumia valitulla päivällä");
                        spanni.appendChild(text);
                        divi.appendChild(spanni);
                    }
                    for (var tapahtuma in data) {
                            var dataTapahtuma = data[tapahtuma];
                            var tapahtumatext = dataTapahtuma.paiva + ", "  + " klo " + dataTapahtuma.aika
                                + ". Kuvaus: " + dataTapahtuma.kuvaus;
                            var tapahtumadiv = document.createElement("div");
                            tapahtumadiv.setAttribute('class', 'list-group');
                        for (var paikka in tapahtuma) {
                            var tapahtumaPaikka = dataTapahtuma.paikat[paikka];
                            var paikkatietohref = "javascript:vaihdaTila(" + "'" + tapahtumaPaikka.lat + "'" + ","
                                + "'" + tapahtumaPaikka.lon + "'" + "," + "'" + tapahtumaPaikka.areaId + "'" + ","
                                + "'" + tapahtumaPaikka.buildingId + "'" + "," + "'" + tapahtumaPaikka.floorId + "'" + ","
                                + "'" + tapahtumaPaikka.spaceId + "')";
                            var paikkatext = tapahtumaPaikka.paikka;
                            var paikkaelem = document.createElement('a');
                            paikkaelem.setAttribute('class', 'list-group-item');
                            paikkaelem.setAttribute("href", paikkatietohref);
                            paikkaelem.textContent = paikkatext;
                            tapahtumadiv.appendChild(paikkaelem);
                        }
                            var elementa = document.createElement("a");
                            elementa.textContent = tapahtumatext;
                            elementa.setAttribute("class", "list-group-item");
                            document.getElementById("valitutTapahtumatmob").appendChild(elementa);
                            document.getElementById('valitutTapahtumatmob').appendChild(tapahtumadiv);

                    }
                });
                return false;
            });
        }
    });
});


function getLocation() {
    try {
        if (navigator.geolocation) {
            navigator.geolocation.getCurrentPosition(showPosition, failed, {enableHighAccuracy: true});
        } else {
            // TODO: Kerrro kayttajalle
        }
    }
    catch (err) {
        console.log(err.message)
    }
}


    function failed () {

    }


function showPosition(position) {
    console.log("sijainti haettu");
    $("#loaderi").css("display", "none");

    rakennusnaytetty = true;
    $("#nappinaytamob").attr("value", "Rakennuksen kartta");
    $("#nappinayta").attr("value", "Rakennuksen kartta");

    var kartta = $("#kartta");
    var karttamobiili = $("#karttamobiili");
    var pos_latitude = position.coords.latitude;
    var pos_longitude = position.coords.longitude;
    if (tlat != undefined && tlon != undefined) {
        var lon = tlon;
        var lat = tlat;
        document.getElementById("ulat").value = pos_latitude;
        document.getElementById("ulon").value = pos_longitude;
        kartta.attr("src", "/kartta?lat=" + lat + "&lon=" + lon + "&ulat=" + pos_latitude + "&ulon=" + pos_longitude);
        karttamobiili.attr("src", "/kartta?lat=" + lat + "&lon=" + lon + "&ulat=" + pos_latitude + "&ulon=" + pos_longitude);
    }
    else {
        kartta.attr("src", "/kartta?" + "ulat=" + pos_latitude + "&ulon=" + pos_longitude);
        karttamobiili.attr("src", "/kartta?" + "ulat=" + pos_latitude + "&ulon=" + pos_longitude);
    }
    naytaNykyinen()
}


function skaalaakaikki(){
    var korkeus =  $(window).height();

    var sisalto = $('#sisaltodesktop');
    var ekarivi = $('#ekarivi');
    var tokarivi = $('#tokarivi');
    var kolmasrivi = $('#kolmasrivi');
    sisalto.css('height', korkeus - $('#jumbotron').height());
    kolmasrivi.css('height', sisalto.height() - ekarivi.height() - tokarivi.height() - 10);

    var tabpalkki = $('#myTabContent');
    var tabiotsikko = $('#myTabs');
    var navigointi = $('#navigointi');
    tabpalkki.css('height', navigointi.height() - tabiotsikko.height() - 25);

    var iframedivdesktop = $('#desktopdiv');
    var zoom = $('.zoom');
    zoom.css('height', iframedivdesktop.height() * 2 );

    var iframedivmobiili = $('#karttadiv');
    var zoommobiili = $('.zoommobiili');
    zoommobiili.css('height', iframedivmobiili.height() * 2 );

    iframedivmobiili.css('height', korkeus * 0.7);
    $(".perusmobiili").css("height", korkeus * 0.7);
    $(".perus").css("height", korkeus * 0.7);
}


function uusiOsoite() {
    var input = document.getElementById("url");
    input.value = input.getAttribute("value");
    input.value = "";
    location.reload()
}


function haeppaSijainti() {
    $("#loaderi").css("display", "block");
    getLocation();
}


function vaihdaTila(lat, lon, area, building, floor, space, klikattu) {
    if (window.innerWidth < 981) {
        $('body').scrollTo('#karttamobiili');
    }
    var kartta = $("#kartta");
    var karttamobiili = $("#karttamobiili");

    setTimeout(function () {
        console.log("Tilan tiedot ladattu");
        rakennusnaytetty = false;
        $("#nappinayta").attr("value", "Rakennuksen kartta");
        $("#nappinaytamob").attr("value", "Rakennuksen kartta");
        tlat = lat;
        tlon = lon;
        console.log(lat + " " + lon);
        areaId = area;
        buildingId = building;
        floorId = floor;
        spaceId = space;
        if (klikattu) naytaoletus = false;
        kartta.attr("class", "perus");
        karttamobiili.attr("class", "perusmobiili");
        skaalaakaikki();
        if (document.getElementById("ulat").value != "" && document.getElementById("ulon").value != "") {

            kartta.attr("src", "/kartta?lat=" + lat + "&lon=" + lon + "&marker=1" + "&ulat="
                + document.getElementById("ulat").value + "&ulon=" + document.getElementById("ulon").value);

            karttamobiili.attr("src", "/kartta?lat=" + lat + "&lon=" + lon + "&marker=1" + "&ulat="
                + document.getElementById("ulat").value + "&ulon=" + document.getElementById("ulon").value);
        }
        else {
            kartta.attr("src", "/kartta?lat=" + lat + "&lon=" + lon + "&marker=1");
            karttamobiili.attr("src", "/kartta?lat=" + lat + "&lon=" + lon + "&marker=1");
        }
        if (tlat == '') {
            $('.flash').html('<div class="alert alert-warning">Tapahtumasi tilaa ei löydy</div>');
            skaalaakaikki();
        }
        else {
            $('.flash').html('');
            skaalaakaikki();
        }
    }, 500);
}


function naytaRakennus() {
    var kartta = $("#kartta");
    var karttamobiili =$("#karttamobiili");
    var nappidesk = $("#nappinayta");
    var nappimob = $("#nappinaytamob");

    if (rakennusnaytetty) {
        kartta.attr("class", "perus");
        karttamobiili.attr("class", "perusmobiili");

        vaihdaTila(tlat, tlon, areaId, buildingId, floorId, spaceId);
    }
    else {
        nappidesk.attr("value", "Nayta rakennus kartalla");
        nappimob.attr("value", "Nayta rakennus kartalla");
        rakennusnaytetty = true;
        if (areaId != '' &&
            buildingId != '' &&
            floorId != '' &&
            spaceId != '') {
            kartta.attr("class", "zoom");
            karttamobiili.attr("class", "zoommobiili");
            skaalaakaikki();
            kartta.attr("src", encodeURI("http://navi.jyu.fi/?viewport=big#map?areaId=" + areaId +
                "&buildingId=" + buildingId + "&floorId=" + floorId + "&spaceId=" + spaceId));
            karttamobiili.attr("src", encodeURI("http://navi.jyu.fi/?viewport=big#map?areaId=" + areaId +
                "&buildingId=" + buildingId + "&floorId=" + floorId + "&spaceId=" + spaceId));
        }
        else {
            kartta.attr("src", "/virhe");
            karttamobiili.attr("src", "/virhe");
        }
    }
}