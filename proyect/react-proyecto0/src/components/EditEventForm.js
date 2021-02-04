import { TextField } from '@material-ui/core';
import  React, {useState, useEffect} from 'react';

export default function EditEventForm( { event } ) {
    const [nombre, setnombre] = useState(event.nombre);
    const [categoria, setcategoria] = useState(event.categoria);
    const [lugar, setlugar] = useState(event.lugar);
    const [direccion, setdireccion] = useState(event.direccion);
    const [fecha_creacion, setfecha_creacion] = useState(event.fecha_creacion);
    const [fecha_inicio, setfecha_inicio] = useState(event.fecha_inicio);
    const [fecha_fin, setfecha_fin] = useState(event.fecha_fin);
    const [virtual, setVirtual] = useState(event.virtual);
  
    const onChangeNombre = (event) => { setnombre( event.target.checked ) };
    const onChangeCategoria = (event) => { setcategoria( event.target.checked ) };
    const onChangeLugar = (event) => { setlugar( event.target.checked ) };
    const onChangeDireccion = (event) => { setdireccion( event.target.checked ) };
    const onChangeInicio = (event) => { setfecha_creacion( event.target.checked ) };
    const onChangeFechaInicio = (event) => { setfecha_inicio( event.target.checked ) };
    const onChangeFechaFin = (event) => { setfecha_fin( event.target.checked ) };
    const onChangeVirtual = (event) => { setVirtual( event.target.checked ) };
  
    function sendEdit(){
      const changes = {
        "id": event.id,
        nombre,
        categoria,
        lugar,
        direccion,
        fecha_creacion,
        fecha_inicio,
        fecha_fin,
        virtual
      };
  
      console.info( changes );
    }
    
    return (
        <form noValidate autoComplete="off">
          <div>
            <TextField required label="Required" value={ nombre } onChange={ onChangeNombre } />
            <TextField required label="Required" value={ categoria } onChange={ onChangeCategoria } />
            <TextField required label="Required" value={ lugar } onChange={ onChangeLugar } />
            <TextField required label="Required" value={ direccion } onChange={ onChangeDireccion } />
            <TextField required label="Required" value={ fecha_creacion } onChange={ onChangeInicio } />
            <TextField required label="Required" value={ fecha_inicio } onChange={ onChangeFechaInicio } />
            <TextField required label="Required" value={ fecha_fin } onChange={ onChangeFechaFin } />
            <TextField required label="Required" value={ virtual } onChange={ onChangeVirtual } />
          </div>
          <button onClick={ sendEdit }>Editar info</button>
        </form>
    );
  }