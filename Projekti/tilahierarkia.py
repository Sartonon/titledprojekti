#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2016  Jose Malmberg, Toni Pitkänen, Santeri Rusila, Markus Valkama
#
#
# This file is part of Karttakotka.
#
# Karttakotka is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# Karttakotka is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Karttakotka.  If not, see <http://www.gnu.org/licenses/>.

def rakennukset():
    rakennukset = {
        'Ag': 'Agora',
        'B': 'Kirjasto',
        'D': 'Educa',
        'F': 'Fennicum',
        'FYS1': 'Fysiikan laitosrakennus',
        'FYS2': 'Fysiikan laitosrakennus',
        'FYS3': 'Fysiikan laitosrakennus',
        'FYS4': 'Fysiikan laitosrakennus',
        'FYS5': 'Fysiikan laitosrakennus',
        'Fysiikan': 'Fysiikan laitosrakennus',
        'H': 'Historica',
        'L': 'Liikuntarakennus',
        'L144': 'Liikuntarakennus',
        'L149C': 'Liikuntarakennus',
        'L157': 'Liikuntarakennus',
        'L158': 'Liikuntarakennus',
        'M': 'Musica',
        'MaA': 'Mattilanniemi A',
        'MaD': 'Mattilanniemi D',
        'O': 'Oppio',
        'Oppio': 'Oppio',
        'P': 'Philologica',
        'Philologica': 'Philologica',
        'PiA': 'Philologica',
        'PiB': 'Philologica',
        'S': 'Seminarium',
        'Sauna': 'Fennicum',
        'Seminarium': 'Seminarium',
        'Soveltava': 'Soveltava kemia',
        'Y33': 'Y33',
        'YA': 'Ambiotica',
        'YAA 303': 'Ambiotica',
        'YAA204': 'Ambiotica',
        'YAA305': 'Ambiotica',
        'YAB314': 'Ambiotica',
        'YAB320': 'Ambiotica',
        'YAB322': 'Ambiotica',
        'YAB324': 'Ambiotica',
        'YE': 'Kemian laitosrakennus',
        'YF': 'Kemian laitosrakennus',
        'YFL': 'Fysiikan laitosrakennus',
        'YFL': 'Fysiikan laitosrakennus',
        'YN': 'NanoScience Center',
        'YO': 'Kemian laitosrakennus',
        'Yn': 'NanoScience Center',
        'A': 'Athenaeum'
    }
    return rakennukset


def alueet():
    alueet = {
        'Agora': 'Mattilanniemi',
        'Ambiotica': 'Seminaarinmäki',
        'Athenaeum': 'Seminaarinmäki',
        'Educa': 'Seminaarinmäki',
        'Fennicum': 'Seminaarinmäki',
        'Fysiikan laitosrakennus': 'Ylistönrinne',
        'Historica': 'Seminaarinmäki',
        'Kemian laitosrakennus': 'Ylistönrinne',
        'Kirjasto': 'Seminaarinmäki',
        'Liikuntarakennus': 'Seminaarinmäki',
        'Mattilanniemi A': 'Mattilanniemi',
        'Mattilanniemi D': 'Mattilanniemi',
        'Musica': 'Seminaarinmäki',
        'NanoScience Center': 'Ylistönrinne',
        'Oppio': 'Seminaarinmäki',
        'Philologica': 'Seminaarinmäki',
        'Seminarium': 'Seminaarinmäki',
        'Soveltava kemia': 'Ylistönrinne',
        'Y33': 'Ylistönrinne',
    }
    return alueet


def agora():
    agora = {
        'Alfa': 1,
        'Beeta': 1,
        'Gamma': 2,
        'Delta': 2,
        'Auditorio': 1
    }
    return agora


def erikoistilat():
    erikoistilat = {
        'Ag Auditorio 1': 'Ag A102',
        'Ag Auditorio 2': 'Ag B103',
        'Ag Auditorio 3': 'Ag B105',
        'Ag B212.2 (Mountains)': 'Ag B212.2',
        'Ag B113.1 (Europe)': 'Ag B113.1',
        'Ag B112.2 (Latin)': 'Ag B112.2',
        'Ag B213.1 (Lakes)': 'Ag B213.1',
        'Ag B212.1 (Finland)': 'Ag B212.1',
        'Ag B112.1 (Africa)': 'Ag B112.1',
        'Ag B111.1 (Asia)': 'Ag B111.1',
        'Ag B211.1 (Sovjet)': 'Ag B211.1',
        'Ag C231': 'Ag C231.1',
        'Martti Ahtisaari -sali': 'Ag A102',
        'YlistoKem1': 'YK 306',
        'YlistoKem2': 'YK 305',
        'YlistoKem3': 'YK 205'
    }
    return erikoistilat
