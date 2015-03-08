$(document).ready(function() {
	$('#example').dataTable( {
		"bJQueryUI": true,
		  //"dom": 'RC<"clear">lfrtip', "columnDefs": [ { "visible": "false", "targets": "1"}],
		 "bFilter": true,
		 "bPaginate":true,
		"sPaginationType": "full_numbers",
		"lengthMenu": [[10, 100, -1], [10, 100, "All"]],
		"ajax": "***fichierJson***",
		"columns": [
			{ "data": "pays" },
			{ "data": "titre"},
			{ "data": "inventeur"},
			{ "data": "applicant"},
			{ "data": "classification" },
			{ "data": "date" },				
			{ "data": "citations" },
			{ "data": "portee" },
			{ "data": "priority-active-indicator"}, 
			{ "data": "representative"},
			{ "data": "label" }
		]
	} );


$('#example thead td').each( function (a) {
        var title = $('#example thead td').eq( $(this).index() ).text();
        $(this).html( '<input type="text" id="and" placeholder="Search" '+title+'/>' );
    } );

$('#example tfoot th').each( function () {
        var title = $('#example tfoot th').eq( $(this).index() ).text();
        $(this).html( '<input type="text" placeholder="Or '+title+'" />' );
    } );
 
    // DataTable
    var table = $('#example').DataTable();

    //Fonction pour la recherche OR    
    function filter_table(param1,param2,param3,param4,param5,param6,param7,param8,param9,param10,param11){
        //$.fn.dataTable.ext.search.push(
        $.fn.dataTableExt.afnFiltering.push(
             function( settings, data, dataIndex ) {
               for(var i=0; i<11; i++)                 
                   // data[i] = data[i].toLowerCase();
                    data[i] = data[i].toLowerCase();



                     if ( data[0].search(param1) > -1 || data[1].search(param2) > -1 || data[2].search(param3) > -1 || data[3].search(param4) > -1 || data[4].search(param5) > -1 || data[5].search(param6) > -1 || data[6].search(param7) > -1 || data[7].search(param8) > -1 || data[8].search(param9) > -1 || data[9].search(param10) > -1 || data[10].search(param11) > -1)
               {return true;}
               else if(param1 == null && param2 == null && param3 == null && param4 == null && param5 == null && param6 == null && param7 == null && param8 == null && param9 == null  && param10 == null  && param11 == null )
               {return true;}
               return false;
             }
        ); 
    }    
        
    //Evenement declencheur de la recherche
    $('tfoot').find('tr').find('th').each(function(){
        $(this).find('input').on('keyup', function(){   

        	var inputText = new Array(15);
            for(var i=0; i<11; i++)
               // inputText[i] = ($.trim($('tfoot').find('tr').find('th:eq('+i+')').find('input').val()) != "")? $.trim($('tfoot').find('tr').find('th:eq('+i+')').find('input').val().toLowerCase()):null;            
                inputText[i] = ($.trim($('tfoot').find('tr').find('th:eq('+i+')').find('input').val()) != "")? $.trim($('tfoot').find('tr').find('th:eq('+i+')').find('input').val().toLowerCase()):null;            
            $.fn.dataTableExt.afnFiltering.pop();
                   filter_table(inputText[0],inputText[1],inputText[2],inputText[3],inputText[4],inputText[5],inputText[6],inputText[7],inputText[8],inputText[9],inputText[10]);
                        table.draw();    
        });
    });


table.columns().eq( 0 ).each( function ( colIdx ) {
        $( 'input', table.column( colIdx ).header() ).on( 'keyup change', function (a) {
            table
                .column( colIdx )
                .search( this.value )
                .draw();
        } ); 
    } ); 
 
 
  
 
} );