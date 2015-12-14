var boolmobiili;
var booldesktop;
var tlat = 62.23252728347515; // Agoran koordinaatit oletuksena, ei mikään oikea tila
var tlon = 25.73729200674370;
var rakennusnaytetty = false;
var naytaoletus = true;
var areaId = '';
var buildingId = '';
var floorId = '';
var spaceId = '';

var $SCRIPT_ROOT = {{ request.script_root | tojson | safe }};


window.onload = function () {
    skaalaakaikki();
    var korkeus = $(window).height();
    $("#perusmobiili").css("height", korkeus * 0.7);
    $("#zoommobiili").css("height", korkeus * 0.7);

    console.log("haetaan sijaintia");

    {% if tapahtumatTanaan %}
    if (naytaoletus) {
        vaihdaTila('{{ tapahtumatTanaan[0].paikat[0].lat }}', '{{ tapahtumatTanaan[0].paikat[0].lon }}', '{{ tapahtumatTanaan[0].paikat[0].areaId }}',
            '{{ tapahtumatTanaan[0].paikat[0].buildingId }}', '{{ tapahtumatTanaan[0].paikat[0].floorId }}', '{{ tapahtumatTanaan[0].paikat[0].spaceId }}', false)
    }
    {% endif %}

}


window.onresize = function() {
    skaalaakaikki();
}


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
}


$(function () {
    $("#datepicker1").datepicker({ //TODO: napit kuukausien vaihtamiseen nakyvii
        firstDay: 1,
        dayNames: ["Sunnuntai", "Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai"],
        dayNamesMin: ['Su', 'Ma', 'Ti', 'Ke', 'To', 'Pe', 'La'],
        monthNames: ['Tammikuu', 'Helmikuu', 'Maaliskuu', 'Huhtikuu', 'Toukokuu', 'Kesakuu', 'Heinakuu', 'Elokuu', 'Syyskuu', 'Lokakuu', 'Marraskuu', 'Joulukuu'],
        monthNamesShort: ['Tammi', 'Helmi', 'Maalis', 'Huhti', 'Touko', 'Kesa', 'Heina', 'Elo', 'Syys', 'Loka', 'Marras', 'Joulu'],
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
                    console.log(data.length);
                    console.log(data);
                    for (var tapahtuma in data) {
                            var tapahtumatext = data[tapahtuma].paiva + ", "  + " klo " + data[tapahtuma].aika
                                + ". Kuvaus: " + data[tapahtuma].kuvaus;
                            var tapahtumadiv = document.createElement("div");
                            tapahtumadiv.setAttribute('class', 'list-group');
                        for (var paikka in tapahtuma) {
                            var paikkatietohref = "javascript:vaihdaTila(" + "'" + data[tapahtuma].paikat[paikka].lat + "'" + ","
                                + "'" + data[tapahtuma].paikat[paikka].lon + "'" + "," + "'" + data[tapahtuma].paikat[paikka].areaId + "'" + ","
                                + "'" + data[tapahtuma].paikat[paikka].buildingId + "'" + "," + "'" + data[tapahtuma].paikat[paikka].floorId + "'" + ","
                                + "'" + data[tapahtuma].paikat[paikka].spaceId + "')";
                            var paikkatext = data[tapahtuma].paikat[paikka].paikka;
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
        },
    });
});


$(function () {
    $("#datepickermob").datepicker({ //TODO: napit kuukausien vaihtamiseen nakyvii
        firstDay: 1,
        dayNames: ["Sunnuntai", "Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai"],
        dayNamesMin: ['Su', 'Ma', 'Ti', 'Ke', 'To', 'Pe', 'La'],
        monthNames: ['Tammikuu', 'Helmikuu', 'Maaliskuu', 'Huhtikuu', 'Toukokuu', 'Kesakuu', 'Heinakuu', 'Elokuu', 'Syyskuu', 'Lokakuu', 'Marraskuu', 'Joulukuu'],
        monthNamesShort: ['Tammi', 'Helmi', 'Maalis', 'Huhti', 'Touko', 'Kesa', 'Heina', 'Elo', 'Syys', 'Loka', 'Marras', 'Joulu'],
        showButtonPanel: true,
        dateFormat: 'yy-mm-dd',
        currentText: "Tänään", //toimiiko push nyt
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
                    console.log(data.length);
                    if (data.length == 0) {
                        var spanni = document.createElement("SPAN");
                        var text = document.createTextNode("Ei tapahtumia valitulla paivalla");
                        spanni.appendChild(text);
                        divi.appendChild(spanni);
                    }
                    console.log(data);
                    for (var tapahtuma in data) {
                            var tapahtumatext = data[tapahtuma].paiva + ", "  + " klo " + data[tapahtuma].aika
                                + ". Kuvaus: " + data[tapahtuma].kuvaus;
                            var tapahtumadiv = document.createElement("div");
                            tapahtumadiv.setAttribute('class', 'list-group');
                        for (var paikka in tapahtuma) {
                            var paikkatietohref = "javascript:vaihdaTila(" + "'" + data[tapahtuma].paikat[paikka].lat + "'" + ","
                                + "'" + data[tapahtuma].paikat[paikka].lon + "'" + "," + "'" + data[tapahtuma].paikat[paikka].areaId + "'" + ","
                                + "'" + data[tapahtuma].paikat[paikka].buildingId + "'" + "," + "'" + data[tapahtuma].paikat[paikka].floorId + "'" + ","
                                + "'" + data[tapahtuma].paikat[paikka].spaceId + "')";
                            var paikkatext = data[tapahtuma].paikat[paikka].paikka;
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
        },
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
    $("#loaderi").css("display", "none")
    rakennusnaytetty = true;
    $("#nappinaytamob").attr("value", "Rakennuksen kartta");
    $("#nappinayta").attr("value", "Rakennuksen kartta");
    if (tlat != undefined && tlon != undefined) {
        var lon = tlon;
        var lat = tlat;
        document.getElementById("ulat").value = position.coords.latitude;
        document.getElementById("ulon").value = position.coords.longitude;
        $(".kartta").attr("src", "/kartta?lat=" + lat + "&lon=" + lon + "&ulat=" + position.coords.latitude + "&ulon=" + position.coords.longitude);
        $(".karttamobiili").attr("src", "/kartta?lat=" + lat + "&lon=" + lon + "&ulat=" + position.coords.latitude + "&ulon=" + position.coords.longitude);
    }
    else {
        $(".kartta").attr("src", "/kartta?" + "ulat=" + position.coords.latitude + "&ulon=" + position.coords.longitude);
        $(".karttamobiili").attr("src", "/kartta?" + "ulat=" + position.coords.latitude + "&ulon=" + position.coords.longitude);
    }
    {% if tapahtumatTanaan %}
    if (naytaoletus) {
        vaihdaTila('{{ tapahtumatTanaan[0].paikat[0].lat }}', '{{ tapahtumatTanaan[0].paikat[0].lon }}', '{{ tapahtumatTanaan[0].paikat[0].areaId }}',
            '{{ tapahtumatTanaan[0].paikat[0].buildingId }}', '{{ tapahtumatTanaan[0].paikat[0].floorId }}', '{{ tapahtumatTanaan[0].paikat[0].spaceId }}', false)
    }
    {% endif %}
}


function skaalaakaikki(){
    sisalto = $('#sisaltodesktop');
    ekarivi = $('#ekarivi');
    tokarivi = $('#tokarivi');
    kolmasrivi = $('#kolmasrivi');
    sisalto.css('height', $(window).height() - $('#jumbotronContainer').height());
    kolmasrivi.css('height', sisalto.height() - ekarivi.height() - tokarivi.height() - 10);

    tabkaikki = $('#kaikkiTapahtumat')
    tabpalkki = $('#myTabContent');;
    tabiotsikko = $('#myTabs');
    navigointi = $('#navigointi');
    tabpalkki.css('height', navigointi.height() - tabiotsikko.height() - 25);

    kartta = $('.kartta');
    zoom = $('#zoom');
    zoom.css('height', kartta.height() * 2 );
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
    /*if (window.innerWidth < 981) {
        $('body').scrollTo('.karttamobiili');
    }
    if (boolmobiili == true){
        var korkeus = $(window).height();
        $("#nappinaytamob").attr("value", "Rakennuksen kartta");
        $(".kartta").attr("id", "perus");
        $(".karttamobiili").attr("id", "perusmobiili");

        var korkeus = $(".karttamobiili").height();
        $("#karttadiv").css("height", "");
        $("#perusmobiili").css("height", korkeus/2);
        boolmobiili = false;
        var korkeus = $(window).height();
        $("#perusmobiili").css("height", korkeus * 0.7);
       $("#zoommobiili").css("height", korkeus * 0.7);
       $(".kartta").css("height", korkeus * 0.7);
       $(".karttamobiili").css("height", korkeus * 0.7);

    }*/
    setTimeout(function () {
        console.log("Tilan tiedot ladattu");
        rakennusnaytetty = false;
        tlat = lat;
        tlon = lon;
        console.log(lat + " " + lon);
        areaId = area;
        buildingId = building;
        floorId = floor;
        spaceId = space;
        if (klikattu) naytaoletus = false;
        $(".kartta").attr("id", "perus");
        $(".karttamobiili").attr("id", "perusmobiili");
        skaalaakaikki();
        if (document.getElementById("ulat").value != "" && document.getElementById("ulon").value != "") {
            $(".kartta").attr("src", "/kartta?lat=" + lat + "&lon=" + lon + "&marker=1" + "&ulat="
                + document.getElementById("ulat").value + "&ulon=" + document.getElementById("ulon").value);
            $(".karttamobiili").attr("src", "/kartta?lat=" + lat + "&lon=" + lon + "&marker=1" + "&ulat="
                + document.getElementById("ulat").value + "&ulon=" + document.getElementById("ulon").value);
        }
        else {
            $(".kartta").attr("src", "/kartta?lat=" + lat + "&lon=" + lon + "&marker=1");
            $(".karttamobiili").attr("src", "/kartta?lat=" + lat + "&lon=" + lon + "&marker=1");
        }
        if (tlat == '') {
            $('.flash').html('<div class="alert alert-warning">Tapahtumasi tilaa ei löydy</div>');
        }
        else {
            $('.flash').html('');
        }
    }, 500);


}


function naytaRakennus() {
    if (rakennusnaytetty) {
        $("#nappinayta").attr("value", "Rakennuksen kartta");
        //TODO:???>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        $(".kartta").attr("id", "perus");
        //<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        $(".karttamobiili").attr("id", "perusmobiili");
        vaihdaTila(tlat, tlon, areaId, buildingId, floorId, spaceId);
        $("#desktopdiv").css("height", "");
    }
    else {
        $("#nappinayta").attr("value", "Nayta rakennus kartalla");
        rakennusnaytetty = true;
        if (areaId != '' &&
            buildingId != '' &&
            floorId != '' &&
            spaceId != '') {
            //TODO:????>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            $(".kartta").attr("id", "zoom");
            $(".karttamobiili").attr("id", "zoommobiili");
            skaalaakaikki;
            //<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
            $(".kartta").attr("src", encodeURI("http://navi.jyu.fi/?viewport=big#map?areaId=" + areaId +
                "&buildingId=" + buildingId + "&floorId=" + floorId + "&spaceId=" + spaceId));
            $(".karttamobiili").attr("src", encodeURI("http://navi.jyu.fi/?viewport=big#map?areaId=" + areaId +
                "&buildingId=" + buildingId + "&floorId=" + floorId + "&spaceId=" + spaceId));
            //>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
             var divkorkeus = $("#desktopdiv").height();
            //$("#desktopdiv").css("height", divkorkeus/2)
            //<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        }
        else {
            $(".kartta").attr("src", "/virhe");
            $(".karttamobiili").attr("src", "/virhe");
        }
    }
}


function naytaRakennusmob() {
    if (rakennusnaytetty) {
        var korkeus = $(window).height();
        $("#nappinaytamob").attr("value", "Rakennuksen kartta");
        //TODO:???>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        $(".kartta").attr("id", "perus");
        $(".karttamobiili").attr("id", "perusmobiili");
        //<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        vaihdaTila(tlat, tlon, areaId, buildingId, floorId, spaceId);
        //>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        var korkeus = $(".karttamobiili").height();
        $("#karttadiv").css("height", "");
        $("#perusmobiili").css("height", korkeus/2);
        //<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        boolmobiili = false;


    if (boolmobiili) {
        $("#perusmobiili").css("height", korkeus * 0.7 * 2);
       $("#zoommobiili").css("height", korkeus * 0.7 * 2);
       $(".kartta").css("height", korkeus * 0.7 * 2);
       $(".karttamobiili").css("height", korkeus * 0.7 * 2);
    }
    else {
        var korkeus = $(window).height();
        $("#perusmobiili").css("height", korkeus * 0.7);
       $("#zoommobiili").css("height", korkeus * 0.7);
       $(".kartta").css("height", korkeus * 0.7);
       $(".karttamobiili").css("height", korkeus * 0.7);
    }
    }
    else {
        $("#nappinaytamob").attr("value", "Nayta rakennus kartalla")
        rakennusnaytetty = true;
        if (areaId != '' &&
            buildingId != '' &&
            floorId != '' &&
            spaceId != '') {
            $(".kartta").attr("id", "zoom");
            $(".karttamobiili").attr("id", "zoommobiili");
            $(".kartta").attr("src", encodeURI("http://navi.jyu.fi/?viewport=big#map?areaId=" + areaId
                + "&buildingId=" + buildingId + "&floorId=" + floorId + "&spaceId=" + spaceId));
            $(".karttamobiili").attr("src", encodeURI("http://navi.jyu.fi/?viewport=big#map?areaId=" + areaId
                + "&buildingId=" + buildingId + "&floorId=" + floorId + "&spaceId=" + spaceId));
           var korkeus = $(window).height();
           $("#perusmobiili").css("height", korkeus * 0.7)
           $("#zoommobiili").css("height", korkeus * 0.7 * 2);
           var divkorkeus = $("#karttadiv").height();
            $("#karttadiv").css("height", divkorkeus/2)
            boolmobiili = true;
        }
        else {
            $(".kartta").attr("src", "/virhe");
            $(".karttamobiili").attr("src", "/virhe");
        }
    }
}
