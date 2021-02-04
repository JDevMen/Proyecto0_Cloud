import  React, {useState, useEffect} from 'react';
import { DataGrid } from '@material-ui/data-grid';
import IconButton from '@material-ui/core/IconButton';
import DeleteIcon from '@material-ui/icons/Delete';
import CheckCircleIcon from '@material-ui/icons/CheckCircle';
import CreateIcon from '@material-ui/icons/Create'
import { findRenderedComponentWithType } from 'react-dom/test-utils';
import Grid from '@material-ui/core/Grid'
import EditEventForm from './EditEventForm';





async function fetchUtils(url = '', data = {}, metodo, header) {
    // Default options are marked with *
    const response = await fetch(url, {
      method: metodo, // *GET, POST, PUT, DELETE, etc.
//      mode: 'cors', // no-cors, *cors, same-origin
//      cache: 'no-cache', // *default, no-cache, reload, force-cache, only-if-cached
//      credentials: 'same-origin', // include, *same-origin, omit
      headers: {
//        'Content-Type': 'application/octet-stream',
        ...header
        // 'Content-Type': 'application/x-www-form-urlencoded',
      },
//      redirect: 'follow', // manual, *follow, error
//      referrerPolicy: 'no-referrer', // no-referrer, *no-referrer-when-downgrade, origin, origin-when-cross-origin, same-origin, strict-origin, strict-origin-when-cross-origin, unsafe-url
    });
    return response.json(); // parses JSON response into native JavaScript objects
  }



export default function Eventos({token}) {
    const [data, setData] = useState([]); 
    const [currentEvent, setCurrentEvent] = useState({});
    useEffect(() => {
        // Update the document title using the browser API
        fetchUtils('/api/events', {}, 'GET', {'Authorization': 'Bearer '+ token }).then((values)=>{setData(values)})
      }, []);
      

      function deleteEvent(id,token){
        fetchUtils('/api/events/'+id, {},'DELETE', {'Authorization': 'Bearer '+ token }).then((values)=>{console.log(values)},
        []);
    }

    function renderEdit(){
        if (currentEvent !== {}){
            return <EditEventForm event = {currentEvent}></EditEventForm>;
        }else
        return <></>;
    }
      const columns = [
        { field: 'id', headerName: 'ID' },
        { field: 'nombre', headerName: 'Nombre' },
        { field: 'categoria', headerName: 'Categoria' },
        { field: 'lugar', headerName: 'Lugar' },
        { field: 'direccion', headerName: 'Dirección' },
        { field: 'fecha_creacion', headerName: 'Fecha Creacion' },
        { field: 'fecha_inicio', headerName: 'Fecha inicio' },
        { field: 'fecha_fin', headerName: 'Fecha fin' },
        { field: 'virtual', headerName: 'Virtual', renderCell: (params)=>(params.row.virtual ? <CheckCircleIcon />: <></>)},
        { field: 'detalle', headerName: 'Ver detalle', renderCell: (params)=>(<a onClick = {()=>{setCurrentEvent(params.row)}}>Ver detalle</a>) },
      ];
  return (
      <div>
          <h1>Tus eventos</h1>
            <div style={{ height: 400, width: '100%' }}>
            <DataGrid rows={data} columns={columns} pageSize={10} />
            </div>
            <Grid container direction= 'row' xs = {12}>
            <Grid xs={6}> <div>
                <ul>
                    <li><strong>id: </strong> {currentEvent.id}</li>
                    <li><strong>nombre: </strong> {currentEvent.nombre}</li>
                    <li><strong>categoria: </strong> {currentEvent.categoria}</li>
                    <li><strong>lugar: </strong> {currentEvent.lugar}</li>
                    <li><strong>direccion: </strong> {currentEvent.direccion}</li>
                    <li><strong>fecha_creacion: </strong> {currentEvent.fecha_creacion}</li>
                    <li><strong>fecha_inicio: </strong> {currentEvent.fecha_inicio}</li>
                    <li><strong>fecha_fin: </strong> {currentEvent.fecha_fin}</li>
                    <li><strong>virtual: </strong> {currentEvent? currentEvent.virtual? "Si": "": "No"}</li>    
                </ul>
                {{}!==currentEvent? <IconButton aria-label="delete" onClick = {()=>{deleteEvent(currentEvent.id)}}>
  <             DeleteIcon />
                </IconButton>: ""}  
            </div>
            {{}!==currentEvent? <IconButton aria-label="delete" onClick = {()=>{deleteEvent(currentEvent.id)}}>
  <             CreateIcon />
                </IconButton>: ""} 
            </Grid>
            <Grid xs={6}>
            {renderEdit()}
            </Grid> 
            </Grid>
      </div>
  );
}