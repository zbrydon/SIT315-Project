const SERVER_URL = 'http://localhost:3000';


$('#current').on('click' , () => {
    $.get(`${SERVER_URL}/current` ).then((res) => {
        let cnt = 0;
        $("#devices tbody tr").remove(); 
        res.forEach((device) => {
            $('#devices tbody').append(` <tr data-device-id=${cnt}>
                    <td>${device.id}</td>
                    <td>${device.temp}</td>
                    <td>${device.avg_temp}</td>
                    <td>${device.time}</td>
                    <td>${JSON.stringify(device.location.lat)}</td>
                    <td>${JSON.stringify(device.location.lng)}</td>
                </tr>` );
            cnt++;
        });
    })
})

$('#avg').on('click' , () => {
    $.get(`${SERVER_URL}/avg` ).then((res) => {
        let cnt = 0;
        $("#devices tbody tr").remove(); 
        res.forEach((device) => {
            $('#devices tbody').append(`  <tr data-device-id=${cnt}>
                    <td>${device.id}</td>
                    <td>${device.temp}</td>
                    <td>${device.avg_temp}</td>
                    <td>${device.time}</td>
                    <td>${JSON.stringify(device.location.lat)}</td>
                    <td>${JSON.stringify(device.location.lng)}</td>
                </tr>` );
            cnt++;
        });
    })
})