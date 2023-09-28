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
    return myChart;
}


var main = () => {

    "use strict";

    var myChart;                // riferimento al grafico creato da "createChart()"
    var firstLoading = true;    // flag per stabilire se il grafico va creato da zero o aggiornato
    var whichButton;            // variabile per stabilire quale richiesta inoltrare al server
    
    // riferimenti a metadati e dati ottenuti via http request
    var getMetadata;
    var getData;

    // riferimenti ai button per la scelta del periodo di tempo
    var $timechosers = $(".period-choser-item");

    // event listener: click
    $timechosers.on("click", function() {

        // Manipolazione delle classi CSS per effetti grafici frontend
        $timechosers.addClass("period-choser-item");
        $timechosers.removeClass("period-choser-item-active");
        $(this).removeClass("period-choser-item");
        $(this).addClass("period-choser-item-active");

        whichButton = $(this).data("value");

        // GET request
        $.ajax({
            method: "GET",
            dataType: "json",
            url: whichButton,
            success: (response) => {
                response = JSON.parse(response);
                getMetadata = response.metadata;
                getData = response.data;

                //sort
                getData.sort(function(a, b) {
                    return new Date(a.time) - new Date(b.time);
                });

                console.log(getData)

                // Se è la prima richiesta, crea il grafico
                if (firstLoading === true) {
                    let config = configurator(getMetadata, getData);
                    myChart = createChart(config);
                    firstLoading = false;
                }

                // altrimenti aggiorna quello esistente con i nuovi dati
                else {
                    myChart.data.labels = getData.map(function(data) {
                        return data.time;
                    });
                    myChart.data.datasets[0].data = getData.map(function(data) {
                        return data.value;
                    });
                    myChart.update(); // Aggiorna il grafico
                }
            }
        });

        

    });

    // Trigger automatico per il primo click al momento del caricamento
    $timechosers.eq(0).trigger("click");
};

$(document).ready(main);
