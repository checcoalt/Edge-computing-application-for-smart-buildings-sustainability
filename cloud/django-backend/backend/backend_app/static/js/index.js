
var getMetadata = {
    type: 'line',
    mainLabel: "Temperature (°C)"
}

var getData = [
    { time: '00:00', value: 20 },
    { time: '00:30', value: 19.5 },
    { time: '01:00', value: 19 },
    { time: '01:30', value: 18.5 },
    { time: '02:00', value: 18 },
    { time: '02:30', value: 17.5 },
    { time: '03:00', value: 17 },
    { time: '03:30', value: 17.5 },
    { time: '04:00', value: 18 },
    { time: '04:30', value: 18.5 },
    { time: '05:00', value: 19 },
    { time: '05:30', value: 19.5 },
    { time: '06:00', value: 20 },
    { time: '06:30', value: 21 },
    { time: '07:00', value: 22 },
    { time: '07:30', value: 23 },
    { time: '08:00', value: 24 },
    { time: '08:30', value: 25 },
    { time: '09:00', value: 26 },
    { time: '09:30', value: 27 },
    { time: '10:00', value: 28 },
    { time: '10:30', value: 29 },
    { time: '11:00', value: 30 },
    { time: '11:30', value: 30.5 },
    { time: '12:00', value: 31 },
    { time: '12:30', value: 31.5 },
    { time: '13:00', value: 32 },
    { time: '13:30', value: 32.5 },
    { time: '14:00', value: 32 },
    { time: '14:30', value: 31.5 },
    { time: '15:00', value: 31 },
    { time: '15:30', value: 30.5 },
    { time: '16:00', value: 30 },
    { time: '16:30', value: 29.5 },
    { time: '17:00', value: 29 },
    { time: '17:30', value: 28.5 },
    { time: '18:00', value: 28 },
    { time: '18:30', value: 27.5 },
    { time: '19:00', value: 27 },
    { time: '19:30', value: 26.5 },
    { time: '20:00', value: 26 },
    { time: '20:30', value: 25.5 },
    { time: '21:00', value: 25 },
    { time: '21:30', value: 24.5 },
    { time: '22:00', value: 24 },
    { time: '22:30', value: 23.5 },
    { time: '23:00', value: 23 },
    { time: '23:30', value: 22.5 }
];

// Estrai le etichette (orari) e i valori delle temperature dai dati

var configurator = (getMetadata, getData) => {

    var labels = getData.map(function(data) {
        return data.time;
    });

    var values = getData.map(function(data) {
        return data.value;
    });

    // Configurazione del grafico
    var config = {
        type: getMetadata.type,
        data: {
        labels: labels,
        datasets: [{
            label: getMetadata.mainLabel,
            data: values,
            fill: false,
            borderColor: '#2364AA',
            borderWidth: 2
        }]
        },
        options: {
            scales: {
                x: {
                    beginAtZero: false,
                    grid: {
                        color: "rgba(17, 11, 17, 0.6)"
                    },
                    ticks: {
                        color: '#110B11'
                    }
                },
                y: {
                    beginAtZero: false,
                    grid: {
                        color: "rgba(17, 11, 17, 0.6)"
                    },
                    ticks: {
                        color: "#110B11"
                    }
                }
            },
            plugins: {
                tooltip: {
                    bodyColor: '#F7F0F5', // Cambia il colore del testo delle label dei tooltip a bianco
                    backgroundColor: '#110B11', // Cambia il colore dello sfondo delle label dei tooltip
                    titleColor: '#F7F0F5'
                },
                legend: {
                    labels: {
                        color: "rgba(17, 11, 17, 1)"
                    }
                }
            }
        }
    };
    return config;
};
  
// Creazione del grafico
var createChart = (config) => {
    var ctx = document.getElementById('chart').getContext('2d');
    var myChart = new Chart(ctx, config);
}


var main = () => {

    "use strict";

    var $timechosers = $(".period-choser-item");

    $timechosers.on("click", function() {
        $timechosers.addClass("period-choser-item");
        $timechosers.removeClass("period-choser-item-active");
        $(this).removeClass("period-choser-item");
        $(this).addClass("period-choser-item-active");

        // $.ajax();
        // ritorna getMetadata, getData
        let config = configurator(getMetadata, getData);
        createChart(config);
    });

    $timechosers.eq(0).trigger("click");
};

$(document).ready(main);
