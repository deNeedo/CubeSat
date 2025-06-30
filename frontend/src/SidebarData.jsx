import React from "react";

export default function SidebarData({speed, setSpeed, state}) {
    if (state == null) return <div> Awaiting Satellite Info... </div>;
    const {name, datetime, position_geo, velocity, solar_flux, magnetic_field, in_shadow, visible} = state;
	function toString(dt) {
		const date = dt.split('T')[0];
		const time = (dt.split('T')[1]).split('.')[0]
		const timezone = (dt.split('T')[1]).split('+')[1]
		return date + " " + time + "+" + timezone
	}
	const updateSpeed = async (newSpeed) => {
		setSpeed(newSpeed);
		await fetch('http://localhost:8000/speed', {
			method: 'POST',
			headers: {'Content-Type': 'application/json'},
			body: JSON.stringify({speed: newSpeed}),
		});
	}
	const resetSimulation = async () => {
		await fetch('http://localhost:8000/reset', {
			method: 'POST',
		});
		window.location.reload();
	}
    return (
		<div className="h-full flex flex-rowflex flex-col">
			<div className="flex-99">
				<h2 className="text-xl font-bold mb-4"> Satellite Info </h2>
				<p> Name: {name} </p>
				<p> Latitude: {position_geo[0].toFixed(6)}° </p>
				<p> Longitude: {position_geo[1].toFixed(6)}° </p>
				<p> Altitude: {position_geo[2].toFixed(6)} km </p>
				<p> Velocity: {velocity.toFixed(8)} km/s </p>
				{/* <p> Solar Flux: {solar_flux.toFixed(4)} </p> */}
				<p> Magnetic Field: {magnetic_field.toFixed(2)} nT </p>
				<p> In shadow? {in_shadow ? "TRUE" : "FALSE"} </p>
				<p> Visible? {visible} </p>
			</div>
			<div className="flex-1">
				<button onClick={resetSimulation}> Reset Simulation </button> <br/> <br/>
				<label> Simulation Speed: {speed.toFixed(1)}x </label>
				<input type="range" min="-50" max="50" step="1" value={speed} onChange={(e) => updateSpeed(parseFloat(e.target.value))} />
				<p> {toString(datetime)} </p>
			</div>
		</div>


    );
}
