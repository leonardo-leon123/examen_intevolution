$(document).ready( function () {
    var table = $('#table_id').DataTable
    ({
        "language": {
                "lengthMenu": "Mostrar _MENU_ registros",
                "zeroRecords": "No se encontraron resultados",
                "info": "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
                "infoEmpty": "Mostrando registros del 0 al 0 de un total de 0 registros",
                "infoFiltered": "(filtrado de un total de _MAX_ registros)",
                "sSearch": "Buscar:",
                "oPaginate": {
                    "sFirst": "Primero",
                    "sLast":"Último",
                    "sNext":"Siguiente",
                    "sPrevious": "Anterior"
			     },
			     "sProcessing":"Procesando...",
            }
    });
    $('#table_id tbody').on( 'click', 'tr', function () {
        
        if ( $(this).hasClass('selected') ) {
            $(this).removeClass('selected');
        }
        else {
            table.$('tr.selected').removeClass('selected');
            $(this).addClass('selected');
        }
    } );
    $('#eliminar').click( function () {
        var ID = table.row('.selected').data() ;
        console.log(ID[0])
        if (ID !== "")
        {
            $.ajax({
                url: '/eliminarUsuario',
                method:'POST',
                headers:
                {
                    'Content-Type':'application/json'
                },
                dataType: 'json',
                data: JSON.stringify(ID),
                success: function(ID)
                {
                    console.log('SI SE PUDO')
                    table.row('.selected').remove().draw( false );
                }
            })
        }
        
    } );
    
} );


function AgregarUsuario()
{
    var nombre = document.getElementById('nombre').value
    var edad = document.getElementById('edad').value
    var genero = document.getElementsByName('genero');
    var table = $('#table_id').DataTable();
    for (var i = 0, length = genero.length; i < length; i++) {
    if (genero[i].checked) {
        var radio = genero[i].value
    break;
  }
}
    var usuario = {
        'nombre': nombre,
        'edad': edad,
        'genero': radio
    }
    console.log(usuario)
    if(usuario !== "")
    {
        $.ajax({
            url: '/nuevoUsuario',
            method:'POST',
            headers:
            {
                'Content-Type':'application/json'
            },
            dataType: 'json',
            data: JSON.stringify(usuario),
            success: function(usuario)
            {
                var nuevoUsuario = table.row.add([nombre,edad,radio]).draw().node();
            }
        })
    }
}


