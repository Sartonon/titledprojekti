function uusiOsoite() {
        var input = document.getElementById("url");
        input.value = input.getAttribute("value");
        input.value = "";
        location.reload()

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

    var $SCRIPT_ROOT = {{ request.script_root|tojson|safe }};

    $(function () {
        $("#datepicker1").datepicker({ //TODO: napit kuukausien vaihtamiseen nakyvii
            firstDay: 1,
            dayNames: ["Sunnuntai", "Maanantai", "Tiistai", "Keskiviikko", "Torstai", "Perjantai", "Lauantai"],
            dayNamesMin: ['Su', 'Ma', 'Ti', 'Ke', 'To', 'Pe', 'La'],
            monthNames: ['Tammikuu', 'Helmikuu', 'Maaliskuu', 'Huhtikuu', 'Toukokuu', 'Kesakuu', 'Heinakuu', 'Elokuu', 'Syyskuu', 'Lokakuu', 'Marraskuu', 'Joulukuu'],
            monthNamesShort: ['Tammi', 'Helmi', 'Maalis', 'Huhti', 'Touko', 'Kesa', 'Heina', 'Elo', 'Syys', 'Loka', 'Marras', 'Joulu'],
            showButtonPanel: true,
            dateFormat: 'yy-mm-dd',
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
                        console.log(data.length)
                        console.log(data);
                        for (var pussy in data) {
                            var paikkatietohref = "javascript:vaihdaTila(" + "'" + data[pussy].lat + "'" + "," + "'" + data[pussy].lon + "'" + "," + "'" + data[pussy].areaId + "'" + "," + "'" + data[pussy].buildingId + "'" + "," + "'" + data[pussy].floorId + "'" + "," + "'" + data[pussy].spaceId + "')";
                            var paikkatietotext = data[pussy].paiva + ", " + data[pussy].paikka + " klo " + data[pussy].aika + ". Kuvaus: " + data[pussy].kuvaus;
                            var elementa = document.createElement("a");
                            elementa.textContent = paikkatietotext;
                            elementa.setAttribute("href", paikkatietohref);
                            elementa.setAttribute("class", "list-group-item");
                            document.getElementById("valitutTapahtumat").appendChild(elementa);
                            //document.getElementById("valittua").href = paikkatietohref;
                            //document.getElementById("valittua").textContent = paikkatietotext;
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
                        for (var pussy in data) {
                            var paikkatietohref = "javascript:vaihdaTila(" + "'" + data[pussy].lat + "'" + "," + "'" + data[pussy].lon + "'" + "," + "'" + data[pussy].areaId + "'" + "," + "'" + data[pussy].buildingId + "'" + "," + "'" + data[pussy].floorId + "'" + "," + "'" + data[pussy].spaceId + "')";
                            var paikkatietotext = data[pussy].paiva + ", " + data[pussy].paikka + " klo " + data[pussy].aika + ". Kuvaus: " + data[pussy].kuvaus;
                            var elementa = document.createElement("a");
                            elementa.textContent = paikkatietotext;
                            elementa.setAttribute("href", paikkatietohref);
                            elementa.setAttribute("class", "list-group-item");
                            document.getElementById("valitutTapahtumatmob").appendChild(elementa);
                            //document.getElementById("valittua").href = paikkatietohref;
                            //document.getElementById("valittua").textContent = paikkatietotext;
                        }

                    });
                    return false;
                });
            },
        });
    });


    var tlat = 62.23252728347514; // Agoran koordinaatit oletuksena
    var tlon = 25.73729200674369;
    var rakennusnaytetty = false;
    var naytaoletus = true;
    var areaId = 'None';
    var buildingId = 'None';
    var floorId = 'None';
    var spaceId = 'None';

    window.onload = function () {
        var korkeus = $(window).height();
        console.log(korkeus/2);
        $("#karttamobiili").css("height", korkeus/2)

        console.log("haetaan sijaintia");
        $("#loaderi").css("display", "block")
        getLocation();
        {%  if tapahtumatTanaan %}
            if (naytaoletus) {
                vaihdaTila('{{ tapahtumatTanaan[0].lat }}', '{{ tapahtumatTanaan[0].lon }}', '{{ tapahtumatTanaan[0].areaId }}',
                        '{{ tapahtumatTanaan[0].buildingId }}', '{{ tapahtumatTanaan[0].floorId }}', '{{ tapahtumatTanaan[0].spaceId }}', false)
            }
        {% endif %}
    };


    function vaihdaTila(lat, lon, area, building, floor, space, klik) {
        $('body').scrollTo('.kartta');

        setTimeout(function () {
            console.log("Tilan tiedot ladattu");
            rakennusnaytetty = false;
            tlat = lat;
            tlon = lon;
            areaId = area;
            buildingId = building;
            floorId = floor;
            spaceId = space;
            if (klik) naytaoletus = false;
            if (document.getElementById("ulat").value != "" && document.getElementById("ulon").value != "") {
                $(".kartta").attr("src", "/kartta?lat=" + lat + "&lon=" + lon + "&marker=1" + "&ulat=" + document.getElementById("ulat").value + "&ulon=" + document.getElementById("ulon").value);
            }
            else {
                $(".kartta").attr("src", "/kartta?lat=" + lat + "&lon=" + lon + "&marker=1");
            }
        }, 500);


    }

    function naytaRakennus() {
        if (rakennusnaytetty) {
            $("#nappinayta").attr("value", "Nayta rakennuksen kartta")
            vaihdaTila(tlat, tlon, areaId, buildingId, floorId, spaceId)
        }
        else {
            $("#nappinayta").attr("value", "Nayta rakennus kartalla")
            rakennusnaytetty = true;
            if (areaId != 'None' &&
                    buildingId != 'None' &&
                    floorId != 'None' &&
                    spaceId != 'None') {
                $(".kartta").attr("src", encodeURI("http://navi.jyu.fi/?viewport=big#map?areaId=" + areaId + "&buildingId=" + buildingId + "&floorId=" + floorId + "&spaceId=" + spaceId));
            }
            else {
                $(".kartta").attr("src", "/virhe");
            }
        }
    }

    function naytaRakennusmob() {
        if (rakennusnaytetty) {
            $("#nappinaytamob").attr("value", "Nayta rakennuksen kartta")
            vaihdaTila(tlat, tlon, areaId, buildingId, floorId, spaceId)
        }
        else {
            $("#nappinaytamob").attr("value", "Nayta rakennus kartalla")
            rakennusnaytetty = true;
            if (areaId != 'None' &&
                    buildingId != 'None' &&
                    floorId != 'None' &&
                    spaceId != 'None') {
                $(".kartta").attr("src", encodeURI("http://navi.jyu.fi/?viewport=big#map?areaId=" + areaId + "&buildingId=" + buildingId + "&floorId=" + floorId + "&spaceId=" + spaceId));
            }
            else {
                $(".kartta").attr("src", "/virhe");
            }
        }
    }

    function getLocation() {
        try {
            if (navigator.geolocation) {
                navigator.geolocation.getCurrentPosition(showPosition);
            } else {
                // TODO: Kerrro kayttajalle
            }
        }
        catch (err) {
            console.log(err.message)
        }
    }

    function showPosition(position) {
        console.log("sijainti haettu");
        $("#loaderi").css("display", "none")
        if (tlat != undefined && tlon != undefined) {
            var lon = tlon;
            var lat = tlat;
            document.getElementById("ulat").value = position.coords.latitude;
            document.getElementById("ulon").value = position.coords.longitude;
            $(".kartta").attr("src", "/kartta?lat=" + lat + "&lon=" + lon + "&ulat=" + position.coords.latitude + "&ulon=" + position.coords.longitude);
        }
        else {
            $(".kartta").attr("src", "/kartta?" + "ulat=" + position.coords.latitude + "&ulon=" + position.coords.longitude);
        }
        {%  if tapahtumatTanaan %}
            if (naytaoletus) {
                vaihdaTila('{{ tapahtumatTanaan[0].lat }}', '{{ tapahtumatTanaan[0].lon }}', '{{ tapahtumatTanaan[0].areaId }}',
                        '{{ tapahtumatTanaan[0].buildingId }}', '{{ tapahtumatTanaan[0].floorId }}', '{{ tapahtumatTanaan[0].spaceId }}', false)
            }
        {% endif %}
    }